# Colour: the brand palette, and grading classic Arabic music footage

## 0. Brand palette and the owner's colour rules
| Role | Name | Hex | Use |
|---|---|---|---|
| Main | Sand | `#E9C89F` | Text on dark, the Arabic account's mark |
| Main | Deep brown | `#1F0D0B` | Backgrounds, ink text on light |
| Secondary | Parchment | `#EED4B4` | Soft text, glow, light panels |
| Secondary | Champagne | `#DDB97C` | Accent words, fine lines (muted gold, **never bright gold**) |
| Secondary | Terracotta | `#A5603F` | Accent word, shapes; large text only on dark (3.9:1) |
| Secondary | Dusty rose | `#C79F8B` | Secondary text, quiet labels |
Machine-readable: `Brand Assets/palette.json`, `palette.css`. Full brand context: `Brand Assets/Sawt-Al-Zaman-Brand.md`.

- **Text is always in brand colours.** A brick red is fine sometimes ("similar" to terracotta). **No blue, green or
  maroon text.** Only one accent colour per frame.
- **Backgrounds may vary freely** within the warm brand range (the owner: "have some fun with it").
- Colour sets are a **brand** decision, not per video; per-video three-colour sets made films unclear.
- Real objects keep real colour: the Algerian or Egyptian flag stays its true colours.
- **No glitch colour:** RGB/red-blue split, solarised flashes, coloured fringes ("really bad for us").
- Light, not decoration: a faint warm glow (like a lit sign through haze), never a neon poster. One consistent grade
  and fine grain for the whole film; the owner calls this a baseline, not a feature.
- Liked: the **clarity step** (levels + large-radius local contrast) and the existing warm grade. None of the strongly
  toned looks fitted. Bright and legible on a phone; gloom only for a story moment (Abdel Halim's illness, then back).

Colour harmony in short: the picture stays quiet and warm so type can lead; contrast comes from light/dark more than
from hue; complementary colour is used only as one small accent, never as a scheme.

# Grading classic Arabic music footage

Most grading advice online is for modern colour cameras (log footage, skin tones, teal and orange). Our footage is
different: mostly black-and-white TV and film from the 1940s–70s, often a low-resolution copy or a screen recording,
sometimes faded colour film. These notes are written for that. Tool: `Tools\Remotion\prep\grades.py` (numpy, explicit
steps), ffmpeg filters, and the `ffmpeg-color-grading` skill for LUTs and curves.

## The order (never skip ahead)

1. **Repair** what the copy broke. 2. **Clarity**: levels and separation. 3. **Look**: one tone for the reel.
4. **Texture**: grain, halation, vignette. 5. **Check** with numbers and on a phone.
A look applied to unrepaired footage only makes the damage prettier. Most of the "wow, before and after" in good
edits comes from steps 1 and 2, not from the look.

## 1. Repair

- **Interlacing** (comb lines on movement, common in TV recordings): deinterlace first (`bwdif`).
- **Compression blocks and screen-recording smear**: light deblock and denoise (`hqdn3d` light, or `nlmeans`). Denoise
  removes digital noise; we add real-looking film grain back later. Never denoise to plastic.
- **Flicker** (brightness pumping between frames): `deflicker`. Old prints and telecines flicker.
- **Shake / gate weave**: stabilise only if it distracts. A little weave is part of film.
- **Upscaling**: Lanczos plus a large-radius, low-amount sharpen. AI upscalers and face restorers (GFPGAN, CodeFormer)
  repaint faces; they would change Umm Kulthum's face, so do not use them on her. AI colourising (DeOldify and others)
  is a no: invented colours on a real person look fake and disrespect the archive.

## 2. Clarity (what makes black-and-white look "clearer")

Black-and-white has no colour to separate things, so all clarity comes from **tonal separation**:
- **Black and white points.** Old copies sit grey: the darkest point is not black, the brightest not white. Stretch
  them (`clarity()` in grades.py: 0.5% to black, 0.4% to white). Keep detail in her hair and dress (no crushed blacks)
  and in the curtain highlights (no clipping).
- **The face first.** Her face is the subject. In black-and-white it should sit in the upper mid-tones (roughly 55–70%
  brightness). Grade for the face, then let the rest follow.
- **Local contrast, not sharpening.** A large-radius, low-amount unsharp mask (radius ~25–30 px at 1080 wide, amount
  ~0.3) separates her from the background. Small-radius sharpening makes halos on low-resolution sources.
- **Dodge and burn, the old darkroom trick.** Brighten the subject a little and darken the edges. We have her cut-out
  mask from the behind-text step, so we can lift her by 5–10% and lower the background: the most "cinematic" single
  move for archive footage. A vignette is the simple version.
- **Highlight roll-off.** Bright areas should fade into white softly, not clip hard (the `roll` setting).

## 3. Look

- **One look per reel**, chosen from the song's mood: silver (neutral, classic), warm print (nostalgia, the default
  for love songs), gold leaf (only the jewels and lights go gold: luxury), cyanotype (night, longing), faded archive
  (memory, documentary), duotone in the reel's colour set (poster style), oxblood shadows (drama).
- **Toning, not tinting.** A tint colours everything the same; toning colours shadows and highlights differently (cool
  dark, warm light, like a toned silver print). Toning looks like a photograph; tinting looks like a filter.
- **Keep saturation low.** A toned black-and-white image should still read as black-and-white. If you notice the colour
  first, it is too strong.
- **The picture stays quiet so the type can be loud.** The accent colour of the reel's colour set belongs to one word at
  a time, never to the picture.
- **Colour footage of the era** (Eastmancolor and similar films of the 1950s–70s): these fade towards magenta or red and
  lose blue. Correct the fade first (make whites neutral), then lower saturation slightly, then a print-film look
  (free Kodak 2383 print-emulation LUTs exist, e.g. Juan Melara's and Cullen Kelly's; check their licence). Keep skin
  natural. Do not push modern teal and orange onto it.

## 4. Texture

- **Grain** is the glue that makes repaired, upscaled footage feel like film again. Moving grain, strongest in the
  mid-tones, size matched to the source (coarser for small sources). Felt, not noticed.
- **Halation** (a soft red glow around bright lights) only where the footage has real stage lights or jewellery.
- **Avoid fake-vintage clichés**: heavy scratches, burn holes, sepia filters at full strength, constant jitter.

## 5. Check

- I cannot judge levels reliably by eye on a small still. Measure: the 0.5% and 99.5% brightness values, the face's
  average brightness, and a waveform (`ffmpeg -vf waveform`).
- Compare before and after side by side at full size, and on a phone at normal brightness. Instagram compression eats
  fine grain: check the uploaded result.
- Match every shot in a reel to the same black point, white point and face brightness before applying the look.

## 6. General grading order (industry consensus, matches ours)
Correct before you grade (exposure, white balance), match black and white points first, keep changes restrained (subtle
reads as professional), film emulation = highlight roll-off + contrast curve + grain as separate steps.
Sources: [No Film School grading guide](https://nofilmschool.com/color-grading-guide-2022),
[Storyblocks: colour grading 101](https://www.storyblocks.com/resources/blog/what-is-color-grading).
