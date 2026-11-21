# Timing picture and text to the music

## 1. Map the song before cutting
Mark the large events first (where the voice enters, phrase starts, the qafla/cadences, section changes, the climax),
then smaller accents only where they help the story ([Artlist: editing music into video](https://artlist.io/blog/?p=1289)).
Listeners hear music in phrases of four and eight bars; a cut in the middle of a phrase feels wrong.

## 2. What to hit, and what not to
- **Scene changes on phrase starts or resolutions;** major visual changes on **downbeats** (the strongest beat of a
  bar); small accents (a word, a photo in a run) on beats or off-beats.
- **Don't cut on every beat.** Constant beat-matching becomes predictable and mechanical; hold shots across several
  beats and save hits for moments that earn them. Vary density with the music: relaxed in a verse (every other
  downbeat), denser where the music builds ([Sonilo](https://sonilo.com/blog/guides/how-to-make-video-sync-with-music),
  [Cursa: beat-based editing](https://cursa.app/en/page/beat-based-editing-in-capcut-syncing-cuts-transitions-and-motion-to-music)).
- **Anticipate:** experienced editors cut 2–3 frames early so the new image is already there when the hit arrives;
  a whoosh peaks on the cut, so it starts 6–10 frames before.
- **Follow the singer, not only the drum:** over vocals, motion flows with the line (a word appears as it is sung);
  hard hits belong to percussion.
- **Edits land on whole frames** (30 fps): round beat times to the nearest frame.

## 3. Arabic classical music specifics
- Much of tarab repertoire has **free-rhythm sections** (taqsīm on an instrument, a mawwāl sung without metre):
  there is no beat to cut to. Follow the phrase and the breath; hold images longer; let the text follow the voice.
- Metred sections run on an **īqāʿ** (rhythmic cycle: maqsūm, waḥda, malfūf, sumāʿī…). The strong strokes (dum) are
  the natural downbeats; cut on the start of a cycle.
- The **qafla** (the cadence that closes a phrase) is where listeners respond: the best place for a reveal, a cut to
  the singer, or the moment of silence before the voice (see `../documentary/storytelling.md` §3).
- Live recordings drift in tempo (rubato): beat grids from a model are a starting point; check them against the song.
- Choosing *which* part of a song plays where: `../sound-voice/music-editing.md` (sections and maqam moods).

## 4. Getting beats and phrases (tools)
| Need | Tool | Note |
|---|---|---|
| Beats in film time + music loudness per frame | `Sawt Al-Zaman/Projects/life_cues.py` (uses the project's `music_beats.json`, made with librosa) | already in every documentary's `cues.json` (`beats`, `env`) |
| Better beats **and downbeats** | **Beat This!** (CPJKU, open source; state of the art in 2024–25) or **madmom** DBN | librosa is simplest but weaker on rhythmic structure; downbeats need Beat This!/madmom ([Beat This! paper](https://arxiv.org/pdf/2407.21658)); not installed yet: ask before installing |
| Phrase boundaries | listen-free proxy: big changes in the music envelope + the singer's line starts (Whisper/lyrics timing) | confirm by eye on a waveform; mark them by hand in `cues.py` |
| Audio-reactive motion (things breathing with the music) | `env` from `life_cues.py`; or Remotion `useWindowedAudioData` + `visualizeAudio` (per-frame spectrum, 0–1 per band) | use the low band for pulse, smooth across frames; keep it subtle ([Remotion audio visualisation](https://remotion.dev/docs/audio-visualization)) |
| Stems (drums vs voice) to drive different elements | Demucs `htdemucs_ft` | voice stem → gentle text motion; percussion → small hits |

## 5. Rules of taste for music sync (owner's)
Sync is a seasoning: words or photos landing on the music feel premium when it's occasional and meaningful (the
rapid photo run with a sound per change, a name landing on the final downbeat); a whole film pulsing to the beat reads
as a template. No effects over foreground singing; the music staff lines in Baligh breathing with the music (`env`)
were liked as a quiet example.

## 6. Lesson from test reel 2 (2026-11-18): verify the beat grid before trusting it
In M1 the words were placed on librosa's beat times from Warda's live recording and **none landed on the beat** to
the owner's ear. Likely causes: librosa's phase/tempo was wrong on a live, rubato recording; every-second-beat picked
the off-beats; and nobody checked the grid against the audio. Before syncing anything:
1. Get beats **and downbeats** from a stronger model (Beat This! or madmom; ask before installing), or from onsets of
   the percussion stem (Demucs drums/other) rather than the full mix.
2. **Check the grid visually:** plot the waveform/onset strength with the beat lines for the section used; the lines
   must sit on the transient peaks. Shift the whole grid if it is consistently early/late.
3. Prefer the **phrase and the singer's line** for text (a word arrives as a sung phrase starts, holds through it);
   use beats only for photo runs and small accents.
4. Say plainly that sync was checked by plot, not by ear.
The owner's wish: text should *fit* the background music (feel part of it), not necessarily land on every beat.

**Second failure (test reel 3):** words placed on onset-detected accents (checked on a waveform plot) were again
"totally off". Plot-checking without hearing isn't enough. Next time: suspect a timeline offset first (the music clip's
start vs the composition, fades, the audio-only Sequence); render a 5 s check with a visible flash on each claimed
accent and ask the owner (or Gemini) to confirm sync before building text on it; or time text to the singer's phrases
instead of percussion.
