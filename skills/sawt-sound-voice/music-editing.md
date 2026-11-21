# Choosing and editing the music (the owner's recordings of classic songs)

## 1. Choosing which part of the song plays where
The owner said: you may want "certain versions at certain times; you deal with that". Choose by **structure** and
**mood**:
- **Structure of a classic tarab song:** an instrumental introduction (*muqaddima*), often a free-rhythm instrumental
  improvisation (*taqsīm*) or a sung one (*mawwāl*, no metre), then sung sections (*maqṭaʿ*) with instrumental
  refrains (*lāzima*) between lines, each line closing on a cadence (*qafla*) where the audience responds.
  - Under narration: the introduction, taqsīm or a lāzima (instrumental, no voice) — or the Demucs instrumental stem.
  - For the finale: a sung line that ends on a strong qafla, so the film ends on a cadence, not mid-phrase.
  - A quiet taqsīm suits the tender or sad parts of a life; a rhythmic refrain suits a rise, success, a journey.
- **Mood of the maqām (the mode)** — traditional associations, loose and debated, useful as a hint:
| Maqām | Traditional character | Fits in a life story |
|---|---|---|
| Rast | pride, strength, clarity | a rise, a confident beginning |
| Bayātī | warmth, tenderness, vitality | childhood, home, love |
| Sīkāh | nostalgia, old times, devotion | memory, the past, legacy |
| Ṣabā | sadness, pain | loss, illness, farewell |
| Ḥijāz | yearning, longing, the desert | exile, separation, distance |
| ʿAjam | brightness, joy | success, celebration |
| Nahawand | drama, emotional extremes | a turning point, conflict |
| Kurd | gentleness, romance, freedom | romance, a gentle ending |
Sources: [Fiveable: maqam system](https://fiveable.me/world-music/unit-3/maqam-system-modal-structures-middle-eastern-music/study-guide/UPlMYlC0zxLWO86J),
[USC Scalar: traditional music in the Arab world](https://scalar.usc.edu/works/music-in-global-america/traditional-music-in-the-arab-world.109)
(sources stress there is no consensus; trust the actual recording's feeling first).

## 2. Editing music invisibly
- **Cut on phrase boundaries** (whole phrases of 4 or 8 bars, or a full qafla); never mid-phrase, never mid-word of
  the singer ([Artlist](https://artlist.io/blog/?p=1289)).
- **Crossfade** at the join: equal-power, ~1.2 s for sections; shorter (50–200 ms) only at a hard transient.
- **Shorten** by removing whole repeats or a lāzima, not by trimming notes.
- **Hide the owner's seeks:** `find_jumps.py` finds them; cut around them on a phrase boundary or use only clean parts.
- **Check by measurement** (the agent can't hear): no level step at the join, the spectrum continuous, beats aligned
  across it (`life_cues.py` beats), then say it wasn't heard by ear.
- Final film: music starts with a short fade-in (0.2–0.4 s), ends on a cadence with a ~1 s fade, gone before the logo.
