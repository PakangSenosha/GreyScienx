"""Render a PDF and make contact sheets for complete visual inspection."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


def render_pdf(pdf: Path, rendered: Path, dpi: int):
    executable = shutil.which("pdftoppm")
    if not executable:
        raise SystemExit("pdftoppm was not found. Install Poppler or add it to PATH.")
    rendered.mkdir(parents=True, exist_ok=True)
    if list(rendered.glob("page-*.png")):
        raise SystemExit(f"Rendered-page directory is not empty; choose a fresh --out-dir: {rendered}")
    prefix = rendered / "page"
    subprocess.run(
        [executable, "-png", "-r", str(dpi), str(pdf), str(prefix)],
        check=True,
    )
    return sorted(rendered.glob("page-*.png"))


def make_contact_sheets(pages, sheets_dir: Path, columns: int, rows: int):
    sheets_dir.mkdir(parents=True, exist_ok=True)
    thumb_width = 455
    label_height = 30
    gap = 16
    page_count = columns * rows
    output_paths = []

    for group_index in range(0, len(pages), page_count):
        group = pages[group_index : group_index + page_count]
        with Image.open(group[0]) as first:
            thumb_height = round(first.height * thumb_width / first.width)
        canvas = Image.new(
            "RGB",
            (
                columns * thumb_width + (columns + 1) * gap,
                rows * (thumb_height + label_height) + (rows + 1) * gap,
            ),
            "#d8d8d8",
        )
        draw = ImageDraw.Draw(canvas)
        for offset, path in enumerate(group):
            row, column = divmod(offset, columns)
            with Image.open(path) as source:
                image = source.convert("RGB")
                image.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            x = gap + column * (thumb_width + gap)
            y = gap + row * (thumb_height + label_height + gap)
            canvas.paste(image, (x, y + label_height))
            draw.text((x + 5, y + 6), path.stem.upper(), fill="#131200")
        output = sheets_dir / f"sheet-{group_index // page_count + 1}.png"
        canvas.save(output, quality=95)
        output_paths.append(output)
    return output_paths


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--dpi", type=int, default=110)
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--rows", type=int, default=3)
    return parser.parse_args()


def main():
    args = parse_args()
    pdf = args.pdf.resolve()
    if not pdf.exists():
        raise SystemExit(f"PDF not found: {pdf}")
    pages = render_pdf(pdf, args.out_dir / "pages", args.dpi)
    sheets = make_contact_sheets(
        pages,
        args.out_dir / "contact-sheets",
        max(1, args.columns),
        max(1, args.rows),
    )
    print(f"Rendered {len(pages)} pages")
    for sheet in sheets:
        print(sheet.resolve())


if __name__ == "__main__":
    main()
