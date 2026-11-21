# Font library: every font, its group, its role and the owner's verdict

Source of truth for code: `Tools/Remotion/src/fonts/library.ts` (`font("camelExtraBold")` loads a font and returns
`{ family, weight }`). Every kept font has its file in `fonts/` in this folder (all 9, 2026-11-18). The renderer reads the downloaded ones
from `Tools/Remotion/public/fonts/` (copy any new file to both) and loads the Google ones (Amiri, Scheherazade, Katibeh,
Mirza) through `@remotion/google-fonts`; their `.ttf` copies here are for installing elsewhere or sharing (SIL Open
Font Licence, `fonts/OFL-licence-google-fonts.txt`). `microsoft-uighur.ttf` is a Windows font licensed with Windows:
fine on this PC, **don't share or upload it** (Windows has no separate bold file; bold is synthesised). Sheet of all kept fonts: `examples/font_collection.png`. Update this file, `library.ts`
and the sheet with every verdict.

## BOLD group (big titles, hero words, accent words)
| Font | Use | Notes |
|---|---|---|
| **The Year of the Camel ExtraBold** | Big lyric and title words, accent words, the bold half of any pair | **First choice.** The owner's own font (ArbFonts; called "Old Camel" in the brand file, his account's font before). Liked in test boxes 1 and 8. |
| **PT Bold Heading** | Very heavy poster titles | His account's other old font. Closest free font to the Wassouf reel's thick «فوّق شفافك». Puts the shadda (ّ) too high: leave it off or check every word. Round counters, not the reel's triangles. |

## THIN group (lines, sub-lines, the quieter word beside a bold one)
| Font | Use | Notes |
|---|---|---|
| **The Year of the Camel Light** | Lyric lines, the light word of a contrast pair, already-stretched words | The default partner of Camel ExtraBold (reel 2's long stretched opening). |
| **Diwani Letter** | Calligraphic accent: romantic, ceremonial or nostalgic lines, a name | Liked 2026-11-18. Long swashes: generous line height (≥1.6) and padding, or they clip. Ottoman diwani; reads elegant, not everyday. |
| **Amiri** (bold) | Lines, captions, and display lines | Liked at small size first, then again at display size (2026-11-18). Classic naskh, tarab feel. Stacked ligatures (لخ): set `fontVariantLigatures: "none"` if a word reads oddly. |
| **Katibeh** | Spoken lines and titles in documentaries | Liked in Warda and Baligh ("I like the font for speech"). |
| **Mirza** | Small lines under titles | Quiet, readable; no complaint. |
| **Scheherazade New** (bold) | Small text only | Soft classic naskh. |
| **Microsoft Uighur** (bold) | Small text only | Clean, confident. A Windows font: renders on this PC only. |

## Pairs that work
- **Camel ExtraBold + Camel Light**: same family, maximum weight contrast. The default.
- **Camel ExtraBold + Diwani Letter**: a heavy word beside a flowing calligraphic one (heavy + "italic-serif-like"
  contrast he praised in reel 1, in an Arabic form).
- **Camel ExtraBold + Amiri or Katibeh**: big lyric word with a calm line under it.
- **PT Bold Heading + Mirza or Scheherazade**: heavy poster title with a small caption.
Never more than two families in a frame. Weight contrast does the work; colour contrast is one accent at most.

## Wanted, not owned
- **Beirut** (Diwan Software): the Wassouf reel's thick font (triangular counters, flat base, joined dots on ق). Would
  join the bold group. Mac/iPhone system font, $200 on MyFonts; Apple's licence covers Apple devices, so don't copy it
  from a Mac. Comparison: `examples/fawwaq_shfafak_all_fonts_brand.png`.
- **The Wassouf reel's tall calligraphic naskh** («فوق الخدود», «حلف القمر»): not identified (`examples/fonts_reel_vs_matches.png`).
- DecoType Naskh and Al-Jazeera Bold (Gemini's suggestions for reel 3): commercial/private, no preview available.

## Not to use (with the reason, so nobody re-proposes them)
- **Removed by the owner:** B Jadid V2 Bold ("I don't like it anymore"); The Year of the Camel Thin, ExtraLight,
  Regular, Medium, Bold (only Light and ExtraBold kept).
- **Disliked:** Lalezar ("not like the thick one in the Wassouf video"), Alkalami ("really dislike"), Ruwudu (effects
  test), Alexandria, Aref Ruqaa and Aref Ruqaa Ink, Amiri *italic* (all hated in BaeedAnak v2).
- **Retired:** Jomhuria, Lateef, Gulzar (first set, replaced: "I don't like the current font"); reel 3's big fonts.
- **Unusable:** Qahiri (drops the letter dots).
- **Shown and not chosen:** Reem Kufi, Changa, El Messiri, Blaka, Rakkas, Vibes, Badeen Display, Markazi, Parastoo,
  Lemonada, Cairo (all weights), Tajawal, Almarai, Marhey, Beiruti, Zain, IBM Plex Sans Arabic, Traditional Arabic,
  Farsi Simple Bold, B Titr Bold, Old Antic Bold, VIP Hala Bold, Diwani Bent, IranNastaliq, Aldhabi.
  Sheets: `examples/gemini_reel3_fonts.png`, `examples/fawwaq_shfafak_all_fonts_brand.png`.

## Adding a font
1. Find candidates (Google Fonts with Arabic via `@remotion/google-fonts`, an installed Windows font, or arfonts.net for
   Arabic display fonts; preview there without downloading). 2. Render a sheet with the film's real words in brand
   colours (`Tools/Remotion/src/fx/FontMatch.tsx`, `Collection.tsx`, `GeminiFonts.tsx`), or recolour the site
   preview. 3. Send it; download only what he picks (use the site's own download button, ignore ad buttons; take only
   the .ttf/.otf from the zip; check it starts with TrueType/OTTO bytes). 4. Record the verdict and the group here and
   in `library.ts`. Never put a new font into a film before he has seen it.
