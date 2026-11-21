"""Listening to the audio (Gemini, audio only).

first_listen()          no lyrics: writes the words it hears with rough times. Finds the song AND is the backbone of the
                        sung script (on the reels tried so far it was accurate, repeats of whole lines included).
listen_slice()          one short stretch (a few seconds) with the nearby lyric lines: "what is sung here?". Used for
                        stretches of singing the script does not explain (missed repeats, ad-libs). See gaps.py.
second_listen_gemini()  the whole clip again with the lyrics in hand. OPTIONAL and not trusted by default: on one reel it
                        doubled every line and invented evenly spaced times. looks_invented() rejects that pattern.
An Arabic fine-tuned Whisper was also tried as a second listener and was clearly worse (invented words); it was removed.

The Gemini key is read from the Windows user env var GEMINI_API_KEY; it is never printed or saved.
Free-tier limits are respected: on a daily-quota error the model is dropped for this run and the next one is tried.
"""
import base64
import json
import os
import re
import subprocess
import time
from pathlib import Path

import requests

from arabic_text import is_junk, phonetic, similarity

# strongest first; the free key allows only ~20 calls/day on the first two, flash-lite is the fallback
GEMINI_MODELS = ["gemini-3.5-flash", "gemini-3-flash-preview", "gemini-3.5-flash-lite"]
_dead = set()
_last = 0.0

FIRST_PROMPT = (
    "You are listening to a short clip of an old Arabic song (classical / tarab / folk). Audio only.\n"
    "Write down the Arabic words that are SUNG, line by line, in order, exactly as you hear them (Arabic script, no vowel marks). "
    "For each line give the time it starts, in seconds from the start of the clip. Write a repeated line every time it is sung. "
    "Do not complete verses from memory that are not in this audio. Do not guess the song or the singer. "
    "Ignore instruments, applause and speech. If a part is unintelligible write [unclear].\n"
    'Also say whether there is any singing at all. Return ONLY JSON: {"has_singing": true, "lines": [{"t": 12.5, "text": "..."}]}'
)

SECOND_PROMPT = (
    "You are listening to a short clip of an old Arabic song. Below are the song's official lyrics, numbered.\n"
    "The clip is only a PART of the song, and the singer does not follow the printed text one-to-one: lines, half-lines or single "
    "words are repeated, earlier lines come back, and there are ad-libs (آه، يا ليل، يا عين ...).\n"
    "Write down EXACTLY what is sung in this clip, in the order sung:\n"
    "- one entry per sung phrase, with the time it starts in seconds;\n"
    "- write every repetition as its own entry; if only part of a line is sung, write only that part;\n"
    "- use the spelling of the official lyrics for words that come from them, and give that line's number;\n"
    "- for sung words that are NOT in the lyrics (ad-libs, improvisation) write what you hear with line = null;\n"
    "- do NOT include any lyric line that is not actually sung in this clip. Listen, do not copy.\n"
    'Return ONLY JSON: {"sung": [{"t": 3.2, "text": "...", "line": 7}]}\n\nOFFICIAL LYRICS:\n'
)


def gemini_key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User')"],
                           capture_output=True, text=True)
        k = r.stdout.strip()
    return k


def wav16k(video: Path, out: Path) -> Path | None:
    if not (out.exists() and out.stat().st_size > 1000):
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video), "-vn", "-t", "300", "-ac", "1", "-ar", "16000", str(out)],
                       capture_output=True)
    return out if out.exists() and out.stat().st_size > 1000 else None


def _gemini(wav: Path, prompt: str, models=None) -> tuple[dict, str]:
    """-> (parsed JSON object or {}, model used or error text). Tries the models in order."""
    global _last
    key = gemini_key()
    if not key:
        return {}, "GEMINI_API_KEY not set"
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(wav.read_bytes()).decode()}},
                                    {"text": prompt}]}], "generationConfig": {"temperature": 0.2}}
    err = "no model available"
    for model in models or GEMINI_MODELS:
        if model in _dead:
            continue
        for attempt in range(2):
            wait = 6.0 - (time.time() - _last)
            if wait > 0:
                time.sleep(wait)
            _last = time.time()
            try:
                r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                                  params={"key": key}, json=body, timeout=150)
            except Exception as e:
                err = f"{model}: {type(e).__name__}"
                continue
            if r.status_code == 200:
                parts = ((r.json().get("candidates") or [{}])[0].get("content") or {}).get("parts", [])
                m = re.search(r"\{.*\}", "".join(p.get("text", "") for p in parts), re.S)
                try:
                    o = json.loads(m.group(0)) if m else {}
                except Exception:
                    o = {}
                if o:
                    return o, model
                err = f"{model}: unreadable answer"
                continue
            err = f"{model}: HTTP {r.status_code}"
            if r.status_code == 503 and attempt == 0:
                time.sleep(15)
                continue
            if r.status_code in (429, 400, 404):
                _dead.add(model)          # quota or unavailable: move on, never work around it
            break
    return {}, err


def _entries(raw, text_key="text"):
    out = []
    for x in raw or []:
        if isinstance(x, str):
            x = {"text": x}
        if not isinstance(x, dict) or not isinstance(x.get(text_key), str):
            continue
        txt = re.sub(r"\s+", " ", x[text_key]).strip()
        if "[unclear]" in txt.lower() or is_junk(txt):
            continue
        try:
            t = float(x.get("t"))
        except Exception:
            t = None
        e = {"t": t, "text": txt}
        if "line" in x:
            e["line"] = x["line"] if isinstance(x["line"], int) else None
        out.append(e)
    return out


def first_listen(wav: Path, models=None) -> dict:
    o, model = _gemini(wav, FIRST_PROMPT, models)
    if not o:
        return {"ok": False, "error": model, "lines": []}
    return {"ok": True, "model": model, "has_singing": o.get("has_singing"), "lines": _entries(o.get("lines"))}


def second_listen_gemini(wav: Path, lyric_lines: list[str], models=None) -> dict:
    numbered = "\n".join(f"{i + 1}. {l}" for i, l in enumerate(lyric_lines[:220]))
    o, model = _gemini(wav, SECOND_PROMPT + numbered, models)
    if not o:
        return {"ok": False, "error": model, "sung": []}
    sung = _entries(o.get("sung"))
    for e in sung:                       # 1-based line numbers -> 0-based index, validated
        n = e.get("line")
        e["line"] = n - 1 if isinstance(n, int) and 1 <= n <= len(lyric_lines) else None
    return {"ok": True, "model": model, "sung": sung}


SLICE_PROMPT = (
    "This is a FEW SECONDS cut from an old Arabic song. Write exactly the Arabic words that are SUNG in it, in order, each with "
    "the time it starts in seconds from the start of this cut. If a word or phrase is sung twice, write it twice. Sung ad-libs "
    "(آه، يا ليل، يا عين ...) count; instruments, applause and speech do not. Write only what you hear in this cut; if nothing "
    'is sung, return an empty list. Return ONLY JSON: {"sung": [{"t": 1.2, "text": "..."}]}'
)


def listen_slice(piece: Path, nearby_lines=None, models=None) -> dict:
    """What is sung in this short cut? No lyrics are given on purpose: when nearby lyric lines were included, the model
    recited them instead of listening. Spelling is fixed afterwards by script.snap()."""
    o, model = _gemini(piece, SLICE_PROMPT, models)
    if not o and model.endswith("unreadable answer"):
        return {"ok": True, "model": model, "sung": []}
    if not o:
        return {"ok": False, "error": model, "sung": []}
    return {"ok": True, "model": model, "sung": _entries(o.get("sung"))}


def looks_invented(entries) -> str:
    """Why a whole-clip second listen should not be trusted, or '' if it looks fine.
    Seen in practice: every line doubled, with start times on an even grid (2.2, 5.2, 8.2, 12.2 ...)."""
    ts = [e["t"] for e in entries if e.get("t") is not None]
    if len(ts) < 6:
        return ""
    gaps = [b - a for a, b in zip(ts, ts[1:])]
    frac = [round(t % 1, 2) for t in ts]
    if max(frac.count(f) for f in set(frac)) >= 0.75 * len(ts):
        return "start times all share the same decimals: an invented grid"
    mean = sum(gaps) / len(gaps)
    if mean > 0 and (sum((g - mean) ** 2 for g in gaps) / len(gaps)) ** 0.5 < 0.12 * mean:
        return "phrases are evenly spaced: an invented grid"
    return ""
