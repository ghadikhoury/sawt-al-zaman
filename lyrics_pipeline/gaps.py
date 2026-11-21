"""Find singing that the script does not explain (missed repeats, ad-libs) and lines placed where nobody sings.

WHY THIS EXISTS
- Singers repeat words and lines and improvise; a listener that hears the whole clip at once misses some of these,
  and when asked to "write exactly what is sung" for a whole clip it can invent evenly spaced lines.
- With the voice isolated we can SEE where she is singing. Any stretch of singing with no caption line is a missed
  repeat or an ad-lib; we then ask Gemini about that short stretch only (a much easier, harder-to-fake question).
- The reverse check catches invented lines: a caption line over a stretch with no singing is flagged.
"""
import subprocess
from pathlib import Path

import numpy as np

import align_ctc

FRAME = 0.05


def singing(wav: Path):
    """-> (is_singing per 50 ms frame, loudness in dB per frame), from the isolated voice."""
    a, sr = align_ctc.read(align_ctc.vocals(wav))
    n = int(sr * FRAME)
    rms = np.array([np.sqrt(np.mean(a[i:i + n] ** 2) + 1e-10) for i in range(0, len(a) - n, n)])
    db = 20 * np.log10(rms + 1e-10)
    loud = np.percentile(db, 95)
    on = db > max(loud - 22.0, -48.0)                 # within ~22 dB of her loud passages
    k = 5                                              # close 250 ms dips (breaths, consonants), drop <200 ms blips
    sm = np.convolve(on.astype(float), np.ones(k) / k, mode="same") > 0.4
    return sm, db


def stretches(mask, min_len=0.0):
    out, s = [], None
    for i, v in enumerate(list(mask) + [False]):
        if v and s is None:
            s = i
        if not v and s is not None:
            if (i - s) * FRAME >= min_len:
                out.append((round(s * FRAME, 2), round(i * FRAME, 2)))
            s = None
    return out


def extend_held_notes(lines, mask):
    """A line's last word is often held long after its last letter starts. Stretch each line's end through the
    continuous singing that follows it (until a pause or the next line), so held notes are not mistaken for gaps
    and the caption stays up while she holds the note."""
    for i, l in enumerate(lines):
        limit = lines[i + 1]["start"] - 0.05 if i + 1 < len(lines) else len(mask) * FRAME
        j = int(l["end"] / FRAME)
        while j < len(mask) and j * FRAME < limit and mask[j]:
            j += 1
        new_end = round(min(limit, j * FRAME), 2)
        if new_end > l["end"]:
            l["end"] = new_end
            if l["words"]:
                l["words"][-1]["end"] = new_end
    return lines


def unexplained(lines, mask, min_len=1.3, hold=2.5):
    """Stretches of singing that no WORD accounts for. Call this BEFORE extend_held_notes.
    A word is allowed to be held for up to `hold` seconds after the timer's end for it; singing that goes on longer
    than that with no word (between two words of a line, or after a line) is either a very long held note or a
    repeat / ad-lib the script is missing, so it is worth a second listen."""
    cov = np.zeros(len(mask), dtype=bool)
    for l in lines:
        for w in l["words"] or [{"start": l["start"], "end": l["end"]}]:
            cov[int(max(0, w["start"] - 0.3) / FRAME): int((w["end"] + hold) / FRAME) + 1] = True
    return stretches(mask & ~cov, min_len)


def long_words(lines, min_dur=3.0):
    """Words the timer stretched over 3 s or more. The timer absorbs a repeated word into one long word (it has no
    second copy of the word to place), so a very long word is either a genuinely held note or a missed repeat.
    These stretches are worth a second listen too."""
    out = []
    for l in lines:
        for w in l["words"]:
            if w["end"] - w["start"] >= min_dur:
                out.append((round(w["start"], 2), round(w["end"], 2)))
    return out


def already_have(entry, lines, tol=1.5):
    """True if a phrase heard on a second listen is just a word/line we already placed at about that time."""
    from arabic_text import similarity
    for l in lines:
        if abs(l["start"] - entry["t"]) < tol and similarity(l["text"], entry["text"]) >= 0.6:
            return True
        ws = l["words"]
        for i in range(len(ws)):
            for j in range(i + 1, len(ws) + 1):
                if abs(ws[i]["start"] - entry["t"]) < tol and similarity(" ".join(x["w"] for x in ws[i:j]), entry["text"]) >= 0.7:
                    return True
    return False


def flag_silent_lines(lines, mask):
    """Mark lines that sit where almost nobody is singing: probably not sung in this clip."""
    for l in lines:
        a, b = int(l["start"] / FRAME), max(int(l["end"] / FRAME), int(l["start"] / FRAME) + 1)
        seg = mask[a:b]
        if len(seg) and seg.mean() < 0.25:
            l["flags"].append("little or no singing at this point")
            l["status"] = "weak"
    return lines


def cut(wav: Path, start: float, end: float, out: Path) -> Path:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0, start):.2f}", "-t", f"{end - start:.2f}", "-i", str(wav),
                    "-ac", "1", "-ar", "16000", str(out)], capture_output=True)
    return out


def relisten(wav: Path, gap, lines, lyric_lines, tmp: Path):
    """Ask Gemini what is sung in one unexplained stretch (with 1 s of context each side).
    -> script entries with clip times, or [] if it hears nothing."""
    import listen
    import script as sc
    a, b = max(0.0, gap[0] - 1.0), gap[1] + 1.0
    piece = cut(wav, a, b, tmp)
    # the lyric lines most likely sung here: around the neighbouring lines' place in the song
    near = [l["line"] for l in lines if l.get("line") is not None and (abs(l["start"] - gap[0]) < 25 or abs(l["end"] - gap[1]) < 25)]
    lo, hi = (max(0, min(near) - 3), min(len(lyric_lines), max(near) + 4)) if near else (0, min(len(lyric_lines), 12))
    res = listen.listen_slice(piece, lyric_lines[lo:hi])
    if not res.get("ok"):
        return []
    heard = [{"t": round(a + (e["t"] or 0.0), 2), "text": e["text"]} for e in res["sung"] if e["t"] is None or 0.5 <= e["t"] <= (b - a) - 0.3]
    return [e for e in sc.snap(heard, lyric_lines, "gap") if gap[0] - 0.8 <= e["t"] <= gap[1] + 0.3]
