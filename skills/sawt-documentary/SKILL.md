---
name: sawt-documentary
description: "How to make a Sawt Al-Zaman one-minute life documentary (an artist's life in formal Arabic narration over archive photos and the artist's own music) — the step-by-step workflow from idea to delivered file, the owner's verdicts on past films (what made Umm Kulthum 'perfect', why the darkroom and paper-theatre films failed), picture rules (the face every 15 s, real photos, no empty frames), Arabic storytelling principles (ḥakawātī, frame and thread, balāgha in light doses, tarab build-and-release, Al Jazeera's narration rules), script language rules, fact checking, photo sourcing and credits. Use when starting, scripting, building, revising or delivering any documentary, explainer or artist-story video."
---

# Sawt Al-Zaman life documentaries

**The bar:** the Umm Kulthum film (`Tools/Remotion/src/UmmKulthumLife.tsx`), "absolutely magnificent, literally
perfect": one governing idea, real archive photos, a rich drawn world, beats keyed to the narration words, each device
used once with a reason, layered sound, silence before the peak, her real voice arriving at the end.

## Files in this skill
| File | Read it when |
|---|---|
| [storytelling.md](storytelling.md) | Writing the script: Arabic storytelling tradition, rhetoric, tarab, documentary craft, the 60-s shape |
| [hooks-and-ethics.md](hooks-and-ethics.md) | Writing the first seconds (open loop, show something at once, honest payoff); respect for the archive (no AI colourising or face restoration) |
| [script-and-sources.md](script-and-sources.md) | Language rules he set, fact checking, photos (Wikimedia), credits, music files |

This skill is the workflow; the craft lives in the other skills: look and the 20 principles → `sawt-design`; fonts and
text moves → `sawt-text`; motion, devices, editing, camera, production checklist → `sawt-motion-edit`; voice, music
and sound → `sawt-sound-voice`.

## Workflow (a project lives in `Sawt Al-Zaman/Projects/<artist>_life/`)
1. **Research** facts (keep only what sources agree on) and gather photos (Wikimedia paced; credits). Note the
   artist's vibe.
2. **Idea + script:** one governing idea in a sentence; ~11 short, fully vowelled lines (`audio/script.txt`) shaped
   hook → origin → gift/struggle → turn → peak → legacy/name (storytelling.md). Formal Arabic, his grammar rules.
3. **Voice:** one take of the whole script (sawt-sound-voice/narration.md) → `split_lines.py` → `build_audio.py`
   (LINES, TEMPO ~1.15) → `narration.wav` + `timeline.json`.
4. **Music:** clean his recording's jumps (`find_jumps.py`), choose sections and stems (Demucs).
5. **Cues:** `audio/cues.py` (uses `Projects/life_cues.py`): every visual beat keyed to a narration word.
6. **Design:** a new style for this artist; pick 2–3 devices with story reasons (sawt-motion-edit/devices.md), one
   BOLD + one THIN font (sawt-text). **Stills first**, checked against the 20 principles.
7. **Build** the Remotion composition (`Tools/Remotion/src/<Artist>Life.tsx`, register in `Root.tsx`).
8. **Mix:** `audio/mix.py` (uses `Projects/life_mix.py`): sound rules, effects only on attention points, −14 LUFS.
9. **Render and check:** contact sheet every ~2.5 s, Whisper pass on the final narration, loudness, the production
   checklist (sawt-motion-edit/production.md). Fix, re-render, then deliver to `Sawt Al-Zaman/Exports/`.
10. **Record** every new owner verdict in the right skill file the same day.

## The owner's rules for documentaries
- **The artist's face at least every 15 s** (photo, carved or drawn version); a photo in the opening too. Reuse few
  photos in different treatments rather than leave gaps.
- **No empty placeholders and no near-blank moments** between scenes (overlap them).
- **Reflect the artist lightly**, change scenes, new style per film (rejected: Abdel Halim darkroom — too gloomy,
  unreadable projections, constant hum; Fairuz paper theatre — one theme, "Roman Empire" colours, narrating from a
  stage).
- **Professional, not cartoon:** no clip-art props; real photos with depth and camera moves.
- **Nostalgic and cool, not National Geographic:** fewer fact captions; feeling first.
- **Fixes he lists apply to all films**, not just the one named. Deliver finals together; show results, keep moving.
- Past films and their state: Umm Kulthum (the bar), Wadih (liked; asked: known name, photos regularly), Fairuz v2,
  Abdel Halim v3 (illness scene fixed; candles may read cartoonish), Baligh v3 (done: no oud strings move, title font
  changed), Warda v3 (done: flag at true proportions). Baligh and Warda use Ruwudu on names, now disliked; no redo asked.
