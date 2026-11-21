"""Rough preview: burn the timed lyrics onto the clip so the owner can WATCH whether words land when they are sung.
This is a check, not the final design; the real captions are made by the editing step from lyrics.json.
Words appear one by one as they are sung; shaky lines are tinted so they are easy to spot.
"""
import subprocess
from pathlib import Path

SAND, DIM = "&H009FC8E9", "&H008B9FC7"     # brand sand #E9C89F and a dimmer tint (ASS colours are BGR)


def _ts(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def write_ass(lines, path: Path, font="Arial", show_weak=False, show_adlibs=True):
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: ok,{font},74,{SAND},&H000B0D1F,&H96000000,1,1,4,1,2,70,70,330,1\n"
            f"Style: shaky,{font},74,{DIM},&H000B0D1F,&H96000000,1,1,4,1,2,70,70,330,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    shown = [l for l in lines if (show_weak or l["status"] != "weak") and (show_adlibs or l["kind"] != "adlib")]
    ev = []
    for i, l in enumerate(shown):
        end = l["end"]
        if i + 1 < len(shown):
            end = min(max(end, l["start"] + 0.6), shown[i + 1]["start"])
        style = "ok" if l["status"] == "ok" else "shaky"
        ws = l.get("words") or []
        if len(ws) < 2:
            ev.append((l["start"], end, style, l["text"]))
            continue
        for k, w in enumerate(ws):                       # reveal word by word
            a = l["start"] if k == 0 else w["start"]
            b = ws[k + 1]["start"] if k + 1 < len(ws) else end
            if b - a > 0.02:
                ev.append((a, b, style, " ".join(x["w"] for x in ws[:k + 1])))
    body = "".join(f"Dialogue: 0,{_ts(a)},{_ts(b)},{st},,0,0,0,,{txt}\n" for a, b, st, txt in ev)
    path.write_text(head + body, encoding="utf-8-sig")


def burn(video: Path, lines, out_dir: Path, name="preview", font="Arial", **kw) -> Path:
    ass = out_dir / f"{name}.ass"
    write_ass(lines, ass, font=font, **kw)
    out = out_dir / f"{name}.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video), "-vf", f"subtitles={ass.name}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "copy", out.name], cwd=str(out_dir), capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-400:])
    return out
