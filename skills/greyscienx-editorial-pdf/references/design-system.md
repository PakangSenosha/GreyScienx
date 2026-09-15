# GreyScienx PDF and figure design system

This document translates `app/globals.css` into a reproducible editorial system. The stylesheet remains authoritative: if its core tokens change, reload them and update output rather than preserving stale values here.

## Contents

- Brand source and visual character
- Page architecture
- Typography
- Editorial components
- Scientific figures
- Content integrity
- Export and quality assurance

## Brand source and visual character

Read these CSS custom properties at build time:

| Token | Current value | Print role |
|---|---:|---|
| `--black` | `#131200` | Main text, axes, rules |
| `--true-black` | `#000000` | Cover, section banners, callouts, table headers |
| `--coral` | `#f26157` | Brand rule, primary data series, links, emphasis |
| `--white` | `#fbfffe` | Page and figure ground |
| `--grey-100` | `#f0f1f2` | Alternating table rows and quiet bands |
| `--grey-300` | `#cccccc` | Hairlines and grids |
| `--grey-500` | `#777777` | Captions and tertiary series |
| `--grey-700` | `#3d3d3d` | Secondary copy |

The visual character is high-contrast, editorial, and sharp-edged. Use true black fields, coral rules, oversized heavy headings, white or warm-paper reading surfaces, and restrained grey structure. Avoid rounded cards, gradients, soft shadows, excessive colour, or ornamental data-ink. The site uses offset black shadows in interface cards; in a long-form PDF, reserve that device for rare covers or short feature panels.

## Page architecture

- Use A4 portrait unless the source requires another format.
- Set body margins near 18-20 mm. Leave enough top and bottom space for running furniture.
- Draw a 4 pt coral rule at the top of every page. A matching bottom rule belongs on the cover, not every body page.
- Cover: true-black field, coral eyebrow and rule, large white title with coral emphasis, restrained grey wave forms near the top, and at most three factual metrics in a coral band.
- Body header: small GreyScienx wordmark at left and short publication title at right, divided from the page by a light grey hairline.
- Footer: short metadata at left, zero-padded page number at right, and a light grey hairline above.
- Major parts may open with a rectangular black banner, a coral top rule, a small coral part label, and a large white title.
- Prefer a deliberate page break to an orphaned heading, caption, table header, or one-line final page.

## Typography

Use Segoe UI when available, falling back to a neutral sans serif. Embed the fonts in the PDF.

| Element | Typical print treatment |
|---|---|
| Cover title | 34-40 pt, bold, tight leading |
| Part banner | 21-25 pt, bold |
| Section heading | 15-18 pt, bold |
| Subheading | 11-13 pt, bold, optional coral slash |
| Body | 9.2-9.8 pt, 1.42-1.50 line spacing |
| Table | 7.2-8.0 pt with comfortable cell padding |
| Caption/footer | 7.2-8.2 pt |

Use bold to establish hierarchy, not to decorate entire paragraphs. Keep long prose on the white page; black fields are for short, high-value statements.

## Editorial components

### Tables

- Use a true-black header row with white bold text and a 3-4 pt coral rule beneath it.
- Use alternating white and `--grey-100` rows.
- Prefer horizontal hairlines to vertical grids.
- Align numeric columns right when that improves scanning.
- Repeat the header on subsequent pages and keep its text explicitly white; container text colour alone may not override paragraph styling.
- Keep units in headings and avoid repeating them in every cell.

### Callouts and quotations

Use a true-black rectangle with white text for a thesis, qualification, or counterweight that materially changes interpretation. Use coral sparingly as a rule or label. Do not place long passages in reverse type.

### Links and citations

Use coral underlined text for clickable links. Preserve the full destination as a PDF annotation. Citations belong near the claim they support unless the source requests a formal reference list.

### Lists

Use compact spacing and a coral ASCII hyphen. Do not substitute large decorative bullets.

## Scientific figures

Figures must look native to the publication and remain analytically honest.

### Frame and hierarchy

- Use the white page colour as the figure background.
- Add a coral top rule, a small coral field label, a bold left-aligned title, and an optional one-line grey subtitle.
- Keep axes black, gridlines thin and grey, and remove top/right spines unless they carry meaning.
- Use explicit axis titles and units. Captions below the figure should explain interpretation, not repeat the title.
- Export raster figures at 240-300 dpi at the dimensions at which they will be placed.

### Data encodings

Use colour plus line style or marker so meaning does not depend on colour alone:

| Role | Colour | Line | Marker |
|---|---|---|---|
| Primary or early case | Coral | Solid | Circle |
| Comparator or later case | Black | Dashed | Square |
| Third scenario | Grey 500 | Dotted | Diamond |

For additional persistent series, reuse these colours only when distinct line styles, markers, facets, or direct labels keep the mapping unambiguous. Prefer small multiples over a rainbow legend.

### Labels and annotation

- Direct-label important endpoints when space permits.
- Place event annotations away from lines and markers; inspect the final placed size, not only the source canvas.
- Keep chart text at least about 7 pt in the printed artifact.
- Use constant-rand or nominal-rand labels explicitly when monetary values span time.
- A negative simulated balance must be described according to the model - for example as a funding shortfall rather than literal bank debt - when that distinction matters.

## Content integrity

- Preserve the source's substantive sections even when redesigning the publication.
- Do not introduce equations, appendices, forecasts, or causal claims unless requested. If a user asks to remove equations, remove the notation without removing the readable economic reasoning.
- Distinguish examples, scenarios, estimates, and forecasts in both prose and figure labels.
- Treat combined household wealth as an aggregate: it does not establish equal control or individual welfare.
- Keep assumptions and caveats visible enough to constrain interpretation.

## Export and quality assurance

Before delivery:

1. Confirm the PDF metadata, page size, page count, file size, and lack of unintended encryption.
2. Extract text and verify the title, major headings, conclusion, and citations are present.
3. Render every page with Poppler at roughly 110-150 dpi.
4. Inspect contact sheets, then inspect dense tables and every figure at original size.
5. Check cover alignment, running furniture, table headers, link contrast, caption placement, plot-label collisions, and the final page.
6. Rebuild and repeat the affected checks after every visual change.

A successful export is not sufficient evidence of a successful publication.
