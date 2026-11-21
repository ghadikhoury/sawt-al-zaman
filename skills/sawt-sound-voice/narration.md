# Narration: the voice, the script and the delivery

## 1. The voice (owner's settings, final 2026-11-17)
Gemini TTS **`gemini-3.8-flash-tts`**, voice **Charon**, **temperature 0**, and this style prompt (also `STYLE` in
`Tools/tts/gemini_tts.py`):
> A very deep, low-pitched, resonant bass voice, chest voice, never bright with just a bit of rasp. A documentary
> narrator in Modern Standard Arabic: warm and calm, at a natural, steady pace (not slow), with short pauses at the
> commas and the dots. Pronounce every word in correct formal Arabic, exactly as vowelled; every letter clear (ذ is a
> soft dh, never d). Pronounce every tanween fully (-un, -an, -in) and every case ending whenever the word is not
> followed by a pause — for example أَلْفٍ وَتِسْعِمِئَةٍ is "alfin wa tisʿimiʾatin". Drop the ending only on the word
> right before a comma or full stop, as in correct formal recitation.
He wants a deep, Morgan-Freeman-like narrator; one register only (mixing formal and colloquial was mispronounced).
Some pitch variation between takes is fine: check the words with Whisper and move on ("don't overcomplicate it").

## 2. Script rules for the voice
- **Full diacritics every time** (fatha, damma, kasra, sukun, shadda, tanween) so the model never guesses.
- **One take for the whole script.** If a line changes, regenerate everything in one call; never splice a single
  re-recorded line (tone and pace jump).
- **Names keep their natural ending:** فَيْرُوزْ with sukun; fix sounds through the style prompt, not the spelling.
- Pause shape comes from punctuation: commas for short breaths, full stops for longer ones.

## 3. Delivery principles (Arabic documentary practice)
From the Al Jazeera Media Institute's guide to documentary voice-over ([فن التعليق الصوتي للفيلم الوثائقي](https://institute.aljazeera.net/en/node/449)):
- Balance **الوصل والوقف** (connected speech and pauses) within a sentence; not every paragraph gets the same breath
  or emotional intensity.
- Pronounce correctly; **don't drop letters, especially at word ends** (our tanween rule).
- Avoid **promotional delivery** (الأداء الدعائي) and **poetic/declamatory delivery** (الأداء الشعري): warm, calm,
  informative — matches the owner's "warm and calm" prompt.
- The ear tires before the eye: an unpleasant or monotonous voice loses the viewer; keep narration stretches short and
  let picture and music breathe between them.
Writing the narration (what to say, not how): `../documentary/storytelling.md`.

## 4. Generating it (free, in the owner's Chrome)
The free API tier allows ~10 TTS requests a day; the owner's logged-in AI Studio speech playground has no such limit and
runs with "No API key selected" (free, no credits). Never spend paid credits on narration.
1. `aistudio.google.com/generate-speech` → new dialog → voice settings: search "Charon", select.
2. Model settings → temperature 0. Style → custom box: **type** the prompt above.
3. Click the speech block **by its ref** ("Speech block text"), Ctrl+A, Delete, **type** the script (setting the text by
   script changes only the screen). Verify the textarea before running.
4. Run (Ctrl+Enter), pause the autoplay, Download → `Downloads/Generated Audio <date> - <time>.wav` (24 kHz) → copy to
   `<project>/audio/narration_raw.wav`.
5. `python Sawt Al-Zaman/Projects/split_lines.py <project>/audio` → Whisper words + line spans → paste into
   `build_audio.py` LINES (check no boundary cuts a word) → `build_audio.py` → `cues.py` → mix → render.
The film plays narration ~1.1–1.2× faster than the raw take (pitch kept); judge pace at film speed.

## 5. Models
The owner wants **Gemini 4 Hydrogen** (`gemini-4-hydrogen`) for text and analysis work (a text model; voices stay on
the TTS model). For image analysis in his Gemini app, the strongest unlocked mode is Argon (Carbon is a paid upgrade).
The $20 Google AI Pro subscription raises limits in the web UI, not the API.

## 6. Pace and script length
Synthetic Modern Standard Arabic speech at "normal" rate runs about 4.5 syllables per second, and Arab listeners
rated that as slow ([Aldholmi et al., Interspeech 2021](https://www.isca-archive.org/interspeech_2021/aldholmi21_interspeech.html));
we speed the raw Charon take ~1.15× in the film. Rule of thumb from our films: ~11 short lines of narration fill
55–60 s at film speed with room for pauses and the singer's ending. Measure the real take rather than estimate; Arabic
speech rate is better measured in syllables than words.
