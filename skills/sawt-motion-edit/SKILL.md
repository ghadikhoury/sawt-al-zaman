---
name: sawt-motion-edit
description: "How Sawt Al-Zaman videos move and are cut — premium motion physics (easing, anticipation, follow-through, timing), the owner's liked and banned transitions and devices with their code (photo pop-up collage, sliding push, letters as a window, carry-over, woodcut/pencil landscapes, map journeys, aspect-ratio transitions), editing and pacing (Murch's rule of six, J-cuts, cut on the voice), virtual camera and parallax, cut-outs for text behind the subject, the lyric-reel method, the reference reels, and Remotion production, safe areas and the pre-delivery checklist. Use when animating, cutting, building transitions or effects, making a lyric reel, or rendering and checking any Sawt Al-Zaman video."
---

# Sawt Al-Zaman motion and editing

"Every move has a reason and good timing." Physical, purposeful, brief — never a kids' show, never decoration.

## Files in this skill
| File | Read it when |
|---|---|
| [motion.md](motion.md) | Animating anything: easing and timing rules, liked and banned motion |
| [devices.md](devices.md) | Choosing devices and transitions for a film: every liked device with where its code lives |
| [transitions.md](transitions.md) | Choosing a transition: invisible ones (default), accents (rare), banned, montage rhythm |
| [music-sync.md](music-sync.md) | Timing cuts, words and motion to the music: song map, what to hit, Arabic music specifics (taqsīm, īqāʿ, qafla), beat/downbeat tools, audio-reactive motion |
| [editing.md](editing.md) | Cutting: Murch's rule of six, split edits, rhythm, openings and endings |
| [camera-and-compositing.md](camera-and-compositing.md) | Camera moves, parallax, depth-map 2.5-D photos, aspect transitions; cut-outs and text-behind-subject recipes |
| [lyric-reel.md](lyric-reel.md) | Making a lyric (single song clip) reel |
| [references.md](references.md) | Studying the owner's reference reels (videos in `references/`) |
| [production.md](production.md) | Remotion, rendering, safe areas, export, and the **checklist before showing the owner** |

Code: `Tools/Remotion/src/` (films), `src/fx/` (effects toolkit). Related: `sawt-design` (layout, colour, the 20
principles), `sawt-text` (fonts and text moves), `sawt-sound-voice`, `sawt-documentary`. Generic helpers installed:
`remotion-best-practices`, `mg-object-separation` (SAM 2 cut-outs), `ffmpeg-color-grading`.

## Core rules
1. **Motion with physics:** ease-out arrivals, shorter ease-in exits, a small anticipation before big moves, parts
   settling at different times, curved paths, snap then hold.
2. **Depth over flatness:** cut out the subject; text and shapes pass behind and in front; parallax on stills.
3. **Devices from the menu, two or three per film**, each with a story reason (devices.md); never all, never stacked.
4. **Cut on the voice and music**; flurries only as punctuation, then breathe; J-cuts to bring sound in first.
5. **Aspect-ratio change only as a transition** (narrow → wide with moving images), not constantly.
6. **Accent transitions stay rare.** Glitch, RGB split, colour fringes, white flashes as decoration, zoom-through exits,
   bouncing or rotating words: banned.
7. **Stills before motion; contact sheet after render**; run the production checklist before sending.
