# Motion: how things move

Premium motion = physical, purposeful, brief (Apple HIG); motion carries meaning, it isn't decoration (Willenskomer,
*UX in Motion*). The owner's version: "every move has a reason and good timing"; ours used to feel "like a kid should
be watching this".

## 1. Physics of every move (the twenty principles in practice, see `../design/principles.md`)
- **Ease everything.** Arrivals: strong ease-out (fast start, long soft landing), e.g. `bezier(0.16, 1, 0.3, 1)`.
  Exits: ease-in, shorter than the entrance (exits need less attention: Material). Moves between two places:
  asymmetric ease-in-out. Never linear except for continuous drift.
- **Anticipation:** a tiny counter-move (4–8 px, 3–5 frames) before a big one.
- **Follow-through and overlap:** parts settle at different times (the frame after the photo; each word of a line in
  turn; offset/delay of 2–4 frames between siblings).
- **Arcs:** things entering from off-screen travel on a slight curve; camera moves across a board on arcs.
- **Timing:** snap in (6–12 frames), hold to be read, then leave. Duration scales with distance travelled.
- **Springs only for physical moments** (a word landing in front with a slight overshoot, box 8). Bouncy/playful
  springs are wrong for this brand.
- **One attention-grabbing move at a time.** If two things move, one is the hero and the other is quiet.
- **Camera life on stills:** slow push or drift 2–8 % over a shot; never a constant shake. See camera.md.

## 2. Liked transitions and devices (owner's verdicts)
Full list with code locations: [devices.md](devices.md). The headline ones:
- **Sliding push** with motion blur and vertical strips sliding at different speeds ("blurring is fine").
- **Photo pop-up collage**: hard cuts every 2–3 frames until the frame is full, then reverse out.
- **Rapid photo changes with a sound per change**; a big background photo and a smaller main photo on top changing on
  their own rhythms (reel 2).
- **Aspect-ratio change as a transition**: a narrow frame opening to a wider one while the images keep moving; it can
  pair with rapid photo changes. Not constant.
- **Carry-over element** (one element holds while the world changes around it); **small detail becomes the next
  hero**; whip pan; watercolour bloom; water drop into a wash; film-strip step on the beat; cross-out then circle;
  photos on a string; board journey and the line that travels; window word with swell-open exit.
- **Pencil-drawn / woodcut illustration** (Wadih's mountains, "I like this a lot"): carved line drawing, layered so
  text can sit behind a range.

## 3. Disliked / banned motion
Flashy zoom-through exits; the five lines climbing onto the oud (Baligh, "AI slop", the oud was backwards); the
film-strip carousel with stick-figure parents; the flat basic orbit; constant frame changing; glitch frames, RGB split,
colour fringes, solarised flashes; split-colour words; outline fill-ins; whole-film gimmick themes; bouncing,
rotating every word; transitions between every shot (accents must stay rare to feel special).

## 4. Motion and sound
A motion accent that should draw the eye may get a short sound (whoosh, tick, click); most motion is silent. No
sound over foreground singing or on the logo. Details: `../sound-voice/SKILL.md`.
Sources: [Apple HIG motion](https://developer.apple.com/design/human-interface-guidelines/motion),
[Material duration & easing](https://m1.material.io/motion/duration-easing.html),
[UX in Motion manifesto](https://uxmag.com/articles/creating-usability-with-motion-the-ux-in-motion-manifesto).
