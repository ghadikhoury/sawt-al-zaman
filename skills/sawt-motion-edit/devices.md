# Library of devices the owner likes (with where a working version lives)

A menu, not a checklist: two or three per film, each with a story reason; don't repeat a device in back-to-back films.
Paths are under `Tools/Remotion/src/` unless noted.

## Premium-reel moves (2026-11-18, from his reference reels)
| Device | Verdict | Build |
|---|---|---|
| Photo pop-up collage | "the images collage is nice" | `fx/TextFx.tsx` `PhotoPop` (hard cuts every 2–3 frames, full frame, reverse out) |
| Letters as a window onto the picture | "the effect is nice and it works" (keep the inside plain, not tinted) | `fx/TextFx.tsx` `TextWindow`, `Drift` for stills |
| Sliding push with strip slide and motion blur | liked; **blur yes, colour fringes no** | `fx/TextFx.tsx` `SlidePush`, `Smear` (keep `split` = 0) |
| Font flicker on arrival | in the toolkit; use only liked fonts | `fx/TextFx.tsx` `flickerFont` |
| Text moves 1, 2, 3, 7, 8 | loved | `fx/TextMoves.tsx` (see `../text/text-moves.md`) |
| Rapid photo changes + sound, background photo + smaller main photo | liked (reel 2); bursts of a change **every 3 frames** with holds between: **speed approved** (test 3) | `fx/TextMoves3.tsx` `M2` |
| Aspect change as transition (narrow → wide, images moving) | liked (and in the Umm Kulthum film) | `UmmKulthumLife.tsx` frame change; build a reusable one |
| Cut-out artist moved around with text behind | liked | needs cut-outs: compositing.md |
| Silhouette spawn + editorial labels (artist first appears as a glowing parchment silhouette, small labels by the name) | liked (test 3) | `fx/TextMoves3.tsx` `P8` |
| Ribbon wrap | not good (test 3) | `fx/TextMoves3.tsx` `P7` |
Banned in the same toolkit: `ColourSplit`, `Flash`, `SplitWord`, `Smear split > 0` (glitch / colour fringes).

## Transitions from the documentaries
- **Carry-over element** — one element holds its place while everything changes around it into the next scene. Keep
  it outside both scene layers; cross the scenes behind it. Once or twice a film.
- **Small detail becomes the next hero** — the far ridge lifting off the mountains and becoming the song's waveform
  (`WadihLife.tsx` ridgePath); the sun becoming the moon (`FairuzLife.tsx` Disc).
- **Film strip stepping on the beat** (`AbdelHalimLifeV2.tsx` FilmStrip). Never leave a frame empty.
- **Whip pan** (`WadihLife.tsx`, hook to mountains).
- **Watercolour bloom** opening a photograph (`FairuzLifeV2.tsx` Bloom); give the mask room so no face is cut.
- **Water drop → splash of colour / wash** (`FairuzLifeV2.tsx`, the drop for فيروز; Wash).

## Inside a scene
- **Pencil-drawn / woodcut landscape** — the Wadih mountains, carved knife lines that look pencil-drawn; the owner
  "really liked" it. `Sawt Al-Zaman/Projects/wadih_life/plates.py` + `woodcut.py`; layered so text sits behind a range.
- **Cross out, then circle** (contact sheet / card): rejection, then comeback (`AbdelHalimLifeV2.tsx` Sheet, NameCard).
- **Photos hung on a string**, camera tracking forward through the years (`AbdelHalimLifeV2.tsx` StringLine); only
  with enough photos.
- **Text behind a building / range** (Umm Kulthum skyline; نيحا behind the mountains).
- **Window word with swell-open exit** (Umm Kulthum finale).
- **Board journey / line that travels** — one camera over one drawn world; a pen line draws a route, the place name
  lands with a squash (`UmmKulthumLife.tsx`).
- **Real map journey with arcs** (`WardaLife.tsx`, Natural Earth coastlines; `warda_life/tools/make_map.py`).
- **Music-staff line theme** carried through a film (Baligh: "I like the strings theme"; but not onto objects).
- **Rolling year** digits; **static stretched word**; **shape match**.

## Rules that come with them
The artist's face at least every 15 s (photo, carved or drawn version); no empty placeholder frames; real symbols
(the real flag, real pyramids), true proportions; the vibe of the artist is a flavour, not a theme for the whole film.
