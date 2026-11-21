"""SCORING ONLY - never used by the pipeline. Compares a clip's lyrics.json with the lyrics burned into the original reel.

eval/onscreen/<reel id>.json holds the on-screen lyrics of already-posted reels, read once by OCR (not included in the
public repository because it contains song lyrics; make your own from reels you have the rights to), so any of those
reels can be run through the pipeline and scored without anyone watching it.
eval/split.json lists the 218 downloaded reels as tune / holdout / final (final = 40 reels never tuned on).

  python eval/score.py                 scores every project in "Lyrics Projects" whose clip name ends with a known reel id
Reports, per reel and in total:
  text      share of output lines confirmed by the on-screen lyrics
  timing    share of confirmed lines that start within 1.5 s of when the line appears on screen
  complete  share of on-screen lyric lines that are present in the output
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from arabic_text import normalize, similarity  # noqa: E402
from rapidfuzz import fuzz  # noqa: E402

PROJECTS = Path(os.environ.get("LYRICS_PROJECTS", HERE.parent.parent / "projects"))


def onscreen(rid):
    """On-screen lyric lines with each interval they were visible (text up for more than 12 s is a banner, not a lyric)."""
    p = HERE / "onscreen" / f"{rid}.json"
    if not p.exists():
        return None
    clusters = []
    for fr in json.loads(p.read_text(encoding="utf-8")):
        for ln in fr.get("lines", []):
            if len(normalize(ln).split()) < 2 or not re.search(r"[؀-ۿ]{2,}", ln):
                continue
            for c in clusters:
                if similarity(c["text"], ln) >= 0.82:
                    c["times"].append(float(fr["t"]))
                    break
            else:
                clusters.append({"text": ln, "times": [float(fr["t"])]})
    wins = []
    for c in clusters:
        ts = sorted(c["times"])
        st = prev = ts[0]
        for t in ts[1:] + [None]:
            if t is None or t - prev > 1.6:
                if 0.9 <= prev + 0.5 - st <= 12.0:
                    wins.append({"text": c["text"], "start": st, "end": prev + 0.5})
                st = t
            prev = t if t is not None else prev
    return sorted(wins, key=lambda w: w["start"])


def same(a, b):
    if similarity(a, b) >= 0.70:
        return True
    ta = [w for w in normalize(a).split() if len(w) >= 3]
    tb = [w for w in normalize(b).split() if len(w) >= 3]
    return len(ta) >= 2 and sum(any(fuzz.ratio(x, y) >= 78 for y in tb) for x in ta) >= 0.6 * len(ta)


def score(rid, lines):
    wins = onscreen(rid)
    if not wins or len({w["text"] for w in wins}) < 3:
        return None
    lines = [l for l in lines if l.get("status") != "weak"]
    texts = [w["text"] for w in wins]
    pairs = texts + [texts[i] + " " + texts[i + 1] for i in range(len(texts) - 1)]
    judged = ok = timed = 0
    for l in lines:
        near = [w for w in wins if l["end"] >= w["start"] - 2 and l["start"] <= w["end"] + 2]
        hit = any(same(l["text"], p) for p in pairs)
        if not near and not hit:
            continue                  # sung while nothing was on screen: cannot be judged
        judged += 1
        if hit:
            ok += 1
            timed += any(same(l["text"], w["text"]) and abs(l["start"] - w["start"]) <= 1.5 for w in wins)
    uniq = list(dict.fromkeys(texts))
    cov = sum(any(same(t, l["text"]) or same(l["text"], t) for l in lines) for t in uniq)
    return {"judged": judged, "text_ok": ok, "timed": timed, "onscreen_lines": len(uniq), "covered": cov}


if __name__ == "__main__":
    tot = {"judged": 0, "text_ok": 0, "timed": 0, "onscreen_lines": 0, "covered": 0}
    for d in sorted(PROJECTS.iterdir()) if PROJECTS.exists() else []:
        lp = d / "lyrics.json"
        rid = next((f.stem for f in (HERE / "onscreen").glob("*.json") if d.name.endswith(f.stem)), None)
        if not lp.exists() or not rid:
            continue
        r = score(rid, json.loads(lp.read_text(encoding="utf-8"))["lines"])
        if not r:
            continue
        for k in tot:
            tot[k] += r[k]
        print(f"{d.name[:40]:40s} text {r['text_ok']}/{r['judged']}  timing {r['timed']}/{r['text_ok']}  complete {r['covered']}/{r['onscreen_lines']}")
    if tot["judged"]:
        print(f"TOTAL  text {100*tot['text_ok']/tot['judged']:.0f}%  timing {100*tot['timed']/max(1,tot['text_ok']):.0f}%  complete {100*tot['covered']/max(1,tot['onscreen_lines']):.0f}%")
