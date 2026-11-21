# Sound design: which sound, when, how long, how loud

The owner's rules come first (`mixing.md` §1): sound marks attention; nothing over foreground singing or on the logo;
everything short; no beds. Below is how to apply them precisely. Numbers are starting points from practice and
industry heuristics; **always check by measurement and on a phone speaker**.

## 1. The hierarchy (what the ear should follow)
1. **The voice** (narration, or the singer when the singing is the foreground): always the reference and always clear.
2. **Music:** carries emotion; sits under the voice, rises when no one speaks.
3. **Sound effects:** punctuation for the eye's key moments. If an effect is the first thing you notice, it's too loud.
Silence (or near-silence) is a fourth tool: a breath before the peak, a pause after a cadence (tarab's *qafla*).

## 2. Relative levels (measure as short-term loudness, LU relative to the narration)
| Layer | Under narration | When no voice speaks |
|---|---|---|
| Narration | **0 LU** (reference; final mix −14 LUFS integrated) | — |
| Music bed | **−18 to −24 LU** below the voice (our duck: ~−9 dB on a bed already set ~3 dB under the voice) | −6 to −10 LU below where the voice sat; full level for the finale / singing |
| Whoosh / swish (transition) | 12–18 dB below narration peaks | 6–10 dB below the music |
| Tick / click / shutter (photo change, word hit) | 18–24 dB below narration peaks; felt, not heard | 12–18 dB below the music |
| Soft impact / low hit (a reveal, a year landing) | only in narration gaps; 8–12 dB below where the voice would be | 6–10 dB below the music |
| Paper / page / pen foley (diegetic small action) | 16–22 dB below narration | 10–16 dB below the music |
| Riser / swell | almost never (owner: long swells too long); if used, ≤1.5 s, 12 dB+ below music | — |
Duck effects ~3 dB more while the voice speaks (`life_mix.py` `fx_duck`). `life_mix.py` `sfx(..., g=-24)` is the
default gain for library effects; tune per effect against this table.

## 3. Durations (keep everything short)
| Effect | Length | Note |
|---|---|---|
| Tick / click / UI tap | 30–120 ms | a single transient |
| Shutter / snap for a photo change | 80–200 ms | in a rapid run, every change or every second change, varied |
| Whoosh / swish | 200–600 ms | its peak lands on the cut or the fastest frame of the move |
| Soft impact | 300–800 ms | trim the tail; fade the last 80 ms (`maxdur` in `life_mix.py`) |
| Foley (paper, pen) | ≤700 ms | match the visible action length |
| Anything over 1 s | avoid | the owner found multi-second sounds far too long |

## 4. Timing to picture
- The transient lands **on the exact frame** of the visual event (a photo appearing, a word landing). A whoosh starts
  6–10 frames before the cut so its peak hits the cut.
- **Motion maps to sound:** fast lateral swipe/push → short whoosh; zoom-in reveal or a big word landing → low soft hit;
  photo snapping in → tick or shutter; pen line drawing → quiet pen scratch for its length; page or card → paper flick.
- **Pan follows motion:** a push from right to left pans its whoosh slightly right → left (pan ±0.2–0.4).
- **On the beat when possible:** photo-change ticks and cuts aligned with the music's beats (`life_cues.py` writes
  beats in film time).

## 5. Restraint and variation
- **Not every transition, word or zoom gets a sound.** Pick the moments the editor wants the viewer to notice (the
  owner's reading of the premium reels). Typical 60 s documentary: 4–10 short effects in all.
- **Never the same sample on every cut;** vary the sample, or its pitch ±1–2 semitones and level ±2 dB.
- **Leave the first words of each narration line clear;** no effect under the first syllable.
- **Effects stop before foreground singing starts** and never sit on the logo.

## 6. Making effects read on phones
Phone speakers have little bass: an effect needs midrange presence (a short mid "zip" plus a light airy tail beats a
long low cinematic whoosh). High-pass effects ~120–200 Hz so they don't muddy the voice; keep them out of the voice's
1–4 kHz band where possible (or duck them there). Check the final mix on a phone speaker.

## 7. Music choices inside the mix
- Use the instrumental stem under narration when the recording has singing there; the full mix (with voice) for the
  finale.
- Cut music on phrase boundaries; crossfades ~1.2 s equal-power; never an audible seek or jump.
- A beat of near-silence (music dipped, no narration) before the artist's own voice gives it its power.
Sources: [SFX Engine: sound design tips](https://sfxengine.com/blog/sound-design-tips-for-video-editors),
[SFX Engine: common sound design mistakes](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing),
[Cursa: sound design for small speakers](https://cursa.app/en/page/sound-design-that-reads-on-small-speakers),
[Adorama: audio levels](https://www.adorama.com/alc/?p=118366), [Overseer: music under voice-over](https://www.overseeros.com/blog/background-music-volume-under-voiceover).

## 8. Sound for emotion (tension, release, silence)
- **Silence is the strongest effect.** A brief drop to near-silence before a peak makes what follows feel louder and
  bigger even at the same level; the most emotional moments often sit in near-silence. Our use: narration ends, a
  breath, then the artist's voice (the qafla moment).
- **Build → release.** If a build is used at all, it's the music doing it (a rising section), or at most a very short
  soft swell whose peak lands exactly on the hit; a riser that misses the downbeat makes the release limp.
- **Density follows emotion:** fewer sounds in tender moments, slightly more in a lively run (a rapid photo sequence);
  never a constant layer.
Sources: [SFX Engine: risers](https://sfxengine.com/blog/risers-sound-effects),
[Violet Recording: sound design for trailers](https://violetrecording.com/sound-design-for-trailers/),
[C&I Studios: mixing for emotional impact](https://c-istudios.com/audio-mixing-for-emotional-impact-turning-sound-into-storytelling/).

## 9. Observed in the owner's premium reference (frame analysis, 2026-11-18)
More than half the text moments had **no sound**; effects marked impacts, transitions and visual state changes; most
lasted 0.1–0.25 s; whooshes led their cut by ~0.1 s. The music **dropped out briefly before a key moment and came back
on the beat**. Music sat ~12–15 dB under the voice there (a beat-driven talking edit); our documentaries keep music
lower (18–24 dB under the narrator). Details: `../motion-edit/references/premium_DfMiYjYRbMI_analysis.md`.
