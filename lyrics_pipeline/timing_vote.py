"""Word start times by vote: the middle value of several independent estimates.

WHY THIS EXISTS
On sung Arabic no single timer is reliable, and their errors go in different directions:
- the letter-level (CTC) timer marks a letter where it "spikes", which on a long held note can be seconds after the
  word really began (on the first reel it put a word at 15.5 s that three other sources put at 12-13 s);
- Whisper forced alignment (stable-ts) also tends to start a held word late;
- free Whisper transcription of the isolated voice gives back-to-back word boundaries, which suits legato singing
  but sometimes snaps to the start of the audio;
- Gemini listening to one line's few seconds gives rough but independent times.
Taking the median of what is available cancels one source's lateness. Starts at the very edge of the audio
(< 0.05 s) are treated as artefacts and ignored.
"""
import json
import os
from pathlib import Path
from statistics import median

from arabic_text import similarity

MIN_GAP = 0.15


def _free_whisper(voc: Path, cache: Path):
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    import glob
    import nvidia
    for p in glob.glob(os.path.join(list(nvidia.__path__)[0], "*", "bin")):
        os.add_dll_directory(p)
        os.environ["PATH"] = p + os.pathsep + os.environ["PATH"]
    from faster_whisper import WhisperModel
    m = WhisperModel("large-v3", device="cuda", compute_type="float16")
    segs, _ = m.transcribe(str(voc), language="ar", word_timestamps=True, condition_on_previous_text=False, beam_size=5)
    words = [{"w": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for s in segs for w in (s.words or [])]
    del m
    cache.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    return words


def _gemini_slices(wav: Path, lines, cache: Path):
    """Gemini hears each line's stretch on its own (no lyrics given). Cached; costs one call per line."""
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    import gaps
    import listen
    out = []
    for i, l in enumerate(lines):
        a, b = max(0.0, l["start"] - 1.0), l["end"] + 0.6
        r = listen.listen_slice(gaps.cut(wav, a, b, cache.parent / "_slice.wav"))
        out.append([{"w": e["text"], "start": round(a + (e["t"] or 0.0), 2)} for e in r.get("sung", []) if e.get("t") is not None])
    (cache.parent / "_slice.wav").unlink(missing_ok=True)
    cache.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def _match(script_words, cand, lo, hi):
    """Map each script word to a candidate word (in order, similar spelling, inside [lo, hi]). -> list of start or None."""
    cand = [c for c in cand if lo <= c["start"] <= hi]
    out, j = [], 0
    for w in script_words:
        best, bk = 0.0, None
        for k in range(j, min(len(cand), j + 4)):
            s = similarity(w, cand[k]["w"])
            if s > best:
                best, bk = s, k
        if bk is not None and best >= 0.5:
            out.append(cand[bk]["start"])
            j = bk + 1
        else:
            out.append(None)
    return out


def vote(wav: Path, voc: Path, entries, ctc_lines, project: Path, use_gemini=True):
    """ctc_lines: output of align_ctc.time_script for the same entries. Returns the same lines with voted word starts.
    Each word gets "votes": the estimates it was given, so the agent can see where the sources disagreed."""
    import timing
    st_lines = timing.time_script(wav, entries)                       # Whisper forced alignment, per window
    free = _free_whisper(voc, project / "whisper_free.json")
    gem = _gemini_slices(wav, ctc_lines, project / "gemini_slices.json") if use_gemini else []
    out = []
    for i, l in enumerate(ctc_lines):
        words = l["words"]
        if not words:
            out.append(l)
            continue
        toks = [w["w"] for w in words]
        lo = min(l["start"], st_lines[i]["start"] if i < len(st_lines) else l["start"]) - 2.0
        hi = l["end"] + 1.0
        sources = {"ctc": [w["start"] for w in words]}
        if i < len(st_lines) and len(st_lines[i]["words"]) == len(words):
            sources["stable_ts"] = [w["start"] for w in st_lines[i]["words"]]
        sources["whisper_free"] = _match(toks, free, lo, hi)
        if i < len(gem):
            sources["gemini"] = _match(toks, gem[i], lo, hi)
        new, prev = [], -1.0
        for k, w in enumerate(words):
            vals = {n: v[k] for n, v in sources.items() if v[k] is not None and v[k] >= 0.05}
            s = median(vals.values()) if vals else w["start"]
            s = max(s, prev + MIN_GAP)
            new.append({**w, "start": round(s, 2), "votes": vals})
            prev = s
        for k in range(len(new) - 1):                                 # a word lasts until the next one starts
            new[k]["end"] = round(max(new[k]["start"] + 0.1, new[k + 1]["start"] - 0.02), 2)
        new[-1]["end"] = round(max(new[-1]["end"], new[-1]["start"] + 0.3), 2)
        spread = max((max(w["votes"].values()) - min(w["votes"].values()) for w in new if len(w["votes"]) >= 2), default=0.0)
        flags = list(l["flags"])
        if spread > 2.0:
            flags.append(f"timing sources disagree by up to {spread:.1f}s on a word: check by ear")
        out.append({**l, "start": new[0]["start"], "end": new[-1]["end"], "words": new, "flags": flags})
    # lines must not overlap: a line ends before the next one starts
    for i in range(len(out) - 1):
        if out[i]["words"] and out[i + 1]["words"] and out[i]["end"] > out[i + 1]["start"] - 0.05:
            out[i]["end"] = round(out[i + 1]["start"] - 0.05, 2)
            out[i]["words"][-1]["end"] = max(out[i]["words"][-1]["start"] + 0.1, out[i]["end"])
    return out
