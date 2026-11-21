"""Timing: Whisper (large-v3, forced alignment via stable-ts) is given the sung script and finds WHEN each line and
each word is sung. It does not decide what the words are.

Output per line: start, end, text, conf (0..1), status, words [{w, start, end, p}].
status: ok (trusted) | review (shaky) | weak (the audio does not clearly support this line: check before showing).
"""
import contextlib
import glob
import io
import os
import warnings

GOOD, KEEP = 0.55, 0.35
_model = None


def _load():
    global _model
    if _model is None:
        import nvidia
        for p in glob.glob(os.path.join(list(nvidia.__path__)[0], "*", "bin")):
            os.add_dll_directory(p)
            os.environ["PATH"] = p + os.pathsep + os.environ["PATH"]
        import stable_whisper
        _model = stable_whisper.load_faster_whisper("large-v3", device="cuda", compute_type="float16")
    return _model


def _align(audio, texts):
    with warnings.catch_warnings(), contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
        warnings.simplefilter("ignore")
        return _load().align(audio, "\n".join(texts), language="ar", original_split=True).segments


def _line(e, seg, offset=0.0):
    words = [{"w": w.word.strip(), "start": round(float(w.start) + offset, 2), "end": round(float(w.end) + offset, 2),
              "p": round(float(w.probability or 0.0), 2)} for w in seg.words if w.word.strip()]
    conf = round(sum(w["p"] for w in words) / len(words), 2) if words else 0.0
    start, end = round(float(seg.start) + offset, 2), round(float(seg.end) + offset, 2)
    status = "ok" if conf >= GOOD else ("review" if conf >= KEEP else "weak")
    flags = []
    if e.get("t") is not None and abs(start - e["t"]) > 4.0:
        flags.append(f"timer put it {start - e['t']:+.1f}s from where it was heard")
        status = "review" if status == "ok" else status
    if end - start < 0.25 * min(len(words), 4):
        flags.append("too short to be sung")
        status = "weak"
    return {"start": start, "end": end, "text": e["text"], "conf": conf, "status": status, "kind": e.get("kind", "lyric"),
            "line": e.get("line"), "heard_at": e.get("t"), "by": e.get("by", []), "flags": flags, "words": words}


def time_script(wav, entries, before=2.5, after=1.5):
    """If every phrase has a rough heard time, each phrase is aligned inside its own window
    [heard time - 2.5 s, next phrase's heard time + 1.5 s]: long instrumental gaps can then not drag the timing.
    Without heard times the whole script is aligned across the whole clip in one pass."""
    entries = [e for e in entries if e["text"].strip()]
    if not entries:
        return []
    if any(e.get("t") is None for e in entries):
        return [_line(e, seg) for e, seg in zip(entries, _align(str(wav), [e["text"] for e in entries]))]
    import wave
    import numpy as np
    with wave.open(str(wav)) as w:
        sr = w.getframerate()
        audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    dur = len(audio) / sr
    out, prev_end = [], 0.0
    for i, e in enumerate(entries):
        nxt = entries[i + 1]["t"] if i + 1 < len(entries) else dur
        lo = max(0.0, e["t"] - before, prev_end - 0.15)
        hi = min(dur, max(nxt + after, lo + 2.0))
        segs = _align(audio[int(lo * sr):int(hi * sr)], [e["text"]])
        if not segs:
            continue
        l = _line(e, segs[0], offset=lo)
        out.append(l)
        if l["end"] > l["start"]:
            prev_end = l["end"]
    return out
