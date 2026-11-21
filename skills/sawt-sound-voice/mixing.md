# Music, sound effects and the mix

## 1. The owner's rules
- **No bed under the whole film** (hum, drone, room tone). The safelight hum in Abdel Halim v1 was "fridge-like".
  Every sound starts and stops with something on screen.
- **Sound effects are for attention:** a short click, tick or whoosh only on what the viewer should look at (a word that
  matters, a photo change in a rapid run). Most motion is silent. They fit when the music is a background bed (under
  narration, in a busy edit).
- **No effects over foreground singing** (the singer's own voice opening or closing the film, a reveal). The animation
  continues, silent.
- **No sound on the logo** (a ding felt gimmicky), no echo tail under it.
- **Keep every effect short.** Long swells, rustles and multi-second beds were too long.
- **Music a notch lower than first instinct** (Fairuz v1 was too loud); the rises and dips were good.
- **Clean the owner's music.** His files are phone screen recordings; he seeks forward/back, so they contain jumps. Find
  every jump and hide it (cut on a phrase boundary with a short crossfade, or use only clean sections). Choose which
  versions or sections of the recording play where. A viewer must never hear an edit.
- **Bring the singer's voice in soon after the narration ends** (~0.5 s), not after a wait.

## 2. Levels and movement (numbers that worked)
- Music under narration sits roughly 18–24 dB below the voice in loudness terms (industry range: −18 to −25 dB;
  measure the gap in LU, not peaks); louder when no one speaks. Our mixes: music RMS = narration RMS − 3 dB before the
  duck, then a smoothed duck of about −9 dB while the voice speaks.
- **Glide every move:** hold the duck through short pauses and smooth it (~0.6 s); level changes over 1.5–2.5 s; stem
  swaps (full ↔ instrumental) as equal-power crossfades of ~1.2 s; cover a song's own silent gaps with narration.
- **Instrumental under the voice, vocals for the finale:** separate stems with Demucs (`htdemucs_ft`) when the song
  has singing where the narration speaks; bring the full mix in for the ending.
- **Final loudness:** two-pass loudnorm to **−14 LUFS**, true peak −1.5 dB (platforms normalise anyway; consistency
  and clean headroom matter most). Gentle tanh limiting before loudnorm.
Sources: [Overseer: music volume under voice-over](https://www.overseeros.com/blog/background-music-volume-under-voiceover),
[Vidpros: music too loud](https://vidpros.com/fix-background-music-too-loud-video/),
[Salford/AES: background ducking for clear speech](https://salford-repository.worktribe.com/output/1371938/background-ducking-to-produce-esthetically-pleasing-audio-for-tv-with-clear-speech).

## 3. Tools
| Tool | What it does |
|---|---|
| `Sawt Al-Zaman/Projects/find_jumps.py <music.wav>` | Finds seeks in screen recordings (spectral change + drop-outs); prints candidates |
| `Sawt Al-Zaman/Projects/life_mix.py` (`Mix` class) | Segments with equal-power joins, gliding level curve, short library SFX, narration duck, −14 LUFS finish |
| `Sawt Al-Zaman/Projects/life_cues.py` | Cue times from narration words; music envelope and beats in film time |
| `<project>/audio/mix.py` | Each film's mix script (e.g. `baligh_life`, `warda_life`, `wadih_life`) |
| `Tools/external/motion-graphics/skills/sound-effects/sfx` | CC0 effects library used by `life_mix.py` |
| `Tools/sfx` | Older synthesised kit (glitch/tape-stop sounds there are off-brand now) |
| Demucs `htdemucs_ft` | Vocal / instrumental stems |
Run audio scripts with the TTS venv Python (`Tools/tts/.venv`).

## 4. Checks
Loudness reads −14 LUFS; scan the mix for clicks and sudden level jumps; listen-free check for audible music edits
(run `find_jumps.py` on the final mix too); Whisper on the final narration hears every word. The agent can't hear:
say what wasn't verified by ear.
