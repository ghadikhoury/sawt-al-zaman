# The owner's reference reels

Files: `references/refNN_<id>.mp4` in this folder (downloaded from public Instagram links, 2026-11-17).
Per-reel data in `references/analysis/`: `refNN_..._sheet.jpg` (36 frames across the reel), `refNN_....json`
(cut times, and for four reels Gemini's description of picture and sound; three calls failed and were not retried).
`references/analysis/analyze.py` regenerates all of it (check its input paths first; the reels moved here 2026-11-18). Notes below are from looking at the frame sheets; sound was not heard.

Use these to understand *why* something works. Do not rebuild any of them.

| Ref | What it is | Format | Cuts | What to learn from it |
|---|---|---|---|---|
| 01 `DeWqcPBADIA` | A presenter talks about Umm Kulthum over Cairo night b-roll | landscape in a rounded frame, 34 s | flurry of 12 cuts in the first 1.6 s, then one every 2–3 s | One calligraphic word at a time, centred, gold on dark shots and black on light ones. Archive photo of Umm Kulthum cut out, given a painted look and placed over new city backgrounds. Colour and black-and-white alternate. The opening flurry then calm is a reusable shape |
| 02 `Dfud8tUKl8H` | Fairuz archive collage with a spoken text | 4:3 image band on black, 14 s | very fast at the start (25 cuts in 3 s), then slow | Picture on top, type below in bands: Arabic, English, Turkish, each with its own face and size. Magazine covers, records and photos as collage. Grainy high-contrast black-and-white |
| 03 `DfkLS5TIuDV` | Poem as kinetic typography over cinematic b-roll | landscape, letterbox strip that opens, 47 s | slow (about one cut per 4 s) | The richest type lesson: kashida stretching, thin outlined words against heavy solid ones, one red accent word, phrases built up and rearranged, full black frames with only type, words overlapping. Teal-and-orange grade |
| 04 `Dfx3Akhxtrp` | Umm Kulthum "أنا في انتظارك" over the Alexandria seafront | landscape, rounded frame, 27 s | medium, quicker at the end | Orange calligraphy written on over teal sea. Words placed around the subject in each shot. A held "نااااري" drawn out with repeated letters. Repeated "يا ريت" set differently on every cut |
| 05 `DcjZx8MsraL` | A spoken idea illustrated with a bow and arrow | vertical, 16 s | medium | Minimal: a tiny square picture on white that opens to full frame, hard black-and-white, tiny text. Literal images for abstract words. Shows how much a frame change alone can do |
| 06 `Dduf_x9I3La` | George Wassouf lyric edit (closest to this brand's subject) | landscape, 31 s | bursts of 3–4 very fast cuts between long holds | Chrome-filled calligraphy, a word behind his head, photo collage built on the beat, RGB glitch frames as punctuation, a Nokia phone screen typing the lyric, an old-TV vignette with small subtitles, switching between colour and black-and-white per section. Each 4–6 s section has its own device |
| 07 `DeAcVTcMFNW` | Umm Kulthum "أنا في انتظارك" over Homs streets | landscape, 42 s | slow, then a fast run of cuts for the repeated line | Golden vintage grade. Text following the perspective of buildings, stretched along a facade, inside a round street mirror. "يا ريت" repeated on each cut in a new colour and face. Zoom-blur and an overexposed flash between shots. Lines stacking up at the end |

Sound, from Gemini on refs 02, 04, 05, 06 only (unverified): voice or song leads; cuts and text hits follow its phrasing;
glitch sounds accompany glitch frames; impacts mark emphasised words; vinyl or tape texture underneath.

Earlier reference (motion captions on a talking video, English): `instagram.com/reel/DdGs8HcRd6j` — mixed sans and italic
serif, a coloured emphasis word, large words placed behind the speaker.

## The three "premium" references (2026-11-18): `references/premium_*.mp4`
| File | What it is | What he liked | What he didn't |
|---|---|---|---|
| `premium_DfMiYjYRbMI` (reel 1) | English talking-head "captions" edit, warm room | Text behind his head, orbiting his head, a ribbon wrapping behind then in front; text coming from outside the screen; words shuffling, leaving one by one; bold + italic-serif mix; seamless minimal glow; sound only on what to focus on | Text stuck to the wall, glowing letters, big white capitals |
| `premium_DeboEc9nR2V` (reel 2) | Arabic motivational edit with rapid archive images | The font (The Year of the Camel: stretched opening, yellow typed text); rapid photo changes with a sound per change; background photo + smaller main photo changing on their own | — |
| `premium_Dc9DiPQos4e` (reel 3) | Arabic edit over paintings and archive | Subtle glow on big words at the start; aspect-ratio change; red word in front of a white word behind | Its big fonts |
Frame-level analysis of reel 1 (timings, orbit geometry, sound) and what we take or leave: [premium_DfMiYjYRbMI_analysis.md](references/premium_DfMiYjYRbMI_analysis.md).
His full analysis in plain words: `../design/premium-look.md`. A copy of these three for Gemini: `Downloads/premium_references_for_gemini.zip`.
Wassouf reel (`ref06`) also gave: letters as a window, photo pop-up collage, sliding stripes (his screenshots in `../text/examples/`).
