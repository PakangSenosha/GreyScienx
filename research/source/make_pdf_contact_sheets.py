"""Create contact sheets for visual QA of every rendered PDF page."""

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RENDERED = ROOT / "work" / "pdf" / "rendered-final"
SHEETS = ROOT / "work" / "pdf" / "contact-sheets-final"
SHEETS.mkdir(parents=True, exist_ok=True)

pages = sorted(RENDERED.glob("page-*.png"))
thumb_width = 455
label_height = 30
gap = 16
cols = 2
rows = 3

for group_index in range(0, len(pages), cols * rows):
    group = pages[group_index:group_index + cols * rows]
    first = Image.open(group[0]).convert("RGB")
    thumb_height = round(first.height * thumb_width / first.width)
    sheet = Image.new(
        "RGB",
        (
            cols * thumb_width + (cols + 1) * gap,
            rows * (thumb_height + label_height) + (rows + 1) * gap,
        ),
        "#d8d8d8",
    )
    draw = ImageDraw.Draw(sheet)
    for offset, path in enumerate(group):
        row, col = divmod(offset, cols)
        image = Image.open(path).convert("RGB")
        image.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        x = gap + col * (thumb_width + gap)
        y = gap + row * (thumb_height + label_height + gap)
        sheet.paste(image, (x, y + label_height))
        draw.text((x + 5, y + 6), path.stem.upper(), fill="#131200")
    sheet.save(SHEETS / f"sheet-{group_index // (cols * rows) + 1}.png", quality=95)

print(f"Created {len(list(SHEETS.glob('sheet-*.png')))} contact sheets for {len(pages)} pages")
