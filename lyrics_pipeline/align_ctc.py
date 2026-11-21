"""Onset-accurate timing on the isolated voice.

WHY THIS EXISTS
- Whisper's forced alignment marks a long held word late (near where the note ends), so captions appeared as she
  finished a word instead of as she began it. A CTC model scores every 20 ms of audio against letters, so a word's
  start is where its first sound is actually heard.
- The orchestra confuses any aligner, so the voice is separated first (Demucs) and only the voice is aligned.
- Because CTC gives a total score for "this text over this stretch of audio", it can also TEST a repeat:
  does "نسيت نسيت النوم" fit the sound better than "نسيت النوم"? (see best_variant)

Model: jonatasgrosman/wav2vec2-large-xlsr-53-arabic (Arabic letters, 20 ms steps), downloaded once from Hugging Face.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

from arabic_text import normalize

MODEL = "jonatasgrosman/wav2vec2-large-xlsr-53-arabic"
STEP = 0.02
_m = None


def vocals(wav: Path) -> Path:
    """Separate the singing voice from the orchestra (cached next to the clip's audio as vocals16k.wav)."""
    out = wav.parent / "vocals16k.wav"
    if out.exists() and out.stat().st_size > 1000:
        return out
    tmp = wav.parent / "_demucs"
    r = subprocess.run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", str(tmp), str(wav)], capture_output=True)
    src = tmp / "htdemucs" / wav.stem / "vocals.wav"
    if r.returncode != 0 or not src.exists():
        return wav                       # separation failed: fall back to the full mix
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", "16000", str(out)], capture_output=True)
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return out if out.exists() else wav


def read(wav: Path):
    import wave
    with wave.open(str(wav)) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    return a, sr


def _load():
    global _m
    if _m is None:
        import torch
        from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
        proc = Wav2Vec2Processor.from_pretrained(MODEL)
        mdl = Wav2Vec2ForCTC.from_pretrained(MODEL).to("cuda" if torch.cuda.is_available() else "cpu").eval()
        vocab = proc.tokenizer.get_vocab()
        _m = (proc, mdl, vocab, proc.tokenizer.pad_token_id, vocab.get("|"))
    return _m


def emissions(audio: np.ndarray):
    """Log-probabilities of every letter for every 20 ms of this audio."""
    import torch
    proc, mdl, *_ = _load()
    x = proc(audio, sampling_rate=16000, return_tensors="pt").input_values.to(mdl.device)
    with torch.no_grad():
        return torch.log_softmax(mdl(x).logits, dim=-1).cpu()        # [1, T, C]


def _tokens(text: str):
    """Text -> letter ids the model knows, plus which word each letter belongs to."""
    _, _, vocab, _, bar = _load()
    ids, word_of = [], []
    words = normalize(text).split()
    kept = []
    for w in words:
        t = [vocab[c] for c in w if c in vocab]
        if not t:
            continue
        if ids and bar is not None:
            ids.append(bar); word_of.append(-1)
        ids.extend(t); word_of.extend([len(kept)] * len(t))
        kept.append(w)
    return ids, word_of, len(kept)


def align_text(em, text: str):
    """Best placement of `text` in this audio. -> (word spans [(start_sec, end_sec, confidence)], total log-likelihood)."""
    import torch
    import torchaudio.functional as AF
    _, _, _, blank, _ = _load()
    ids, word_of, nwords = _tokens(text)
    if not ids or em.shape[1] < len(ids) + 2:
        return [], float("-inf")
    al, sc = AF.forced_align(em, torch.tensor([ids]), blank=blank)
    al, sc = al[0].tolist(), sc[0].tolist()
    spans = [[None, None, []] for _ in range(nwords)]
    k, prev = -1, blank
    for fr, tok in enumerate(al):
        if tok != blank and tok != prev:
            k += 1                                        # a new letter of the text starts on this frame
        if tok != blank and 0 <= k < len(word_of) and word_of[k] >= 0:
            s = spans[word_of[k]]
            if s[0] is None:
                s[0] = fr
            s[1] = fr + 1
            s[2].append(float(np.exp(sc[fr])))
        prev = tok
    out = [(s[0] * STEP, s[1] * STEP, float(np.mean(s[2]))) if s[0] is not None else None for s in spans]
    return out, float(sum(sc))


def best_variant(em, text: str, margin: float = 4.0):
    """Was part of this line repeated? Try the line as written, with its first word sung twice, its last word sung twice,
    and the whole line sung twice; keep a variant only if it fits the sound clearly better. -> (text, why)."""
    words = text.split()
    base = align_text(em, text)[1]
    cands = []
    if len(words) >= 2:
        cands.append((" ".join([words[0]] + words), "first word sung twice"))
        cands.append((" ".join(words + [words[-1]]), "last word sung twice"))
    cands.append((" ".join(words + words), "line sung twice"))
    best, why, score = text, "", base
    for t, w in cands:
        s = align_text(em, t)[1]
        # a longer text must beat the written one by a margin that grows with the letters it adds
        if s > score and s - base > margin + 0.6 * (len(t) - len(text)):
            best, why, score = t, w, s
    return best, why


def time_script(wav: Path, entries, before: float = 2.5, after: float = 0.5, test_repeats: bool = True):
    """Each phrase is placed inside its own window: from 2.5 s before where it was heard until just after where the NEXT
    phrase was heard (a phrase must finish before the next one starts; a wider window let a held last word swallow the
    start of the next line). Returns timed lines with word times.
    status: ok | review | weak, from how confidently the letters were found in the voice. These confidence cut-offs
    (0.35 / 0.2) are a first guess for this model and have not been calibrated."""
    voc = vocals(wav)
    audio, sr = read(voc)
    dur = len(audio) / sr
    entries = [dict(e) for e in entries if e["text"].strip()]
    timed = all(e.get("t") is not None for e in entries)
    out, prev_end = [], 0.0
    for i, e in enumerate(entries):
        if timed:
            nxt = entries[i + 1]["t"] if i + 1 < len(entries) else dur
            lo = max(0.0, e["t"] - before, prev_end - 0.1)
            hi = min(dur, max(nxt + after, lo + 2.0))
        else:                            # no heard times: share the clip evenly as a rough window
            lo = max(0.0, dur * i / len(entries) - 3.0)
            hi = min(dur, dur * (i + 1) / len(entries) + 3.0)
        em = emissions(audio[int(lo * sr):int(hi * sr)])
        text, flags = e["text"], []
        if test_repeats and e.get("kind", "lyric") == "lyric":
            t2, why = best_variant(em, text)
            if why:
                flags.append(f"repeat found by the timer: {why}")
                text = t2
        spans, _ = align_text(em, text)
        words = [{"w": w, "start": round(lo + s[0], 2), "end": round(lo + s[1], 2), "p": round(s[2], 2)}
                 for w, s in zip(text.split(), spans) if s is not None]
        if not words:
            out.append({"start": round(lo, 2), "end": round(lo, 2), "text": text, "conf": 0.0, "status": "weak", "kind": e.get("kind", "lyric"),
                        "line": e.get("line"), "heard_at": e.get("t"), "by": e.get("by", []), "flags": flags + ["could not be placed in the voice"], "words": []})
            continue
        conf = round(float(np.mean([w["p"] for w in words])), 2)
        status = "ok" if conf >= 0.35 else ("review" if conf >= 0.2 else "weak")
        if e.get("t") is not None and abs(words[0]["start"] - e["t"]) > 4.0:
            flags.append(f"placed {words[0]['start'] - e['t']:+.1f}s from where it was heard")
            status = "review" if status == "ok" else status
        out.append({"start": words[0]["start"], "end": words[-1]["end"], "text": text, "conf": conf, "status": status, "kind": e.get("kind", "lyric"),
                    "line": e.get("line"), "heard_at": e.get("t"), "by": e.get("by", []), "flags": flags, "words": words})
        prev_end = words[-1]["end"]
    return out
