# Arabic script craft for video

## 1. The calligraphic families and their feeling
Arabic type descends from a few calligraphic styles; each carries a mood. Pick by meaning, not novelty.
| Style | Look | Feeling / where it fits | Our fonts |
|---|---|---|---|
| **Naskh** | Upright, round, readable | Everyday clarity, books, captions; classic tarab when high-contrast | Amiri, Scheherazade, Mirza, Uighur, Katibeh (naskh-poster) |
| **Thuluth** | Tall, sweeping, monumental | Prestige, headings, ceremony | (none owned) |
| **Ruqʿah** | Short, quick, practical | Handwritten, casual, intimate | (Aref Ruqaa and Rakkas were rejected) |
| **Diwani** | Flowing, ornate, Ottoman court | Romance, ceremony, nostalgia; accent words only | **Diwani Letter** |
| **Kufic** | Geometric, angular, monumental | Architecture, modern posters | (Reem Kufi shown, not chosen) |
| **Nastaʿlīq** | Sloped, hanging | Persian/Urdu poetry; reads Persian to Arab eyes | (IranNastaliq not chosen) |
| Modern display | Heavy, simplified, poster | Titles, hooks, hero words | **The Year of the Camel**, PT Bold Heading |
Sources: [Rosetta: Arabic calligraphic styles](https://old.rosettatype.com/blog/2016/05/24/Arabic-calligraphic-styles),
[Middle East Eye: seven styles](https://acquiaprod.middleeasteye.net/node/267721), [Wikipedia: Islamic calligraphy](https://www.wikipedia.org/wiki/Arab_calligraphy).

## 2. Rules that keep Arabic correct on screen
- **Right to left:** `dir="rtl"` on every Arabic element; reveals and write-ons run right → left.
- **Never letter-space Arabic** (it breaks the joins). Use size, weight and face for emphasis.
- **Animate words, not letters.** If letters must move separately, keep their joined shapes with zero-width joiners
  (U+200D) on both sides of each letter (`letters()` in `Tools/Remotion/src/fx/TextMoves.tsx`). The owner prefers
  words leaving one by one over letters anyway.
- **Keep lam-alef (لا) together**; never split it across animation units.
- **Diacritics:** narration scripts are fully vowelled (see sound-voice); on-screen text normally isn't, except a
  deliberate shadda or tanween that the word needs (فعلاً، عنّك). Check that the font places them well (PT Bold Heading
  puts shadda too high). Harakat on lyrics only after the text is approved; sung vowels can differ from grammar.
- **Line height and padding:** calligraphic faces (Diwani, Amiri) have tall ascenders and long tails; give line height
  ≥1.4 (Diwani ≥1.6) and padding so swashes aren't clipped by masks or boxes.
- **Numbers:** use Arabic-Indic digits (١٩٧٢) in Arabic text. Never mirror them.
- **Tatweel (kashida, ـ):** stretches a word *between two joining letters only*. Use it sparingly, as emphasis or to
  fit a line, never as default justification ([Reading University: on Arabic justification](https://research.reading.ac.uk/typoarabic/on-arabic-justification-part-1/)).
  The owner likes **some words set already stretched next to normal ones** and **dislikes animating the stretch**.
  Exception: a held sung note may open a word around a subject (BaeedAnak `OpenBehind`), but prefer static stretch.
- **Hierarchy in Arabic** comes from size, weight and face, not italics (Arabic has no true italic; "italic Arabic"
  fonts are slanted Latin habits and look wrong — Amiri italic was hated).
- **Words, not letters, carry meaning:** "draw letters, design words" — check how the whole word shapes, not single
  glyphs ([Comm Arts: basic principles of Arabic type design](https://www.commarts.com/features/basic-principles-of-arabic-type-design)).

## 3. Arabic with English
Arabic is the hero; English small beneath (or omitted on the Arabic account). Different fonts per script; never two
scripts at equal size side by side. Latin fonts installed for translations: Cormorant Garamond italic, Playfair,
Bodoni Moda (not yet reviewed by the owner).

## 4. Quality check for every word on screen
Joins intact? Dots and diacritics present and well placed? Nothing clipped (swashes, tails, mask edges)? Correct
spelling and the owner's grammar rules (see `../documentary/script-and-sources.md`)? Reads in under a second at phone size?
