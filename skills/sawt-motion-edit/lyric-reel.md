# Lyric reels: the artistic music edit (one song clip, the lyrics are the design)

Distilled from seven reels the owner loves (`references/ref01–07`) and his notes on BaeedAnak v1/v2. Learn the
principles; never rebuild a reference.

## Method
1. **Lyrics first.** Run the lyrics pipeline (root `README.md`): sung script with word times, repeats included. Every
   decision hangs on which word is sung when and how long it's held.
2. **One idea** in a sentence ("each word is ink on the city she sang about", "an old phone types the song"), plus
   three or four supporting devices. More reads as a template pack (BaeedAnak v2: ~15 devices in 50 s = "AI slop").
3. **Picture:** the singer's footage, b-roll of the lyric's mood (sea, streets, night city; ask where b-roll may come
   from), archive photos, or type on dark. Never pull other creators' footage; archive photos can be treated (cut out,
   placed over new backgrounds, one grade) so they sit in one world. A single-clip edit is **not a montage**: no extra clips or intrusive effects;
   the artistry goes into type and frame.
4. **Type system:** one BOLD + one THIN font (`../text`), one accent colour, rules for which words get which treatment.
5. **Beat plan:** one row per sung phrase: time, words, picture, frame shape, type treatment, entrance, sound accent.
6. **Stills before motion** (6–10 key frames as posters; two or three directions when the brief is open).
7. **Animate, then check** (production.md checklist).

## What the loved references share
- One thought on screen at a time: one to three words, large.
- Text is *placed*, not centred by default: in the empty part of the shot, behind a head or a tower, along a wall's
  perspective, inside a shape (a mirror, a phone screen).
- Contrast inside a phrase (bold beside thin, small above huge, one accent word).
- Rhythm from the voice: words on the syllable, cuts on phrase starts, fast flurries only as punctuation.
- One strong grade for the whole piece; texture (grain, rounded frames, letterbox strips) makes it feel hand-made.
- Restraint in transitions: mostly hard cuts.

## Devices for lyric reels
- **Captions as sung:** each word at its start; repeated words repeat on screen; a repeat is a chance to show the word
  in a new size, font or place (يا ريت on every cut).
- **Text behind the singer:** the big word spans from one side of the head to the other, head in the middle; only for
  the strongest one or two words, and it leaves. (In v1 it was too small, one-sided, on all the time, slipping.)
- **Held notes:** a word set already stretched with tatweel, or opening around the head (`OpenBehind` in
  `Tools/Remotion/src/BaeedAnakV2.tsx`); don't animate the stretch itself otherwise.
- **Build a phrase in place:** earlier words stay, move or shrink as new ones arrive.
- **Written-on calligraphy** right → left at the pace of the sung word.
- **Letters as a window** onto the footage (the brown screen with one word as a window was the one thing liked in v2).
- **Frame as design element:** a letterbox strip that opens to full on a key word; rounded-corner frame; picture top,
  type bottom. Two or three frame changes a reel, each a transition on a musical change.
- **Black is a shot:** one word on deep brown gives the next image force.
- **Stacked translation:** Arabic large, English small beneath (English account).
Banned here too: glitch/RGB frames, white flashes as decoration, outline fill-ins, zoom-through exits.

## Sound in lyric reels
The song is the soundtrack. No effects over the singing when it's the foreground; at most a soft whoosh on a frame
change under an instrumental moment. Fade in 0.2–0.4 s, out ~1 s; cut before screen-recording UI sounds.
