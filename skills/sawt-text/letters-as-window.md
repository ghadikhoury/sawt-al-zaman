# Letters as a window ("hollow" moving text, the way the owner means it)

To the owner, "hollow" text means **something happening inside the letters**: the word is a window onto moving
footage or a moving photo. Never an outline that fills in (banned). He liked it in the Wassouf reel («فوق الخدود»,
«فوّق شفافك», «اه يا قمر») and in our test ("the effect is nice and it works"); the Umm Kulthum finale's window word was
also liked. Screenshots: `examples/liked_*`.

## 1. The core technique
The word acts as a **matte**: the picture shows only inside the letter shapes. In After Effects / Premiere this is a
track matte (alpha matte; luma matte if the text has no alpha) ([Adobe: track matte, video inside text](https://helpx.adobe.com/lt/premiere-pro/how-to/track-matte-video-inside-text.html),
[4K Shooters](https://4kshooters.net/2018/12/29/how-to-place-video-in-text-or-shape-in-after-effects-cc)).
In our code: `TextWindow` in `Tools/Remotion/src/fx/TextFx.tsx` — an SVG `<mask>` holding the whole word (so Arabic joins
stay clean), with any React node as the inside.

## 2. What makes it premium rather than a cheap template
- **The inside moves differently from the outside.** Use a *second copy* of the picture inside the letters, offset,
  slightly bigger (1.05–1.25×), or a few frames later, so as the camera moves the inside slides at its own speed
  (parallax). A matted clip can also sit over a *different* background video ([Adobe Community](https://community.adobe.com/t5/premiere-pro-discussions/how-can-i-place-a-video-inside-of-text-with-a-different-video-behind-it/m-p/14290612/highlight/true)).
- **The inside has its own treatment:** brighter or softer than the outside (the owner's liked looks); frosted glass
  (blur + lift + low saturation); chrome (contrast up, slight hue shift) used only on footage that suits it. The
  sand-tinted inside "didn't fit": keep tints off, let the picture be the colour.
- **A thin rim** (2–3 px inner edge made by eroding the word's alpha) gives the glass/metal edge; optional.
- **Liquid refraction:** a slight `feDisplacementMap` on the inside only, a few pixels, for glass. Never wobble the
  letter shapes.
- **Over a still photo:** the inside must move on its own (`Drift`: the same photo panning the other way, a slow
  push), or the window looks dead.
- **Readability:** a soft shadow under the word, or a slightly darkened outside, so the letters separate; heavy fonts
  only (BOLD group: The Year of the Camel ExtraBold, PT Bold Heading) — thin fonts show too little picture.

## 3. Ways to animate a window word
- **Reveal:** the window opens upward through a soft edge (`reveal`), or scales down from beyond the lens (move B1).
- **Swell-open exit:** the strokes thicken until the window fills the frame and becomes the next shot (liked, Umm
  Kulthum finale) — a transition, not just an exit.
- **Window inside a window:** the word holds still while the picture inside pushes in slowly.
- **Mix in a phrase:** one word as a window, the next solid (the owner liked solid and window words together).
- **Two pictures:** outside = the singer, inside = the place she sang about (or her younger photo).

## 4. Checks
Joins clean (mask the whole word, never letters); enough of the picture shows (heavy font, large size); the inside is
moving; nothing important of the face is lost behind the outside darkening; works on a phone.
