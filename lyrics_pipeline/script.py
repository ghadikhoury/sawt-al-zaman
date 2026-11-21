"""The SUNG SCRIPT: exactly what is sung in this clip, in order, repeats and ad-libs included.

Printed lyrics are only a reference for which words exist and how they are spelled. Singers repeat lines, half-lines
and words, return to earlier lines and improvise, so the script is built from what was HEARD and only spelled with
the help of the lyrics.

An entry: {"t": rough start sec, "text": words to show, "line": index into the lyrics or None, "kind": "lyric"|"adlib",
           "by": ["gemini2", "whisper", ...]}
"""
from arabic_text import normalize, phonetic, similarity
from rapidfuzz import fuzz

MATCH = 0.58


def _best_line(text, lyric_lines, prev=None):
    """Best lyric line for a heard phrase (prefers the line that continues the song when it is a tie)."""
    hk = phonetic(text)
    best, bi = 0.0, None
    for i, l in enumerate(lyric_lines):
        s = similarity(text, l)
        if prev is not None and i in (prev, prev + 1):
            s += 0.03
        if s > best:
            best, bi = s, i
    return bi, min(best, 1.0)


def _part_of_line(heard, line):
    """If only part of a lyric line was sung, return that part (official spelling); else the whole line."""
    hw, lw = normalize(heard).split(), line.split()
    if len(hw) >= 0.7 * len(lw) or len(lw) < 4:
        return line
    best, span = 0.0, (0, len(lw))
    for n in range(max(1, len(hw) - 1), min(len(lw), len(hw) + 2) + 1):
        for a in range(0, len(lw) - n + 1):
            s = fuzz.ratio(phonetic(" ".join(lw[a:a + n])), phonetic(heard))
            if s > best:
                best, span = s, (a, a + n)
    return " ".join(lw[span[0]:span[1]]) if best >= 70 else line


def snap(heard, lyric_lines, by):
    """Heard phrases -> script entries spelled from the lyrics. Phrases that match no lyric line stay as heard (ad-lib)."""
    out, prev = [], None
    for h in heard:
        txt = h["text"].strip()
        if len(normalize(txt)) < 2:
            continue
        li = h.get("line")
        if li is not None and similarity(txt, lyric_lines[li]) < 0.5:
            li = None                                   # the listener's own line number does not hold up
        if li is None:
            li, s = _best_line(txt, lyric_lines, prev)
            if s < MATCH:
                li = None
        if li is None:
            out.append({"t": h.get("t"), "text": txt, "line": None, "kind": "adlib", "by": [by]})
        else:
            out.append({"t": h.get("t"), "text": _part_of_line(txt, lyric_lines[li]), "line": li, "kind": "lyric", "by": [by]})
            prev = li
    return out


def merge(primary, others):
    """primary: the script to trust for order (Gemini's second listen when available).
    others: {name: script}. Only marks which entries another listener also heard (entry["by"]); it never adds phrases:
    on test reels the extra phrases from weaker listeners were mostly wrong."""
    out = [dict(e) for e in primary]
    timed = all(e["t"] is not None for e in out) and out
    for name, sc in others.items():
        for o in sc:
            if o["t"] is None:
                continue
            near = [e for e in out if e["t"] is not None and abs(e["t"] - o["t"]) <= 5.0 and similarity(e["text"], o["text"]) >= 0.6]
            if near:
                for e in near[:1]:
                    if name not in e["by"]:
                        e["by"].append(name)
    if timed:
        out.sort(key=lambda e: e["t"])
    return out


def insert(entries, new):
    """Add phrases found later (e.g. by the gap check) into the script in time order, skipping near-duplicates."""
    out = [dict(e) for e in entries]
    for n in new:
        if any(e["t"] is not None and abs(e["t"] - n["t"]) < 1.2 and similarity(e["text"], n["text"]) >= 0.6 for e in out):
            continue
        out.append(dict(n))
    return sorted(out, key=lambda e: (e["t"] is None, e["t"] or 0))


def describe(entries, lyric_lines):
    """Short human-readable view for the agent to review."""
    rows = []
    for i, e in enumerate(entries):
        t = f"{e['t']:6.1f}" if e["t"] is not None else "   ?  "
        tag = f"L{e['line'] + 1}" if e["line"] is not None else "ad-lib"
        rows.append(f"{i:2d} {t}  {tag:7s} {'+'.join(e['by']):16s} {e['text']}")
    return "\n".join(rows)
