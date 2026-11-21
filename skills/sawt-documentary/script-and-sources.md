# Script language, facts and sources

## 1. Language rules the owner set
- **Formal Arabic (فصحى), one register**, fully vowelled for the voice (`../sound-voice/narration.md`).
- **Call artists by their known names** (وديع الصافي, not his birth surname).
- **لبنان is feminine** (تستيقظ لبنان، ما زالت لبنان تبدأ صباحها).
- Wording he corrected: «عرف الفقدان» (not الفقد); «زياد، الذي لم يتجاوز السابعة عشرة» (not «ولم يتجاوز»).
- On-screen text = the narration's key phrases, not full sentences (text skill).
- Edit for the ear: shorten long sentences, replace heavy constructions, remove repeated ideas, make the text one body
  (Al Jazeera's editing rules).
- No politics ("it's just music").

## 2. Facts
Keep only what sources agree on (English and Arabic Wikipedia, a reputable obituary or institution). Record sources and
what was left out as unverified in `<project>/CREDITS.txt`.

## 3. Photos and assets
- **Real archive photos**, public domain or free licence. The owner likes the photos found so far and doesn't need more
  for every film.
- **Wikimedia Commons:** collect all file names first; fetch through the API (`prop=imageinfo&iiurlwidth=1280`) one at a
  time, seconds apart; stop at the first 429 and never work around rate limits. If blocked, ask the owner to save the
  files from the Commons pages in his browser into the project's `archive/` folder.
- Real flags and symbols as files (e.g. `Flag_of_Algeria.svg`), at true proportions.
- **Credits:** every photo's source, licence and author in `CREDITS.txt`; CC BY-SA photos need credit when posting
  (e.g. "Photo: FTOUKI, CC BY-SA 4.0").
- Maps: Natural Earth (public domain) via the project's `tools/make_map.py`.
- No AI face restoration or colourising of real artists.

## 4. Music
The owner supplies it as a screen recording (`Sawt Al-Zaman/Background Music/<artist>/owner_reference.mp4`). Clean every
jump before use (`../sound-voice/mixing.md`).
