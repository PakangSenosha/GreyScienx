---
name: greyscienx-editorial-pdf
description: Create or restyle GreyScienx research PDFs and their scientific figures from Markdown or structured prose. Use when a deliverable should reproduce the visual language in app/globals.css; do not use for the GreyScienx website UI itself.
---

# GreyScienx editorial PDF

Produce a readable research publication whose cover, typography, tables, callouts, figures, and page furniture form one GreyScienx system. Treat `app/globals.css` as the colour and brand source of truth.

Before designing or revising an artifact, read [references/design-system.md](references/design-system.md). It is both the human specification and the decision guide for the scripts.

## Workflow

1. Inspect the source, the requested output, `app/globals.css`, and any existing figures. Preserve the author's argument, assumptions, caveats, citations, and requested omissions.
2. For ordinary Markdown research notes, start with `scripts/build_report.py`. Use its command help to select the title, subtitle, cover statistics, metadata, and CSS source.
3. For Python figures, import `scripts/greyscienx_style.py` and use its token loader, Matplotlib configuration, chart header, axis treatment, and redundant line encodings. Keep figures legible when placed at final PDF size.
4. Use the PDF creation workflow available in the environment. Keep intermediate renders outside the final output directory.
5. Run `scripts/render_check.py` on the PDF, inspect every generated contact sheet, and revise any clipped text, orphaned caption, weak contrast, crowded chart, sparse trailing page, or broken table header.

The scripts are reproducible starting points, not permission to flatten the content into a rigid template. Adapt composition when the material requires it while preserving the visual invariants in the design reference.

## Runtime

The renderer uses Python with ReportLab. Figure styling uses Matplotlib, and the QA helper uses Pillow plus Poppler's `pdftoppm`. If a dependency is unavailable, use the workspace-provided document/PDF runtime or install it only with the user's approval when approval is required.

## Common commands

```powershell
python skills/greyscienx-editorial-pdf/scripts/build_report.py note.md output.pdf --css app/globals.css --title "Research title" --subtitle "Readable subtitle" --cover-stat "R50,000|combined monthly income"
```

```powershell
python skills/greyscienx-editorial-pdf/scripts/render_check.py output.pdf --out-dir work/pdf-check
```

Do not claim completion from a successful build alone. Completion requires readable extracted text, correct metadata, expected figures and tables, and visual review of every page.
