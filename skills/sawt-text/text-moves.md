# How words arrive, live and leave

Code: `Tools/Remotion/src/fx/TextMoves.tsx` (the test reel, `Sawt Al-Zaman/Exports/text_moves_test.mp4`) and
`Tools/Remotion/src/fx/TextFx.tsx` (letter windows, pushes, pop-ups). Owner's verdicts are from 2026-11-18.

## Loved: use these
| Move | How it works | Code |
|---|---|---|
| **1. Arrives from beyond the screen** | Starts ~3× size, blurred, close to the lens, settles in ~0.8 s with ease-out; leaves past the camera (scales up, blurs out). | `FlyIn` |
| **2. Word by word, mixed weights** | Words of one line arrive in turn (~0.3 s apart), each rising ~30 px out of a blur; bold and thin words alternate in size. | `Build` |
| **3. Shuffle** | The word rolls up out of a slot with vertical motion blur and the next word takes its place; the slot is a soft mask. | `Shuffle` |
| **7. Written on, already stretched** | A right-to-left mask reveals a word that is set already stretched (tatweel), like a pen stroke. | `WriteOn` |
| **8. Big word behind, accent in front** | A large pale word settles behind; a smaller terracotta word lands in front, overlapping it, with a slight overshoot. | `FrontBack` |

## From the reference's frame analysis
Precise numbers (blur-pop settle, word stagger 0.15–0.2 s, stacked lockups, diagonal line, orbit geometry, behind-head
punch, exits) and what we leave out: `../motion-edit/references/premium_DfMiYjYRbMI_analysis.md`.

## Verdicts on test reel 2 (`Exports/text_moves_test_2.mp4`, 2026-11-18)
| Move | Verdict |
|---|---|
| A2 counter-move rise, A4 horizon line, A5 arch reveal, B2 focus pull, B3 depth stack, B4 hinge flip, C2 dimmed line lit word by word, C5 words leave one by one, D3 weight swap, E1 light sweep | **Liked** |
| B5 behind the head | **Liked, with a rule:** text behind a subject must come **already stretched** (tatweel set in, never animated) so the word stays readable around the head |
| D2 a small word becomes the hero | **Effect liked**; the start looked mushed (the small word overlapped its neighbours). Fix: measure the line and start the hero word exactly in its own slot |
| M1 words on the beat | **Varying weights liked; the timing failed:** "none of the words landed on the beat". Text should *fit* the music; it needn't hit every beat. See `../motion-edit/music-sync.md` §6 |
| M2 photo run on the beats | Nice, but **"way, way faster"** (see `../motion-edit/devices.md`) |
| C4 replace in place | **Disliked** |
| B6 orbit (second try) | **Still not good** ("doesn't look good at all"). Study the reference reel's orbit closely (or the owner's Gemini analysis) before a third try |

## Verdicts on test reel 3 (`Exports/text_moves_test_3.mp4`, built from the reference's frame analysis, 2026-11-18)
| Move | Verdict |
|---|---|
| P1 stacked lockup (small words over one big word, 5-frame blur-pop, drop-away exit as the next slams in) | **Liked** |
| P3 vertical stack, diminishing sizes | **Liked** |
| P4 small word becomes the hero (fixed start) | **Liked** |
| P5 behind the head, pre-stretched, punch-in | **Liked, stretch it more.** Goal for all text behind something: **it must stay readable**; stretch until the hidden part doesn't stop the word being read |
| P6 orbit v3 (reference geometry) | **Somewhat good**: animation OK, but the words were too small and the spin may be too fast for the song. Still not what the reference does |
| P8 silhouette spawn + editorial labels | **Liked** |
| M2 fast photo runs (change every 3 frames, holds) | **Liked, speed right** |
| M1 words on detected accents | **Totally off the beat again** (see `../motion-edit/music-sync.md` §6) |
| P2 diagonal line, P7 ribbon wrap, P9 drop/smear exits | **Not good** |
Overall: the reference's transitions are still not captured ("you still haven't really gotten the sense of the transitions I liked"). To continue later.

## To redo before use
- **4 → words leave one by one** (not letters): each word of the line exits in turn, drifting and blurring.
- **5 → orbit, done properly**: the idea was liked, the execution was "basic, cringe, cheap". Requirements: a real
  cut-out subject; text on a ring that tilts in perspective (an ellipse in 3-D), scales down and dims at the back, truly
  passes behind the head and comes round in front; mixed sizes along the ring; ease the speed, don't spin constantly.
- **6 soft glow** was not picked: glow stays a baseline finish, not a move.

## Seen in reel 1 and expected to fit (not yet tested)
A word pulled from blurred to sharp focus; a subtle colour shift within brand colours as a word glows; text running
along a path around a cut-out body; a thin bracket or line drawing to tie two words; small monospace labels beside a
word (type-specimen style).

## Text inside the scene (the owner's top "premium" point)
- **Behind the subject:** footage, the big word, then the subject cut-out on top. **The word comes already stretched**
  (tatweel set in from the start, never animated) so it stays readable around the subject (owner, 2026-11-18). It is wider than the head so
  the head interrupts its middle and both ends read; at least two-thirds of the letters visible; one or two key words
  only, then it leaves. Match the scene: `multiply` dark ink on light, `screen`/`soft-light` light text on dark, a
  little blur and grain. The cut-out decides it: check frames with the most movement; feather 2–4 px.
- **Behind objects:** a word rising behind a skyline or a mountain range (liked: Umm Kulthum skyline, نيحا behind the
  mountains).
- **Letters as a window** onto the picture (liked: "the effect is nice and it works"): the word is a mask; inside, a
  second copy of the picture, offset/bigger, moving differently so the letters feel alive. Keep the inside the plain
  picture (brighter or softer); the tinted sand inside "didn't fit". Over a still, keep the inside moving (`Drift`).
  `TextWindow` in `TextFx.tsx`. Window word exit: the letters swell open to reveal the picture (liked).
- Cut-out tooling: `../motion-edit/camera-and-compositing.md`.

## Timing rules
- Each word enters at its spoken/sung **start** (a few frames after onset), never at its end; entrance done in 8–18
  frames so it's readable while being said. Repeated sung words repeat on screen.
- Ease-out in, ease-in out. Hold still while it is read. Clear a line before the next starts; never hard-cut text off.
- A short sound only on the words the viewer should notice (sound-voice skill).
- Vary the move by meaning, not at random; keep one rule per film for which word gets which move.

## Banned text looks
Outline ("hollow") text that fades or fills in (`WebkitTextStroke`: breaks at joins, looks basic; to him "hollow" means
something happening *inside* the letters). Split-colour words (coloured copies closing into one). Glitch, RGB split,
coloured fringes. Animating the tatweel stretch. Text stuck flat to a wall, loud glowing letters, big white capitals
(reel 1). Cringe zoom-through exits (BaeedAnak v2). Bouncing, rotating every word, typewriter clicks, neon colours.
Text overlapping other text or the main image except on purpose (behind-subject, front/behind pair).

---

## Catalogue of professional text moves to test next (researched 2026-11-18)
How motion designers build text animation (After Effects text animators, GSAP SplitText, Apple-style keynote titles):
every move combines a few properties (position, scale, blur, opacity, rotation, mask) on a unit (line, word, rarely a
letter), staggered and eased. The premium look comes from **masks, depth, focus and stagger with strong ease-out**,
not from filters. Filtered against the owner's bans (no bounce, no typewriter clicks, no glitch, no outline fill, no
animated stretch, no zoom-through exits). Arabic: always by **word** (or line), reveals run right → left.
Status: ✅ loved already · 🔁 to redo · 🧪 new, to show him.

### A. Mask reveals (cleanest, most "Apple")
| # | Move | How | Status |
|---|---|---|---|
| A1 | Rise from behind an edge | each line inside an overflow mask moves up from ~110 % below, expo-out, lines staggered ~0.1 s. Alone it's our old "basic" entrance: pair it with blur or a counter-move | (in use; upgrade) |
| A2 | Counter-move rise | the word rises while its mask (or the picture inside) drifts the other way: a little parallax inside the reveal | 🧪 |
| A3 | Pen-stroke write-on | soft-edged mask sweeps right → left across an already-stretched word | ✅ (#7) |
| A4 | Horizon line reveal | a thin champagne line draws first, then the word rises from behind it; the line stays as an underline or retracts | 🧪 |
| A5 | Shape reveal | the word appears inside an opening shape (arch, circle, letterbox strip) that grows to show it | 🧪 |

### B. Depth and camera (the owner's strongest wish: text in the scene)
| # | Move | How | Status |
|---|---|---|---|
| B1 | From beyond the lens | starts ~3× size, blurred, close to camera, settles; leaves past the camera | ✅ (#1) |
| B2 | Focus pull | the new word racks from blurred to sharp while the previous one blurs back (reel 1) | 🧪 |
| B3 | Depth stack | words of a line at different depths (far ones smaller, slightly blurred); a slow camera drift makes them shift in parallax | 🧪 |
| B4 | Hinge flip | each word swings in from rotateX −70° → 0 with perspective, ease-out, staggered; subtle, never a spin | 🧪 |
| B5 | Behind the subject | the word rises from behind the artist's head or shoulder (cut-out) | ✅ idea (build with cut-outs) |
| B6 | Orbit | text on a perspective ring around the cut-out head, back half hidden | 🔁 (#5 redo) |

### C. Stagger and rhythm (timed to the voice)
| # | Move | How | Status |
|---|---|---|---|
| C1 | Word-by-word build | words arrive in turn out of blur, mixed weights | ✅ (#2) |
| C2 | Dimmed line, lit word by word | the whole line is already there dim and soft; each word lights to full and sharpens as it is spoken (Apple keynote reveal). Ideal for narration lines | 🧪 |
| C3 | Shuffle / slot | word rolls up out of a slot, the next replaces it | ✅ (#3) |
| C4 | Replace in place | a word blurs/dissolves into the next word in the same spot | ❌ disliked |
| C5 | Words leave one by one | exit in turn, drifting and blurring | 🔁 (#4 redo) |

### D. Weight and scale (his bold/thin contrast, animated)
| # | Move | How | Status |
|---|---|---|---|
| D1 | Front/behind landing | big pale word behind, accent word lands in front with a slight overshoot | ✅ (#8) |
| D2 | A small word becomes the hero | in a line, one small word grows and moves to become the big word while the others shrink and recede (the "small detail becomes the next hero" idea, in type) | 🧪 |
| D3 | Weight swap | the thin version of a word cross-dissolves into the bold version (Camel Light → ExtraBold) on the stressed syllable | 🧪 |

### E. Light and material
| # | Move | How | Status |
|---|---|---|---|
| E1 | Light sweep | one soft band of light passes once across a name (muted, not gold-shiny), as it settles | 🧪 |
| E2 | Letters as a window | the word as a window onto the picture | ✅ (plain inside) |

### F. Arabic-only ideas
| # | Move | How | Status |
|---|---|---|---|
| F1 | Dots land last | the letter bodies appear, then the dots and diacritics settle a few frames later (follow-through, principle 5). Needs the word split into body and dot layers (SVG outlines) | 🧪 advanced |
| F2 | Calligraphic stroke drawing | a single hero word in Diwani drawn as pen strokes (`evolvePath` on the word's outline) | 🧪 advanced |

### Timing guide (revised 2026-11-18 from the reference's frame analysis)
**Punchy (the reference's default): entrance 3–6 frames (0.1–0.2 s)** — blur-pop scale settle with motion blur — then
hold completely still. **Calm (documentary narration, held notes): 12–24 frames.** Old default was 0.4–0.8 s for
everything, which read soft. With strong ease-out (`expo.out`-like); stagger 2–4 frames between words (or each
word at its spoken start); exit 0.25–0.4 s, ease-in; hold at least long enough to read (~0.3 s a word + 1 s).
Exits shorter than entrances. One hero move per moment; supporting text uses a quieter version of the same move.

Sources: [School of Motion: text animators](https://www.schoolofmotion.com/blog/text-animators-after-effects),
[Adobe: animating text](https://helpx.adobe.com/after-effects/using/animating-text.html),
[GSAP SplitText docs](https://gsap.com/docs/v3/Plugins/SplitText/),
[Codrops: SplitText demos](https://tympanus.net/codrops/2025/05/14/from-splittext-to-morphsvg-5-creative-demos-using-free-gsap-plugins/),
[21st.dev: Apple-style word reveal](https://21st.dev/@dev.yadhakim/components/scroll-reveal-text),
[Jitter: Apple event title reveal](https://jitter.video/template/sliding-title-reveal-apple-event/),
[Linearity: kinetic typography](https://www.linearity.io/blog/kinetic-typography/),
Khajavi, *Arabic Script in Motion* (Palgrave 2019, ch. "Kinetic Behaviors").
