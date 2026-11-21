"""Lyrics pipeline command line. See README.md for the whole procedure and the reasons behind each step.

  python lyrics.py go      <video>     everything below in order; stops and tells the agent what to do if the song is not settled
  python lyrics.py hear    <video>     first listen (Gemini, audio only) -> heard.json
  python lyrics.py find    <video>     search the local catalogue with what was heard -> candidates.json
  python lyrics.py song    <video> --catalog N
  python lyrics.py song    <video> --lyrics FILE --title "..." --artist "..." [--url URL]     (lyrics the agent found / the owner gave)
  python lyrics.py script  <video> [--second-listen]      the sung script -> script.json   (REVIEW IT, edit by hand if needed)
  python lyrics.py time    <video> [--timer vote|ctc|whisper]  when each line and word is sung -> lyrics.json (vote = default)
  python lyrics.py refine  <video>     SUGGEST missed repeats / ad-libs: re-listens to unexplained singing and over-long words -> gaps.json (changes nothing)
  python lyrics.py preview <video>     rough burned-in preview -> preview.mp4

Everything for one clip lives in  projects/<clip name>/ (or the folder named in LYRICS_PROJECTS)  and can be edited by hand and re-run from any step.
"""
import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent
PROJECTS = Path(os.environ.get("LYRICS_PROJECTS", ROOT / "projects"))  # one folder per clip


def proj(video: Path) -> Path:
    d = PROJECTS / video.stem
    d.mkdir(parents=True, exist_ok=True)
    return d


def load(p: Path, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def save(p: Path, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def wav_of(video: Path) -> Path:
    import listen
    w = listen.wav16k(video, proj(video) / "audio16k.wav")
    if w is None:
        sys.exit("This clip has no audio stream.")
    return w


def cmd_hear(video, a):
    import listen
    d = proj(video)
    h = load(d / "heard.json")
    if not h or not h.get("ok") or a.again:
        h = listen.first_listen(wav_of(video))
        save(d / "heard.json", h)
    if not h.get("ok"):
        sys.exit(f"Gemini could not listen: {h.get('error')}")
    print(f"heard by {h['model']} | singing: {h.get('has_singing')}")
    for e in h["lines"]:
        print(f"  {e['t'] if e['t'] is not None else '?':>6}  {e['text']}")
    if not h["lines"]:
        print("  (no sung words heard: instrumental or speech)")
    return h


def cmd_find(video, a):
    from catalog import Catalog
    d = proj(video)
    h = load(d / "heard.json") or cmd_hear(video, a)
    res = Catalog().search([e["text"] for e in h["lines"]], top_k=5)
    save(d / "candidates.json", res)
    if not res:
        print("catalogue: nothing matches what was heard")
    for i, r in enumerate(res):
        print(f"  [{i}] score {r['score']:5.2f}  matched {r['heard_lines_matched']}/{r['heard_lines']} heard lines  |  {r['title']} — {r['artist']}")
    return res


def cmd_song(video, a):
    from arabic_text import lyric_lines
    from catalog import Catalog
    d = proj(video)
    cat = Catalog()
    if a.catalog is not None:
        c = load(d / "candidates.json")[a.catalog]
        s = cat.songs[c["index"]]
        song = {"title": s["title"], "artist": s["artist"], "url": s["url"], "lines": s["lines"], "chosen_from": "catalogue"}
    else:
        if not a.lyrics or not a.title:
            sys.exit("give --catalog N, or --lyrics FILE with --title (and --artist)")
        lines = lyric_lines(Path(a.lyrics).read_text(encoding="utf-8"))
        if len(lines) < 2:
            sys.exit("that lyrics file has fewer than 2 usable Arabic lines")
        song = {"title": a.title, "artist": a.artist or "", "url": a.url or "", "lines": lines, "chosen_from": "given"}
        cat.add(a.title, a.artist or "", lines, a.url or "")
    save(d / "song.json", song)
    print(f"song set: {song['title']} — {song['artist']} ({len(song['lines'])} lyric lines)")
    return song


def cmd_script(video, a):
    """Build the sung script. Backbone = the first listen, spelled from the lyrics. The whole-clip second listen is optional
    (--second-listen) and is only used when it does not look invented."""
    import listen
    import script as sc
    d = proj(video)
    song = load(d / "song.json") or sys.exit("no song chosen yet: run `song` first")
    heard = load(d / "heard.json", {"lines": []})
    lines = song["lines"]
    script = sc.snap(heard.get("lines", []), lines, "first")
    if a.second_listen:
        g = load(d / "listen2_gemini.json")
        if not g or not g.get("ok") or a.again:
            g = listen.second_listen_gemini(wav_of(video), lines)
            save(d / "listen2_gemini.json", g)
        if g.get("ok"):
            bad = listen.looks_invented(g["sung"])
            g2 = sc.snap(g["sung"], lines, "gemini2")
            save(d / "script_gemini2.json", g2)
            if bad:
                print(f"second listen NOT used: {bad}")
            else:
                script = sc.merge(g2, {"first": script})
    save(d / "script.json", script)
    print(f"--- sung script ({len(script)} phrases). Review it; edit script.json to correct it:")
    print(sc.describe(script, lines))
    return script


def cmd_time(video, a, script_file=None, name=None):
    d = proj(video)
    sf = Path(script_file or a.script or d / "script.json")
    if not sf.is_absolute():
        sf = d / sf
    entries = load(sf) or sys.exit(f"no script at {sf}: run `script` first")
    song = load(d / "song.json", {})
    wav = wav_of(video)
    if a.timer == "whisper":
        import timing
        lines = timing.time_script(wav, entries)
    else:
        import align_ctc
        import gaps
        lines = align_ctc.time_script(wav, entries, test_repeats=not a.no_repeat_test)
        if a.timer == "vote":
            import timing_vote
            lines = timing_vote.vote(wav, align_ctc.vocals(wav), entries, lines, d, use_gemini=not a.no_gemini_vote)
        mask, _ = gaps.singing(wav)
        holes = gaps.unexplained(lines, mask)            # measured before lines are stretched over held notes
        lines = gaps.flag_silent_lines(gaps.extend_held_notes(lines, mask), mask)
    out = {"video": str(video), "title": song.get("title", ""), "artist": song.get("artist", ""), "source": song.get("url", ""),
           "script": sf.name, "timer": a.timer, "lines": lines}
    if a.timer != "whisper":
        out["unexplained_singing"] = holes
        if holes:
            print("singing that no word accounts for (run `refine`): " + ", ".join(f"{x:.1f}-{y:.1f}s" for x, y in holes))
    name = name or a.name
    op = d / (f"lyrics_{name}.json" if name else "lyrics.json")
    save(op, out)
    n = {s: sum(1 for l in lines if l["status"] == s) for s in ("ok", "review", "weak")}
    print(f"{op.name}: {len(lines)} lines | ok {n['ok']}, review {n['review']}, weak {n['weak']}")
    for l in lines:
        fl = ("  ! " + "; ".join(l["flags"])) if l["flags"] else ""
        print(f"  {l['start']:6.2f}-{l['end']:6.2f}  {l['conf']:.2f} {l['status']:6s} {l['text']}{fl}")
    return out


def cmd_refine(video, a):
    """Suggest what the script may be missing. Takes the stretches of singing no word accounts for, plus words the timer
    stretched over 3 s (a held note or a missed repeat), and asks Gemini what is sung in just those few seconds.
    It only REPORTS (and saves gaps.json): on the first real reel, applying its answers automatically added 15 mostly
    wrong phrases. The agent decides what is real, edits script.json, and runs `time` again."""
    import gaps
    d = proj(video)
    song = load(d / "song.json") or sys.exit("no song chosen yet")
    data = load(d / "lyrics.json") or cmd_time(video, a)
    wav = wav_of(video)
    holes = sorted(set([tuple(h) for h in data.get("unexplained_singing", [])] + gaps.long_words(data["lines"])))
    if not holes:
        print("refine: no singing without a line and no suspiciously long words")
        return []
    report = []
    for g in holes[:8]:
        heard = gaps.relisten(wav, g, data["lines"], song["lines"], d / "_gap.wav")
        new = [e for e in heard if not gaps.already_have(e, data["lines"])]
        report.append({"stretch": g, "heard": heard, "possibly_missing": new})
        print(f"  {g[0]:.1f}-{g[1]:.1f}s  heard: " + (" / ".join(e["text"] for e in heard) or "nothing clear")
              + "  |  possibly missing from the script: " + (" / ".join(f"{e['text']} @{e['t']}" for e in new) or "nothing"))
    (d / "_gap.wav").unlink(missing_ok=True)
    save(d / "gaps.json", report)
    print("refine: suggestions saved to gaps.json. Nothing was changed. If a repeat or ad-lib is real, add it to script.json "
          "(with its rough time) and run `time` again.")
    return report


def cmd_preview(video, a, name=None):
    import preview
    d = proj(video)
    name = name or a.name
    lp = d / (f"lyrics_{name}.json" if name else "lyrics.json")
    data = load(lp) or sys.exit(f"no {lp.name}: run `time` first")
    out = preview.burn(video, data["lines"], d, name=f"preview_{name}" if name else "preview", font=a.font)
    print(f"preview: {out}")
    return out


def cmd_go(video, a):
    h = cmd_hear(video, a)
    if not h["lines"]:
        print("\nNO LYRICS: nothing sung was heard. If this is speech, caption it with plain Whisper instead.")
        return
    res = cmd_find(video, a)
    top = res[0] if res else None
    clear = bool(top) and top["score"] >= 1.2 and top["heard_lines_matched"] >= 2 and top["heard_lines_matched"] >= 0.5 * top["heard_lines"]         and (len(res) < 2 or top["score"] >= 1.8 * res[1]["score"])
    if not clear:
        print("\nSONG NOT SETTLED by the catalogue. Agent: identify the song from the heard lines (your own knowledge, then a web "
              "search), save its lyrics to a text file and run `song --lyrics ... --title ... --artist ...`; if you cannot, ask the owner.")
        return
    a.catalog = 0
    cmd_song(video, a)
    cmd_script(video, a)
    cmd_time(video, a)
    cmd_refine(video, a)
    cmd_preview(video, a)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["hear", "find", "song", "script", "time", "refine", "preview", "go"])
    ap.add_argument("video")
    ap.add_argument("--catalog", type=int)
    ap.add_argument("--lyrics")
    ap.add_argument("--title")
    ap.add_argument("--artist")
    ap.add_argument("--url")
    ap.add_argument("--second-listen", action="store_true", help="also run the whole-clip second listen with lyrics (not trusted by default)")
    ap.add_argument("--timer", default="vote", choices=["vote", "ctc", "whisper"], help="vote = median of several timers per word (default, see timing_vote.py); ctc = letter-level timer only; whisper = old timer")
    ap.add_argument("--no-gemini-vote", action="store_true", help="vote without the Gemini per-line listens (saves Gemini calls)")
    ap.add_argument("--no-repeat-test", action="store_true", help="do not let the timer test for repeated words/lines")
    ap.add_argument("--script")
    ap.add_argument("--name")
    ap.add_argument("--font", default="Arial")
    ap.add_argument("--again", action="store_true", help="redo a listening step even if its result is saved")
    a = ap.parse_args()
    video = Path(a.video).resolve()
    if not video.exists():
        sys.exit(f"no such file: {video}")
    {"hear": cmd_hear, "find": cmd_find, "song": cmd_song, "script": cmd_script, "time": cmd_time, "preview": cmd_preview,
     "refine": cmd_refine, "go": cmd_go}[a.cmd](video, a)


if __name__ == "__main__":
    main()
