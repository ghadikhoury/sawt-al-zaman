# Sawt Al-Zaman · صوت الزمان

Open-source tools for putting **timed lyrics on classical Arabic music**: old recordings of Umm Kulthum, Fairuz,
Abdel Halim Hafez, Wadih el Safi, Warda and the other voices of the golden age.

I built this for my Instagram brand, Sawt Al-Zaman, which posts short vertical videos of these songs with the words
on screen as they are sung. Doing that by hand takes hours per clip, and the usual speech-to-text tools fail on this
music. This repository has three parts:

| Folder | What it is |
|---|---|
| [`lyrics_pipeline/`](lyrics_pipeline) | Turns a clip of an old Arabic song into a timed lyrics file: every line and every word with its start and end time |
| [`remotion-fx/`](remotion-fx) | Text and transition effects for [Remotion](https://www.remotion.dev) (video made with React): letters as a window onto the footage, a photo pop-up collage, a sliding push with motion blur |
| [`skills/`](skills) | Five [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) that hold the brand's design, typography, motion, sound and documentary rules, so an AI agent edits in one consistent style |

## The result

| | Words right and on time |
|---|---|
| Before: general speech-to-text on these recordings | **about 20–25%** |
| Now: this pipeline, when the song is known | **91% of lyric lines correct** |

*How it was measured:* the output was compared with the lyrics shown on 10 reels I had already posted and checked by
hand. The song's name was known: either found by the pipeline or given by me. Finding the song from the audio alone is
much weaker (it named about 4 songs in 10 correctly), so the pipeline asks a person when it isn't sure. The
measurement is small and some of those reels were used while building the pipeline; a larger test on 40 reels that
were set aside from the start (`lyrics_pipeline/eval/split.json`) hasn't been run yet.

## Why Arabic is the hard part

Most lyric and caption tools are built for English pop. Classical Arabic recordings break almost every assumption
they make:

- **Written Arabic leaves out most vowels**, and the same word is spelled several ways across lyric sites and
  dialects (أ/إ/ا, ة/ه, ى/ي and more). "Is this the same line?" can't be an exact text match.
- **Formal Arabic and dialect mix in one song**, and speech models trained on news Arabic mishear sung Egyptian or
  Lebanese words.
- **Tarab singing stretches one syllable over many seconds** (a held note, or melisma). Timers mark the word where
  the note ends, so captions appear late.
- **Singers repeat lines, half-lines and single words, go back, and improvise.** The printed lyrics are not what is
  sung, so the captions have to follow what is actually heard.
- **The recordings are old**: mono, hiss, a full orchestra, and often a live audience.
- **Very little labelled data** exists for sung Arabic, so there is no off-the-shelf model to fine-tune from.
- On screen, Arabic is **right-to-left with letters that join**, so splitting a word for animation can break it
  (see `skills/sawt-text/arabic-script.md`).

## Tools: before and after

**Before (what fails on this music):**
- **Whisper large-v3** (OpenAI's speech-to-text) on the full mix: got only about a quarter of sung words right, and
  invented filler phrases over the music.
- **An Arabic fine-tuned Whisper**: worse; it invented words and merged phrases. Removed.
- **Whisper forced alignment alone** (giving it the lyrics and asking only *when*): drifted by seconds across
  instrumental breaks and marked held words late.

**After (what this pipeline does):**
1. **Listen:** Google **Gemini** hears the audio only (never the on-screen text) and writes the words it hears with
   rough times. This is the backbone of the "sung script".
2. **Find the song:** a fuzzy search over a local catalogue of song lyrics (character-trigram TF-IDF, tolerant of
   Arabic spelling variants). If that's not convincing, the AI agent (**Claude**) names the song from the heard words,
   and if it is still unsure, it **asks a person**. A wrong caption is worse than a question.
3. **Build the sung script:** what was heard, in the order it was sung, repeats included, spelled from the official
   lyrics (sources such as [LRCLIB](https://lrclib.net)). Claude reviews this file.
4. **Separate the voice** from the orchestra with **Demucs** (`htdemucs`).
5. **Time every word by vote:** the median of four independent estimates:
   - a letter-level aligner (**wav2vec2 XLS-R Arabic**, CTC; it finds where a word's first sound is);
   - **Whisper large-v3 forced alignment** through **stable-ts** / **faster-whisper**, each phrase in its own window;
   - free Whisper transcription of the isolated voice;
   - Gemini listening to each line's few seconds.

   Each timer is wrong in its own direction on held notes; the median cancels that.
6. **Refine:** find stretches of singing that no caption explains (a missed repeat or an ad-lib) and lines placed
   where nobody sings. These are only *suggested*; when applied automatically they were mostly wrong.
7. **Preview:** burn the timed words onto the clip with ffmpeg to watch whether they land.

The output is `lyrics.json`: `{title, artist, lines: [{start, end, text, conf, status, words: [{w, start, end}]}]}`,
ready for any editor. The Sawt Al-Zaman videos read it straight into Remotion.

## Running the lyrics pipeline

You need Python 3.10+, [ffmpeg](https://ffmpeg.org) on your PATH, an NVIDIA GPU for Whisper and Demucs at a
reasonable speed, and a Google Gemini API key (the free tier works; about 20 calls a day on the better models).

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=...            # Windows: set it as a user environment variable
cd lyrics_pipeline
python lyrics.py go path/to/clip.mp4
```

`go` runs every step and stops with instructions when the song isn't settled. The steps can also be run one at a
time (`hear`, `find`, `song`, `script`, `time`, `refine`, `preview`); `python lyrics.py --help` lists them. Each clip
gets a folder in `projects/` (or wherever `LYRICS_PROJECTS` points) with every intermediate file, and you can edit
`script.json` by hand and run `time` again.

**The song catalogue isn't included,** because it contains copyrighted lyrics. Build your own as
`lyrics_pipeline/catalog/songs.jsonl`, one song per line:

```json
{"title": "ثورة الشك", "artist": "أم كلثوم", "url": "https://…", "lines": ["أكاد أشك في نفسي", "…"]}
```

Or skip the catalogue and pass the lyrics yourself:
`python lyrics.py song clip.mp4 --lyrics lyrics.txt --title "…" --artist "…"`.

`eval/score.py` scores a run against lyrics you already know are right. It is for measuring only and is never used as
input.

## The text effects

`remotion-fx/TextFx.tsx` is one file with no dependencies beyond Remotion. Copy it into a Remotion project.

- `TextWindow`: the letters are a window onto moving footage or a photo, with a soft rim. Keep the inside untinted.
- `PhotoPop`: photos pop in full-frame one after another every 2–3 frames, then leave in reverse.
- `SlidePush`, `Smear`: one scene pushes the next off-screen with a directional motion blur.
- `Drift`: a slow move across a still.
- `flickerFont`: a word flickers through a few fonts as it lands.
- `ColourSplit`, `Flash`, `SplitWord` are kept for reference but are not used in the brand's style (glitch and colour
  fringes read as cheap).

## The skills

Each folder in `skills/` is a Claude Code skill: a `SKILL.md` with a description that tells the agent when to load
it, plus reference pages. They show one way to give an AI agent a creator's taste: every rule comes from a real
verdict on a real video ("liked", "too fast", "banned"), and the owner's verdicts outrank generic advice.

- `sawt-design`: palette, layout for 1080×1920, grading black-and-white archive footage, twenty principles to check
  every frame against.
- `sawt-text`: Arabic typography, pairing a bold and a thin font, how words arrive and leave, letters as a window.
- `sawt-motion-edit`: easing and timing, transitions, pacing, music sync, the production checklist.
- `sawt-sound-voice`: sound-design levels and timing, mixing to −14 LUFS, Arabic narration.
- `sawt-documentary`: a one-minute artist documentary from research to delivery, with Arabic storytelling principles.

To use them, copy a folder into your project's `.claude/skills/`. They mention files from the private production
setup (footage, reference reels, font files) that aren't in this repository; adapt the paths and the taste to your
own brand.

## Not included

Songs, footage, archive photos, finished videos, other creators' reference reels, paid font files and the lyrics
catalogue are not here. They aren't mine to share. Fonts the skills mention are listed with sources in
`skills/sawt-text/fonts.md`.

## Contributing and contact

Use any of this freely. I'll keep improving it and adding layers, such as better song identification from audio,
timing for improvised passages, and a reusable caption template. Issues and pull requests are welcome. If you work on
Arabic music, audio or captioning and want to talk, open an issue or message me (Ghadi Khoury) on
LinkedIn.

## Licence

Code: [MIT](LICENSE). Written guides in `skills/`: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
(reuse with credit). The models and services used (Whisper, Demucs, wav2vec2, Gemini) have their own licences and
terms.
