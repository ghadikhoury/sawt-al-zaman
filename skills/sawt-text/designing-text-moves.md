# How to invent a new text move (a method, not a menu)

The catalogue in `text-moves.md` is a reference. This file is for creating new moves that fit the brand. A move that
"makes or breaks the video" (the owner) comes from a reason, physical motion and good timing, not from filters.

## 1. The anatomy of any text move
Every professional text animation (After Effects text animators, GSAP SplitText, Apple keynote titles) is built from
the same parts. Decide each one consciously:
| Part | Choices | Brand default |
|---|---|---|
| **Unit** | line · word · (letter) | **word** for Arabic (letters only with ZWJ joins, rarely) |
| **Properties** | position, scale, rotation (2-D/3-D), opacity, blur, mask/clip, weight (font swap), colour, light | 2–3 at once, never all |
| **Path** | straight, arc, from depth (z), along a curve, around a subject | arcs and depth over straight lines |
| **Origin** | outside the frame, behind an edge, behind the subject, out of focus, from a line, from another word | anywhere *meaningful* |
| **Timing** | punchy entrance 3–6 frames (reference), calm 12–24; hold still to read; exit 3–10 frames | exits shorter than entrances |
| **Easing** | ease-out arrival, ease-in exit, overshoot only for a landing | strong ease-out (expo/quint-out) |
| **Stagger** | 2–4 frames between units, or each word at its spoken/sung start | timed to the voice |
| **Layer** | in front of / behind the subject, inside a window, between photo layers | in the scene, not on top |
| **Sound** | none (default) or one short accent | only if it should draw the eye |
| **Exit** | reverse, continue the path, blur back, leave past camera, carry over into the next scene | a designed exit, never a cut-off |

## 2. Start from meaning (the creative engine)
- **Let the word suggest its motion.** رحل (left) leaves the frame and doesn't return; عاد (returned) comes back along
  the path it left on; صوت (voice) arrives in a ripple of focus; سهرة (an evening) appears as a light comes up;
  تخونوه (betray him) is pulled away from its pair; اسمها (her name) is revealed last, inside the frame of the opening.
- **Let the voice suggest its timing.** A held sung note holds the word still (or reveals an already-stretched word
  slowly); a quick spoken list staggers fast; a pause in the narration is a held, empty frame.
- **Let the scene suggest the layer.** A skyline → the word rises behind it; a face → the word passes behind the head;
  a map → the word lands where the line ends; a photo collage → the word sits on top as the photos snap in.
- **Let the story suggest continuity.** The word that ends a scene can become the first element of the next
  (carry-over); a small word in a line can grow into the next hero.

## 3. Combine, don't decorate
New moves usually come from **combining two known ones with a reason**: focus pull + depth stack; mask rise + counter
move; front/behind pair + shuffle (the front word shuffles while the back word holds); window word + slow push of the
picture inside; dimmed line + weight swap on the stressed word. Change one variable at a time when testing.

## 4. Brand filters (reject a move if it fails any)
1. Does it have a reason (meaning, voice, scene or story)? 2. Is it physical (ease, arc, depth), not a filter? 3. Can
the word be read for at least ~0.8 s at rest? 4. Brand colours only, one accent? 5. None of the banned looks (outline
fill, split colour, glitch/RGB, animated stretch, bounce, rotate-every-word, zoom-through exit, typewriter clicks, flat
wall text, loud glow)? 6. Arabic intact (RTL, joins, dots)? 7. Only one hero move at this moment?

## 5. Reading time (so motion never costs legibility)
- A word or line must be fully at rest long enough to read: **minimum ~0.83 s even for one word** (subtitle practice),
  and roughly 13–17 characters per second for a line (Netflix's general adult limits; no published Arabic figure —
  stay on the slow side for calligraphic fonts).
- The entrance doesn't count as reading time; the hold does.
- Sources: [Netflix Arabic timed-text guide](https://backlothelp.netflix.com/hc/en-us/articles/215517947),
  [subtitle reading speed](https://subtitle-toolset.pages.dev/guides/subtitle-reading-speed/).

## 6. Text and the music
When words appear over music without narration (lyric reels, a title over an instrumental), they can follow the music:
a word lands on a downbeat, a line builds across a phrase, a held note holds the word. Follow the **musical
structure** (phrases, the singer's line), not every beat: typography that only mirrors beats feels mechanical, and
vocal material asks for flowing motion rather than hard hits ([FEVR: sound + type](https://wearefevr.com/sound-type)).
How to get the beats, downbeats and phrases: `../motion-edit/music-sync.md`.

## 7. Test before use
Build each new move as a short test (one word, brand colours, the real font), render stills at the start, middle and
rest frames, then a 3 s clip; check against §4; show the owner with others side by side. Record his verdict in
`text-moves.md`.
