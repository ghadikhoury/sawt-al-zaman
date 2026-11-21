# Editing and pacing

## 1. What decides a cut (Walter Murch's Rule of Six, in priority order)
**Emotion** (how should the viewer feel now?) > **story** (does it move the story?) > **rhythm** (does it land at the
right moment?) > **eye trace** (where is the eye, and where will it be on the next shot?) > 2-D screen plane >
3-D space. A cut that is right emotionally can break the lower rules; never the reverse.
([No Film School](https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch),
[StudioBinder](https://www.studiobinder.com/blog/walter-murch-rule-of-six/); from Murch's *In the Blink of an Eye*.)
- **Eye trace for us:** place the next hero where the eye already is (Fitts's law). A word on the right third → the
  next photo's face near the right third, or a deliberate move that leads the eye across.

## 2. Our cutting rules
- **Cut on the voice and the music.** Lyric reels: cut on phrase starts from `lyrics.json`; words land on their
  syllable. Documentaries: beats keyed to narration word times (`audio/cues.py`).
- **Flurry, then breathe.** Fast bursts (3–6 frames a shot) as punctuation at an opening or a turn; then long holds.
  Rapid photo changes get a short sound on each change (reel 2).
- **The first frame already shows something** (Doherty threshold); the idea is clear in the first two seconds; open on
  the subject or the first sung word, never a slow title card.
- **Overlap scenes** so the next is arriving as the last one leaves; no near-blank moments (check contact sheets at
  ~2.5 s spacing).
- **Split edits** (J-cut: next sound starts before its picture; L-cut: sound carries over the next picture) hide the
  seam. Use J-cuts most: sound leading the picture feels natural — e.g. the singer's voice arriving under the last
  narration image ([Adobe](https://www.adobe.com/creativecloud/video/discover/j-cut-and-l-cut.html),
  [Epidemic Sound](https://www.epidemicsound.com/blog/j-cuts-and-l-cuts/)).
- **Final singing clip:** one smooth continuous move into it (slow, then fast), never appear–pause–zoom; the voice
  arrives ~0.5 s after the narration ends.
- **Ending:** land on a held note or phrase end, then the logo for 1.5–2.5 s, silent, no echo tail.
- **Single-clip music edits are not montages:** no extra clips, no intrusive effects; the artistry goes into type and
  frame (BaeedAnak style).
- **Accent transitions stay rare** (a few per film); most cuts are hard cuts or carry-overs.

## 3. Rhythm across a 60 s documentary
Hook (0–5 s: one strong image and line) → origin → turning point(s) → peak (silence before it, then the artist's real
voice) → legacy and name → logo. Change scene roughly every 4–8 s; let the peak breathe longer. Details of story
structure: `../documentary/storytelling.md`.

## 4. Before showing
Contact sheet of the render; first and last two seconds at full size; every cut checked against emotion → story →
rhythm; nothing important outside the safe area; say plainly what wasn't verified (sync by ear, phone view).
