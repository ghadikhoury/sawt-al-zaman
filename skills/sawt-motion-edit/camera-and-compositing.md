# Virtual camera, depth and cut-outs

The owner's top "premium" point is depth: text and shapes living *inside* the scene. This is the craft that makes it.

## 1. The virtual camera
- **Stills get camera life:** slow push, pull or drift. Professional pan-and-zoom on archive photos stays restrained,
  about 5–8 % scale change per shot ([Shoots: Race to the Clouds](https://www.shoots.video/post/building-the-opening-of-race-to-the-clouds/)).
  Move *towards* what matters (the face, the detail that tells the story: "introduce large stories through small
  details", Ken Burns).
- **Parallax** = the biggest single upgrade for stills. Split a photo into layers (subject cut-out, background, an
  optional foreground element) and move them at different speeds: background slowest, subject a little faster,
  foreground fastest. Fill the hole behind the subject with a blurred, content-aware extension or keep moves small.
- **Depth of field:** blur the far layer slightly (2–6 px) so the subject separates; never blur a face.
- **Camera across a board:** one big world (map, drawn landscape) and the camera travels between places on eased arcs
  (Umm Kulthum, Warda maps); zoom in log space so wide-to-close feels even (`WardaLife.tsx` `camAt`).
- **Aspect-ratio transition:** animate the frame's mask from a narrow strip to full frame on a musical or story turn,
  images moving throughout. Rare, intentional.
- **No constant shake, no zoom punches** between identical shots.

## 2. Cut-outs (separating the artist from the background)
Needed for: text behind the head, orbiting text, ribbons wrapping the body, moving the artist over new backgrounds.
- **Still photos:** a background-removal model (e.g. rembg / BiRefNet locally; check licence) → PNG with alpha; clean the
  edge (feather 2–4 px, no halo; erode 1 px if a light fringe shows).
- **Video:** SAM 2 via the `mg-object-separation` skill (masks per frame), or `@remotion/video-matting`
  (`.claude/skills/remotion-best-practices`, `video-matting.md`), or the tracked silhouette tooling in
  `Tools/Remotion/prep`. Output VP9 WebM with alpha, played with `<OffthreadVideo transparent>`.
- **Check the mask on the frames with the most movement.** If it slips, use the effect only where the subject is still.
- **Respect the archive:** no AI face restoration or colourising on real artists (it repaints their faces).

## 3. Layering recipes
- **Word behind the head:** background → big word → subject cut-out. The word comes **already stretched** (tatweel),
  wider than the head; two-thirds readable.
- **Orbit** (two tries rejected; reference geometry in `references/premium_DfMiYjYRbMI_analysis.md`: tilt 15–20°, words
  entering one by one from the back arc, back words 50–65 % scale / 50–70 % opacity / blurred, ~0.5 rev/s): an ellipse path in 3-D perspective around the head; draw the back half *before* the cut-out
  (dimmed, smaller, slightly blurred) and the front half *after* it; ease the rotation; mixed sizes along the ring.
- **Silhouette spawn:** the cut-out first shown as a glowing parchment silhouette, dissolving into the real image in
  ~0.13 s (a reveal for the artist's first appearance).
- **Text along the contour:** a line typed along a path hugging the cut-out's outline, timed to speech.
- **Ribbon wrap:** a ribbon path drawn in two pieces (behind the body, in front of it), switched where it crosses the
  silhouette edge.
- **Letters as a window:** `TextWindow` (`Tools/Remotion/src/fx/TextFx.tsx`), the inside a second copy of the picture.
- **Match the light:** soft shadow of the word on the background, a little grain over everything so layers sit in one
  world; blend modes `multiply` (ink on light), `screen`/`soft-light` (light on dark).

## 4. 2.5-D photo animation with depth maps
A depth model estimates how far each pixel is from the camera; the photo is then moved like a 3-D scene (true parallax
from one still). Tools: **Depth Anything V2** for the depth map; **DepthFlow** (open-source parallax shader, Python) or
**Parallax Maker** (cuts the photo into depth cards) to animate ([DepthFlow](https://pypi.org/project/depthflow/0.7.1),
[Parallax Maker](https://socket.dev/pypi/package/parallax-maker)). Neither is installed yet: ask before installing.
- **Failure mode:** "stretchy" artefacts where the depth map is wrong, worst at the edges of people; keep the camera
  move small and choose a trajectory that shows parallax without stretching ([Google Research: Cinematic photos](https://research.google/blog/the-technology-behind-cinematic-photos/?hl=en)).
- Old archive photos (soft, flat, grainy) give weak depth maps: prefer the cut-out + layers method (§1) for faces, and
  use depth parallax for places and groups. Never let a face warp.
