---
name: sawt-text
description: "Sawt Al-Zaman typography — the font library in two groups (BOLD: The Year of the Camel ExtraBold, PT Bold Heading; THIN: Camel Light, Diwani Letter, Amiri, Katibeh, Mirza, Scheherazade, Uighur), how to pair them, Arabic script rules (RTL, joins, tatweel, diacritics, calligraphic styles and their moods), how words arrive and leave (the owner's loved and banned text moves), text inside the scene and letters as a window. Use whenever any word goes on screen in a Sawt Al-Zaman video, when choosing or adding a font, and whenever the owner reacts to a font or a text effect."
---

# Sawt Al-Zaman text

Type is where most of this brand's artistry lives. The owner's verdicts below override anything generic.

## Files in this skill
| File | Read it when |
|---|---|
| [fonts.md](fonts.md) | Choosing a font: every kept font with its group, role and quirks; wanted, removed and banned fonts; how to add one |
| [text-moves.md](text-moves.md) | Animating words: loved moves with code, moves to redo, the researched catalogue of moves to test, text inside the scene, timing, banned looks |
| [designing-text-moves.md](designing-text-moves.md) | **Inventing a new move:** the anatomy of a move, starting from meaning, combining moves, brand filters, reading time, text and music |
| [letters-as-window.md](letters-as-window.md) | The "hollow" moving text he means: letters as a window onto moving footage, how to make it premium, ways to animate it |
| [arabic-script.md](arabic-script.md) | Setting Arabic: calligraphic styles and moods, RTL, joins, tatweel, diacritics, line height, digits |
| `fonts/` | Master font files (renderer copies: `Tools/Remotion/public/fonts/`) |
| `examples/` | His liked/banned screenshots and every font comparison sheet (`font_collection.png` = all kept fonts) |

Code: `Tools/Remotion/src/fonts/library.ts` (load fonts), `src/fx/TextMoves.tsx`, `src/fx/TextFx.tsx`.
Related: layout and colour → `sawt-design`; motion, cut-outs and transitions → `sawt-motion-edit`.

## The core rules
1. **One BOLD + one THIN per frame.** He loves weight contrast. Pick one font from each group that suit each other;
   never more than two families in a frame. Default pair: **The Year of the Camel ExtraBold + Camel Light**.
   - BOLD: The Year of the Camel ExtraBold (first choice), PT Bold Heading.
   - THIN: Camel Light, Diwani Letter, Amiri, Katibeh (documentary spoken lines), Mirza, Scheherazade, Uighur (last two small only).
2. **Brand colours only** for text: sand, parchment, champagne (muted, never bright gold), terracotta, dusty rose, deep
   brown; brick red sometimes. No blue, green or maroon. One accent colour per frame.
3. **Big beside small.** Hero word 3–5× the supporting line. On 1080×1920: hero/emphasis 120–180 px, base Arabic
   76–96 px, small lines 40–46 px (never smaller). Over busy footage use a soft dark shadow or gradient scrim, never a hard box.
4. **Text lives inside the scene**: behind the subject, behind objects, through letters as windows, between layers;
   never stuck flat on top.
5. **Every word moves with a reason**: arrives physically (ease-out from beyond the frame, out of blur, rolled in a
   slot), holds still to be read, leaves deliberately. No plain fades, no even-speed slides.
6. **Arabic done right**: RTL, joins intact, no letter-spacing, lam-alef together, tatweel only between joining letters
   and never animated, Arabic-Indic digits, generous line height for calligraphic faces.
7. **Timed to the voice**: each word at its start; repeats repeat; a short sound only on words that should draw the eye.
8. **New fonts are shown before use**, as a sheet of the film's real words in brand colours.

## Banned (never)
Outline text that fades/fills in; split-colour words; glitch/RGB fringes; animated stretch; flat wall text, loud glow,
big white capitals; zoom-through exits; bouncing/rotating words; fonts on the "not to use" list in fonts.md.
