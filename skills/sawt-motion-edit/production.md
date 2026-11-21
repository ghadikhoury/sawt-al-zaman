# Production: Remotion, rendering, safe areas, export, checks

## Remotion (Tools/Remotion)
- Drive everything with `useCurrentFrame()` + `interpolate()` with easing, clamped both ends; springs only for a
  deliberate physical moment.
- Fonts: load through `src/fonts/library.ts` (`font("camelExtraBold")`); hold the render until fonts are ready
  (`delayRender` / `document.fonts.ready`). Text measured before fonts load is wrong; `@remotion/layout-utils`
  `measureText` / `fitText` size a word to a box.
- Video with alpha: VP9 WebM, `<OffthreadVideo transparent>`. Shared motion (push-in) on one wrapper so footage,
  behind-text and cut-out move together.
- Register compositions in `src/Root.tsx`. Effects toolkit: `src/fx/` (`TextFx.tsx`, `TextMoves.tsx`).
- Remotion's own skill: `.claude/skills/remotion-best-practices` (see its `remotion-markup` folder: Arabic text,
  video matting, transitions, light leaks, measuring text). Where it says to open Studio, render stills instead.
- Quick checks: `npx remotion still <Comp> out.png --frame=N --scale=0.5`; contact sheets with ffmpeg
  (`fps=1/2.5,scale=…,tile=…`).

## Frame and safe area (vertical reels)
1080×1920, 30 fps, H.264 MP4, AAC 48 kHz. Keep text and faces inside roughly x 60–990, y 220–1600 (Instagram covers
the top ~220 px, bottom ~320 px, right ~90 px; guides disagree). `--crf=18–20` is enough (Instagram recompresses);
grain is the first thing compression eats, so check the uploaded result.

## Low-resolution sources
Don't fight softness with heavy sharpening (halos). Grain, a gentle grade and a vignette make softness read as
vintage; upscaling beyond ~4× looks mushy, so frame wider or design a border area. Repair steps:
`../design/colour-grading.md`.

## Checklist before showing the owner
1. Words: every on-screen word correct (spelling, joins, diacritics), each at its start; repeats present.
2. Faces: the artist on screen at least every 15 s (documentaries); no crop through a face; photos not stretched.
3. Nothing important outside the safe area; nothing clipped at frame or mask edges.
4. Every still passes `../design/principles.md` and the layout self-check.
5. Contact sheet every ~2.5 s: no near-blank frames, no collisions, scenes overlap.
6. Sound: loudness −14 LUFS, no music jumps, no effects over foreground singing or the logo (sound-voice).
7. Whisper pass on narration films: every word heard as written.
8. Say plainly what wasn't verified (sync by ear, phone view).
