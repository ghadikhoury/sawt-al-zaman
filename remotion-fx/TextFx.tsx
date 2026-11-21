/* Text-window and slide effects the owner loves (2026-11-18), distilled from his reference reel
 * Sawt Al-Zaman/Style References/motion-edit/references/ref06 (George Wassouf) and the screenshots in Style References/text/examples.
 *
 * - <TextWindow>: big Arabic letters as a window. Whatever you pass as `inside` shows only through the letters (an exact
 *   alpha mask of the whole word, so the letter joins stay clean: no outline strokes). Give the inside its own motion
 *   and look so the letters seem alive: a second copy of the clip, offset, scaled, delayed or filtered.
 *   Presets in WINDOW_LOOKS (glass, chrome, bright, ink). `rim` adds a thin inner edge made from the word's own
 *   pixels (erode filter), for the glass or metal edge.
 * - <Smear>: the sliding transition. One SVG filter turns a moving picture into broken vertical strips sliding at
 *   different speeds, with a sideways motion blur (no colour fringes). Its strength follows the slide speed.
 * - <SlidePush>: shot A is pushed out and shot B pushed in (any direction) through <Smear>.
 * - <ColourSplit>, <Flash>, <SplitWord>, Smear split > 0: glitch and colour-fringe looks. BANNED by the owner
 *   (2026-11-18: "the colours around the blurring don't fit our vibe", "the glitch type effect is really bad for us").
 *   Kept only so old code compiles; do not use. Plain blur is fine.
 * - <Drift>: the "static background" helper. Moves a still photo slowly on its own path (pan, zoom, light sweep)
 *   so a window over a still photo still feels like footage.
 * Use: see FxDemo.tsx, and skills sawt-motion-edit (devices.md) and sawt-text (text-moves.md).
 */
import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, Easing } from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const ramp = (t: number, a: number, b: number, e = Easing.bezier(0.45, 0, 0.2, 1)) => interpolate(t, [a, b], [0, 1], { ...clamp, easing: e });

/* ---------- letters as a window ---------- */
export type WindowLook = { filter: string; dx: number; dy: number; scale: number; rim: number; rimColour: string; tint?: string };
export const WINDOW_LOOKS: Record<string, WindowLook> = {
  // «فوق الخدود»: a lighter, cooler, softened copy, slightly bigger than the background
  glass: { filter: "brightness(1.45) saturate(0.35) contrast(0.9) blur(1.5px)", dx: -24, dy: -10, scale: 1.12, rim: 2, rimColour: "rgba(255,255,255,.85)", tint: "rgba(190,215,235,.28)" },
  // Wassouf «اه يا قمر»: iridescent metal, strong contrast and shifted hues
  chrome: { filter: "contrast(1.9) saturate(2.2) hue-rotate(160deg) brightness(1.15)", dx: 30, dy: 18, scale: 1.25, rim: 2.5, rimColour: "rgba(255,250,235,.9)" },
  // «فوّق شفافك»: the same picture, brighter, a little zoomed
  bright: { filter: "brightness(1.9) contrast(1.15) grayscale(0.2)", dx: 0, dy: -14, scale: 1.08, rim: 0, rimColour: "#fff" },
  // brand version for the documentaries: warm sand glass
  sand: { filter: "brightness(1.35) sepia(0.55) saturate(1.2) contrast(0.95)", dx: -20, dy: -8, scale: 1.12, rim: 2, rimColour: "rgba(238,212,180,.9)", tint: "rgba(233,200,159,.25)" },
};

let uid = 0;
export const TextWindow: React.FC<{
  text: string; font: string; size: number; x?: number; y: number; w?: number; h?: number; weight?: number | string;
  inside: React.ReactNode; look?: WindowLook; reveal?: number; letterSpacing?: number; shadow?: boolean;
}> = ({ text, font, size, x = 0, y, w = 1080, h, weight = 400, inside, look = WINDOW_LOOKS.glass, reveal = 1, letterSpacing = 0, shadow = true }) => {
  const [id] = React.useState(() => `tw${uid++}`);
  const H = h ?? Math.round(size * 1.9);
  const txt = (fill: string, extra?: React.SVGProps<SVGTextElement>) => (
    <text x={w / 2} y={H * 0.6} textAnchor="middle" direction="rtl" fontFamily={font} fontSize={size} fontWeight={weight} letterSpacing={letterSpacing} fill={fill} {...extra}>{text}</text>
  );
  // reveal: the window opens upward through a soft edge (no fade of an outline)
  const cut = (1 - reveal) * H;
  return (
    <svg width={w} height={H} style={{ position: "absolute", left: x, top: y, overflow: "visible" }}>
      <defs>
        <linearGradient id={`${id}g`} x1="0" y1="1" x2="0" y2="0">
          <stop offset={Math.max(0, reveal - 0.15)} stopColor="#fff" /><stop offset={reveal} stopColor="#000" />
        </linearGradient>
        <mask id={id} maskUnits="userSpaceOnUse" x={-200} y={-200} width={w + 400} height={H + 400}>
          <rect x={-200} y={-200} width={w + 400} height={H + 400} fill="#000" />
          {txt("#fff")}
          <rect x={-200} y={-200} width={w + 400} height={H + 200 - (H - cut) + 0} fill="#000" opacity={reveal < 1 ? 1 : 0} />
        </mask>
        <filter id={`${id}r`} x="-10%" y="-30%" width="120%" height="160%">
          <feMorphology in="SourceAlpha" operator="erode" radius={look.rim} result="in" />
          <feComposite in="SourceAlpha" in2="in" operator="out" result="edge" />
          <feGaussianBlur in="edge" stdDeviation={0.6} result="soft" />
          <feFlood floodColor={look.rimColour} />
          <feComposite in2="soft" operator="in" />
        </filter>
        <filter id={`${id}s`} x="-20%" y="-40%" width="140%" height="180%"><feDropShadow dx={0} dy={8} stdDeviation={14} floodColor="#000" floodOpacity={0.35} /></filter>
      </defs>
      {shadow && <g opacity={0.9 * reveal} filter={`url(#${id}s)`} mask={`url(#${id})`}><rect x={-200} y={-200} width={w + 400} height={H + 400} fill="#000" opacity={0.01} /></g>}
      <g mask={`url(#${id})`}>
        <foreignObject x={-x} y={-y} width={1080} height={1920}>
          <div style={{ width: 1080, height: 1920, position: "relative", overflow: "hidden" }}>
            <div style={{ position: "absolute", inset: 0, transform: `translate(${look.dx}px, ${look.dy}px) scale(${look.scale})`, filter: look.filter }}>{inside}</div>
            {look.tint && <div style={{ position: "absolute", inset: 0, background: look.tint, mixBlendMode: "screen" }} />}
          </div>
        </foreignObject>
      </g>
      {look.rim > 0 && <g mask={`url(#${id})`} filter={`url(#${id}r)`}>{txt("#fff")}</g>}
    </svg>
  );
};

/* ---------- the sliding smear ---------- */
// v: 0 (still) .. 1 (fastest). dir: 1 = moving right, -1 = left.
export const Smear: React.FC<{ v: number; dir?: number; seed?: number; children: React.ReactNode; split?: number }> = ({ v, dir = 1, seed = 4, children, split = 0 }) => {   // split > 0 adds red/blue fringes: BANNED by the owner, keep 0
  const [id] = React.useState(() => `sm${uid++}`);
  const k = Math.max(0, Math.min(1, v));
  if (k < 0.01) return <AbsoluteFill>{children}</AbsoluteFill>;
  const fr = 8 * k * split;
  return (
    <AbsoluteFill>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <defs>
          <filter id={id} x="-10%" y="0%" width="120%" height="100%" colorInterpolationFilters="sRGB">
            {/* vertical bands of random strength: each strip slides by a different amount */}
            <feTurbulence type="fractalNoise" baseFrequency="0.012 0" numOctaves={2} seed={seed} result="n" />
            <feColorMatrix in="n" type="matrix" values="1 0 0 0 0  0 0 0 0 0.5  0 0 0 0 0  0 0 0 0 1" result="bands" />
            <feDisplacementMap in="SourceGraphic" in2="bands" scale={260 * k} xChannelSelector="R" yChannelSelector="G" result="slid" />
            <feGaussianBlur in="slid" stdDeviation={`${40 * k} 0`} result="blur" />
            {/* red and blue fringes only when split > 0 (owner banned them); otherwise the blur is the result */}
            {split > 0 && <feColorMatrix in="blur" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />}
            {split > 0 && <feOffset in="r" dx={fr * dir} result="ro" />}
            {split > 0 && <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0" result="gb" />}
            {split > 0 && <feOffset in="gb" dx={-fr * dir} result="gbo" />}
            {split > 0 && <feBlend in="ro" in2="gbo" mode="screen" />}
          </filter>
        </defs>
      </svg>
      <AbsoluteFill style={{ filter: `url(#${id})` }}>{children}</AbsoluteFill>
      {/* fine scan stripes over the move */}
      <AbsoluteFill style={{ background: "repeating-linear-gradient(90deg, rgba(255,255,255,.14) 0 2px, transparent 2px 7px)", opacity: k, mixBlendMode: "overlay" }} />
    </AbsoluteFill>
  );
};

// p: 0..1 over the transition. A leaves, B arrives. dir 1 = B comes from the left (moves right).
export const SlidePush: React.FC<{ p: number; a: React.ReactNode; b: React.ReactNode; dir?: number; width?: number }> = ({ p, a, b, dir = 1, width = 1080 }) => {
  const e = Easing.bezier(0.7, 0, 0.2, 1)(Math.max(0, Math.min(1, p)));
  const v = Math.sin(Math.PI * Math.max(0, Math.min(1, p)));        // speed, peaks mid-move
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <Smear v={v} dir={dir}>
        <AbsoluteFill style={{ transform: `translateX(${dir * e * width}px)` }}>{a}</AbsoluteFill>
        <AbsoluteFill style={{ transform: `translateX(${dir * (e - 1) * width}px)` }}>{b}</AbsoluteFill>
      </Smear>
    </AbsoluteFill>
  );
};

/* ---------- colour split and flash ---------- */
export const ColourSplit: React.FC<{ amount: number; children: React.ReactNode; angle?: number }> = ({ amount, children, angle = 0 }) => {
  const [id] = React.useState(() => `cs${uid++}`);
  const dx = Math.cos(angle) * amount, dy = Math.sin(angle) * amount;
  return (
    <AbsoluteFill>
      <svg width={0} height={0} style={{ position: "absolute" }}><defs>
        <filter id={id} colorInterpolationFilters="sRGB">
          <feColorMatrix type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" /><feOffset in="r" dx={dx} dy={dy} result="ro" />
          <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0" result="gb" /><feOffset in="gb" dx={-dx} dy={-dy} result="gbo" />
          <feBlend in="ro" in2="gbo" mode="screen" />
        </filter></defs></svg>
      <AbsoluteFill style={{ filter: amount > 0.2 ? `url(#${id})` : undefined }}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

// k: 0..1..0 over 3–4 frames
export const Flash: React.FC<{ k: number; children: React.ReactNode }> = ({ k, children }) => (
  <AbsoluteFill style={{ filter: k > 0.01 ? `contrast(${1 + 3 * k}) saturate(${1 + 2.5 * k}) brightness(${1 + 1.4 * k}) hue-rotate(${120 * k}deg)` : undefined }}>{children}</AbsoluteFill>
);

/* ---------- a still photo that moves on its own (for windows over static backgrounds) ---------- */
export const Drift: React.FC<{ src: string; t: number; from?: [number, number, number]; to?: [number, number, number]; dur?: number; pos?: string; light?: boolean }> = ({ src, t, from = [0, 0, 1.1], to = [-60, -20, 1.25], dur = 4, pos = "center", light = true }) => {
  const k = Math.min(1, Math.max(0, t / dur));
  const [x, y, s] = from.map((f, i) => f + (to[i] - f) * k);
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: pos, transform: `translate(${x}px, ${y}px) scale(${s})` }} />
      {light && <AbsoluteFill style={{ background: `linear-gradient(105deg, transparent ${-30 + 160 * k}%, rgba(255,240,215,.55) ${-15 + 160 * k}%, transparent ${0 + 160 * k}%)`, mixBlendMode: "screen" }} />}
    </AbsoluteFill>
  );
};

/* ---------- photo pop-up collage (ref06 «لون الورود») ----------
 * Photos appear one every `gap` frames as hard cuts (no fade), straight, unframed and overlapping, until the frame is
 * full; `outAt` removes them again in reverse order, just as fast. A one-frame 4% kick sells each arrival. */
export type PopPhoto = { src: string; x: number; y: number; w: number; h: number; pos?: string; filter?: string };
export const PhotoPop: React.FC<{ frame: number; at: number; photos: PopPhoto[]; gap?: number; outAt?: number; outGap?: number }> = ({ frame, at, photos, gap = 3, outAt = 1e9, outGap = 2 }) => (
  <AbsoluteFill>
    {photos.map((p, i) => {
      const inF = at + i * gap, outF = outAt + (photos.length - 1 - i) * outGap;
      if (frame < inF || frame >= outF) return null;
      const kick = frame - inF === 0 ? 1.04 : 1;
      return (
        <div key={i} style={{ position: "absolute", left: p.x, top: p.y, width: p.w, height: p.h, overflow: "hidden", transform: `scale(${kick})`, boxShadow: "0 10px 30px rgba(0,0,0,.35)" }}>
          <Img src={staticFile(p.src)} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: p.pos ?? "center", filter: p.filter }} />
        </div>
      );
    })}
  </AbsoluteFill>
);

/* ---------- font flicker on arrival ----------
 * The word cycles through `fonts` every `hold` frames for `frames` frames, then settles on the last one. */
export const flickerFont = (frame: number, at: number, fonts: string[], frames = 10, hold = 2) =>
  frame < at || frame >= at + frames ? fonts[fonts.length - 1] : fonts[Math.floor((frame - at) / hold) % fonts.length];

/* ---------- split-colour word: two offset coloured copies that close up into one ---------- */
export const SplitWord: React.FC<{ k: number; children: React.ReactNode; colours?: [string, string]; final: string; dist?: number; style?: React.CSSProperties }> = ({ k, children, colours = ["#A5603F", "#C79F8B"], final, dist = 14, style }) => (
  <div style={{ position: "relative", ...style }}>
    {k > 0.02 && <div style={{ position: "absolute", inset: 0, color: colours[0], transform: `translate(${dist * k}px, ${-dist * 0.4 * k}px)`, mixBlendMode: "screen" }}>{children}</div>}
    {k > 0.02 && <div style={{ position: "absolute", inset: 0, color: colours[1], transform: `translate(${-dist * k}px, ${dist * 0.4 * k}px)`, mixBlendMode: "screen" }}>{children}</div>}
    <div style={{ color: final, opacity: 1 - 0.7 * k }}>{children}</div>
  </div>
);
