"""Build a GreyScienx-styled A4 PDF from a Markdown research note."""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    LongTable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

from greyscienx_style import default_css_path, load_tokens


PAGE_W, PAGE_H = A4
LEFT = 19 * mm
RIGHT = 18 * mm
TOP = 20 * mm
BOTTOM = 19 * mm
FRAME_W = PAGE_W - LEFT - RIGHT


@dataclass
class FontNames:
    regular: str
    bold: str
    italic: str
    bold_italic: str


def _first_existing(paths):
    return next((path for path in paths if path.exists()), None)


def register_fonts() -> FontNames:
    roots = [Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")]
    files = {
        "regular": ["segoeui.ttf", "DejaVuSans.ttf"],
        "bold": ["segoeuib.ttf", "DejaVuSans-Bold.ttf"],
        "italic": ["segoeuii.ttf", "DejaVuSans-Oblique.ttf"],
        "bold_italic": ["segoeuiz.ttf", "DejaVuSans-BoldOblique.ttf"],
    }
    resolved = {
        key: _first_existing([root / filename for root in roots for filename in filenames])
        for key, filenames in files.items()
    }
    if all(resolved.values()):
        names = FontNames("GS-Regular", "GS-Bold", "GS-Italic", "GS-BoldItalic")
        for name, key in (
            (names.regular, "regular"),
            (names.bold, "bold"),
            (names.italic, "italic"),
            (names.bold_italic, "bold_italic"),
        ):
            pdfmetrics.registerFont(TTFont(name, str(resolved[key])))
    else:
        names = FontNames("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique")
    pdfmetrics.registerFontFamily(
        "GS",
        normal=names.regular,
        bold=names.bold,
        italic=names.italic,
        boldItalic=names.bold_italic,
    )
    return names


FONTS = register_fonts()
TOKENS = load_tokens()
COLOURS = {}
STYLES = {}
HEADER_TITLE = "GREYSCIENX RESEARCH"
FOOTER_META = "Research note"


def configure(css_path: Path):
    global TOKENS, COLOURS, STYLES
    TOKENS = load_tokens(css_path)
    COLOURS = {name: colors.HexColor(value) for name, value in TOKENS.items()}
    STYLES = make_styles()


class CoralRule(Flowable):
    def __init__(self, width=FRAME_W, height=4):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, avail_width, avail_height):
        return min(self.width, avail_width), self.height

    def draw(self):
        self.canv.setFillColor(COLOURS["coral"])
        self.canv.rect(0, 0, self.width, self.height, stroke=0, fill=1)


class SectionBanner(Flowable):
    def __init__(self, title: str, label: str):
        super().__init__()
        self.title = title
        self.label = label
        self.height = 42 * mm

    def wrap(self, avail_width, avail_height):
        self.width = avail_width
        return avail_width, self.height

    def draw(self):
        canvas = self.canv
        canvas.setFillColor(COLOURS["true-black"])
        canvas.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        canvas.setFillColor(COLOURS["coral"])
        canvas.rect(0, self.height - 4, self.width, 4, stroke=0, fill=1)
        canvas.setFont(FONTS.bold, 8)
        canvas.drawString(14, self.height - 19, self.label.upper())
        canvas.setFillColor(COLOURS["white"])
        canvas.setFont(FONTS.bold, 23)
        max_width = self.width - 28
        lines, current = [], ""
        for word in self.title.split():
            candidate = f"{current} {word}".strip()
            if pdfmetrics.stringWidth(candidate, FONTS.bold, 23) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        y = self.height - 42
        for line in lines[:2]:
            canvas.drawString(14, y, line)
            y -= 25


class GreyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        cover_frame = Frame(
            LEFT,
            BOTTOM,
            FRAME_W,
            PAGE_H - TOP - BOTTOM,
            id="cover-frame",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        body_frame = Frame(
            LEFT,
            BOTTOM,
            FRAME_W,
            PAGE_H - TOP - BOTTOM,
            id="body-frame",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(
            [
                PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover_page),
                PageTemplate(id="body", frames=[body_frame], onPage=draw_body_page),
            ]
        )

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name.startswith("TOC-"):
            level = {"TOC-H1": 0, "TOC-H2": 1, "TOC-H3": 2}[flowable.style.name]
            text = flowable.getPlainText()
            key = f"heading-{self.seq.nextf('heading')}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=level > 0)
            self.notify("TOCEntry", (level, text, self.page, key))


def draw_cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(COLOURS["true-black"])
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    for colour, bounds in (
        ("#adadad", (-110 * mm, PAGE_H - 46 * mm, 110 * mm, PAGE_H + 17 * mm)),
        ("#6e6e6e", (35 * mm, PAGE_H - 53 * mm, 180 * mm, PAGE_H + 12 * mm)),
        ("#ededed", (135 * mm, PAGE_H - 45 * mm, 290 * mm, PAGE_H + 18 * mm)),
    ):
        canvas.setFillColor(colors.HexColor(colour))
        canvas.ellipse(*bounds, stroke=0, fill=1)
    canvas.setFillColor(COLOURS["coral"])
    canvas.rect(0, 0, PAGE_W, 4, stroke=0, fill=1)
    canvas.rect(0, PAGE_H - 4, PAGE_W, 4, stroke=0, fill=1)
    canvas.restoreState()


def draw_body_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(COLOURS["white"])
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(COLOURS["coral"])
    canvas.rect(0, PAGE_H - 4, PAGE_W, 4, stroke=0, fill=1)
    canvas.setStrokeColor(COLOURS["grey-300"])
    canvas.setLineWidth(0.5)
    canvas.line(LEFT, PAGE_H - 15 * mm, PAGE_W - RIGHT, PAGE_H - 15 * mm)
    canvas.setFont(FONTS.bold, 7.4)
    canvas.setFillColor(COLOURS["black"])
    canvas.drawString(LEFT, PAGE_H - 11.3 * mm, "GREY")
    word_width = pdfmetrics.stringWidth("GREY", FONTS.bold, 7.4)
    canvas.setFillColor(COLOURS["coral"])
    canvas.drawString(LEFT + word_width, PAGE_H - 11.3 * mm, "SCIENX")
    canvas.setFillColor(COLOURS["grey-500"])
    canvas.setFont(FONTS.regular, 7.1)
    canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 11.3 * mm, HEADER_TITLE.upper())
    canvas.line(LEFT, 13.7 * mm, PAGE_W - RIGHT, 13.7 * mm)
    canvas.setFont(FONTS.regular, 7.2)
    canvas.drawString(LEFT, 9.5 * mm, FOOTER_META)
    canvas.setFont(FONTS.bold, 7.2)
    canvas.setFillColor(COLOURS["black"])
    canvas.drawRightString(PAGE_W - RIGHT, 9.5 * mm, f"{doc.page:02d}")
    canvas.restoreState()


def make_styles():
    base = getSampleStyleSheet()
    result = {}
    result["body"] = ParagraphStyle(
        "body",
        parent=base["BodyText"],
        fontName=FONTS.regular,
        fontSize=9.35,
        leading=13.7,
        textColor=COLOURS["black"],
        spaceAfter=5.8,
        allowWidows=0,
        allowOrphans=0,
    )
    result["bullet"] = ParagraphStyle(
        "bullet",
        parent=result["body"],
        leftIndent=13,
        firstLineIndent=-9,
        bulletIndent=0,
        spaceAfter=3.1,
    )
    result["number"] = ParagraphStyle(
        "number", parent=result["body"], leftIndent=18, firstLineIndent=-15, spaceAfter=4
    )
    result["quote"] = ParagraphStyle(
        "quote",
        parent=result["body"],
        fontName=FONTS.bold,
        fontSize=10.1,
        leading=14.7,
        textColor=COLOURS["white"],
        backColor=COLOURS["true-black"],
        borderPadding=(10, 13, 10, 15),
        spaceBefore=6,
        spaceAfter=12,
    )
    result["h1"] = ParagraphStyle(
        "TOC-H1",
        parent=base["Heading1"],
        fontName=FONTS.bold,
        fontSize=20,
        leading=22,
        textColor=COLOURS["black"],
        spaceAfter=12,
        keepWithNext=True,
    )
    result["h2"] = ParagraphStyle(
        "TOC-H2",
        parent=base["Heading2"],
        fontName=FONTS.bold,
        fontSize=16.2,
        leading=19,
        textColor=COLOURS["black"],
        spaceBefore=14,
        spaceAfter=7,
        keepWithNext=True,
    )
    result["h3"] = ParagraphStyle(
        "TOC-H3",
        parent=base["Heading3"],
        fontName=FONTS.bold,
        fontSize=11.8,
        leading=14.4,
        textColor=COLOURS["black"],
        spaceBefore=10,
        spaceAfter=4.5,
        keepWithNext=True,
    )
    result["caption"] = ParagraphStyle(
        "caption",
        parent=result["body"],
        fontName=FONTS.italic,
        fontSize=7.8,
        leading=10.5,
        textColor=COLOURS["grey-500"],
        spaceBefore=4,
        spaceAfter=10,
    )
    result["table"] = ParagraphStyle(
        "table",
        parent=result["body"],
        fontSize=7.35,
        leading=9.55,
        spaceAfter=0,
    )
    result["table-head"] = ParagraphStyle(
        "table-head",
        parent=result["table"],
        fontName=FONTS.bold,
        textColor=COLOURS["white"],
    )
    result["cover-kicker"] = ParagraphStyle(
        "cover-kicker", fontName=FONTS.bold, fontSize=8.4, leading=10,
        textColor=COLOURS["coral"], spaceAfter=14
    )
    result["cover-title"] = ParagraphStyle(
        "cover-title", fontName=FONTS.bold, fontSize=37, leading=34,
        textColor=COLOURS["white"], spaceAfter=18
    )
    result["cover-subtitle"] = ParagraphStyle(
        "cover-subtitle", fontName=FONTS.regular, fontSize=13.2, leading=19,
        textColor=colors.HexColor("#c8c8c8"), spaceAfter=22
    )
    result["cover-meta"] = ParagraphStyle(
        "cover-meta", fontName=FONTS.bold, fontSize=8, leading=11,
        textColor=COLOURS["white"], spaceAfter=4
    )
    result["toc-title"] = ParagraphStyle(
        "toc-title", fontName=FONTS.bold, fontSize=26, leading=29,
        textColor=COLOURS["black"], spaceAfter=8
    )
    result["toc-note"] = ParagraphStyle(
        "toc-note", fontName=FONTS.regular, fontSize=9.4, leading=14,
        textColor=COLOURS["grey-500"], spaceAfter=18
    )
    return result


def sanitize(text: str) -> str:
    return (
        text.replace("—", " - ")
        .replace("–", "-")
        .replace("−", "-")
        .replace("…", "...")
        .replace("\u00a0", " ")
    )


def inline_markup(text: str) -> str:
    text = sanitize(text.strip())
    links = []

    def hold_link(match):
        token = f"@@LINK{len(links)}@@"
        links.append((match.group(1), match.group(2)))
        return token

    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", hold_link, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for index, (label, url) in enumerate(links):
        safe_label = html.escape(sanitize(label), quote=False)
        safe_url = html.escape(url, quote=True)
        text = text.replace(
            f"@@LINK{index}@@",
            f'<a href="{safe_url}" color="{TOKENS["coral"]}"><u>{safe_label}</u></a>',
        )
    return text


def table_flowable(rows):
    parsed = []
    for row_index, row in enumerate(rows):
        style = STYLES["table-head"] if row_index == 0 else STYLES["table"]
        parsed.append([Paragraph(inline_markup(cell), style) for cell in row])
    columns = len(rows[0])
    if columns == 2:
        widths = [FRAME_W * 0.34, FRAME_W * 0.66]
    elif columns == 3:
        widths = [FRAME_W * 0.40, FRAME_W * 0.30, FRAME_W * 0.30]
    elif columns == 4:
        widths = [FRAME_W * 0.31, FRAME_W * 0.23, FRAME_W * 0.23, FRAME_W * 0.23]
    else:
        widths = [FRAME_W / columns] * columns
    if columns == 4 and "age" in sanitize(rows[0][0]).lower():
        widths = [FRAME_W * 0.14, FRAME_W * 0.285, FRAME_W * 0.285, FRAME_W * 0.29]
    table = LongTable(parsed, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), COLOURS["true-black"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, 0), 3, COLOURS["coral"]),
        ("LINEBELOW", (0, 1), (-1, -2), 0.35, COLOURS["grey-300"]),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, COLOURS["black"]),
    ]
    for row_index in range(2, len(rows), 2):
        commands.append(("BACKGROUND", (0, row_index), (-1, row_index), COLOURS["grey-100"]))
    table.setStyle(TableStyle(commands))
    return table


def resolve_image(source: str, markdown_path: Path) -> Path:
    raw = unquote(source)
    if raw.startswith("/") and re.match(r"/[A-Za-z]:/", raw):
        raw = raw[1:]
    path = Path(raw)
    if not path.is_absolute():
        path = markdown_path.parent / path
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    return path


def image_flowable(path: Path):
    image = Image(str(path))
    max_height = 170 * mm if image.imageHeight > image.imageWidth else 105 * mm
    scale = min(FRAME_W / image.imageWidth, max_height / image.imageHeight)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    image.hAlign = "CENTER"
    return image


def parse_markdown(lines, markdown_path: Path, skip_indexes: set[int]):
    story = []
    paragraph = []
    index = 0
    part_count = 0

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            story.append(Paragraph(inline_markup(" ".join(paragraph)), STYLES["body"]))
            paragraph = []

    while index < len(lines):
        raw = lines[index].rstrip()
        line = raw.strip()
        if index in skip_indexes:
            flush_paragraph()
            index += 1
            continue
        if not line:
            flush_paragraph()
            index += 1
            continue
        if line == "---":
            flush_paragraph()
            story.extend([Spacer(1, 4), CoralRule(height=2.6), Spacer(1, 8)])
            index += 1
            continue
        if line.startswith("| "):
            flush_paragraph()
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            rows = []
            for table_line in table_lines:
                cells = [cell.strip() for cell in table_line.strip("|").split("|")]
                if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    continue
                rows.append(cells)
            story.extend([Spacer(1, 4), table_flowable(rows), Spacer(1, 9)])
            continue
        image_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if image_match:
            flush_paragraph()
            path = resolve_image(image_match.group(2), markdown_path)
            group = [Spacer(1, 6), image_flowable(path), Spacer(1, 2)]
            caption_index = index + 1
            while caption_index < len(lines) and not lines[caption_index].strip():
                caption_index += 1
            caption = lines[caption_index].strip() if caption_index < len(lines) else ""
            if caption.startswith("*Figure ") and caption.endswith("*"):
                group.append(Paragraph(inline_markup(caption[1:-1]), STYLES["caption"]))
                index = caption_index + 1
            else:
                index += 1
            story.append(KeepTogether(group))
            continue
        if line.startswith("# "):
            flush_paragraph()
            title = sanitize(line[2:].strip())
            part_count += 1
            if part_count > 1:
                story.append(PageBreak())
            label, separator, title_body = title.partition(":")
            if not separator:
                label, title_body = "SECTION", title
            story.extend(
                [
                    SectionBanner(title_body.strip(), label.strip()),
                    Spacer(1, 11),
                    Paragraph(inline_markup(title), STYLES["h1"]),
                ]
            )
            index += 1
            continue
        if line.startswith("## "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[3:]), STYLES["h2"]))
            index += 1
            continue
        if line.startswith("### "):
            flush_paragraph()
            title = inline_markup(line[4:])
            story.append(
                Paragraph(f'<font color="{TOKENS["coral"]}">/</font> {title}', STYLES["h3"])
            )
            index += 1
            continue
        if line.startswith("> "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[2:]), STYLES["quote"]))
            index += 1
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if numbered:
            flush_paragraph()
            story.append(
                Paragraph(
                    f'<font color="{TOKENS["coral"]}"><b>{numbered.group(1)}.</b></font> '
                    f'{inline_markup(numbered.group(2))}',
                    STYLES["number"],
                )
            )
            index += 1
            continue
        if line.startswith("- "):
            flush_paragraph()
            story.append(
                Paragraph(
                    f'<font color="{TOKENS["coral"]}"><b>-</b></font> {inline_markup(line[2:])}',
                    STYLES["bullet"],
                )
            )
            index += 1
            continue
        if line.startswith("*Figure ") and line.endswith("*"):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[1:-1]), STYLES["caption"]))
            index += 1
            continue
        paragraph.append(line)
        index += 1

    flush_paragraph()
    return story


def title_markup(title: str, accent: str | None):
    escaped = html.escape(sanitize(title), quote=False)
    if not accent:
        return escaped
    safe_accent = html.escape(sanitize(accent), quote=False)
    return escaped.replace(safe_accent, f'<font color="{TOKENS["coral"]}">{safe_accent}</font>', 1)


def cover_story(args, title: str, subtitle: str):
    story = [
        Spacer(1, 44 * mm),
        Paragraph(args.eyebrow.upper(), STYLES["cover-kicker"]),
        CoralRule(width=28 * mm, height=4),
        Spacer(1, 10 * mm),
        Paragraph(title_markup(title, args.title_accent), STYLES["cover-title"]),
        Paragraph(inline_markup(subtitle), STYLES["cover-subtitle"]),
    ]
    if args.cover_stat:
        stats = [value.split("|", 1) for value in args.cover_stat[:3]]
        while len(stats) < 3:
            stats.append(["", ""])
        widths = [FRAME_W / 3] * 3
        table = Table(
            [[item[0] for item in stats], [item[1] if len(item) > 1 else "" for item in stats]],
            colWidths=widths,
            rowHeights=[18 * mm, 13 * mm],
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), COLOURS["coral"]),
                    ("TEXTCOLOR", (0, 0), (-1, -1), COLOURS["black"]),
                    ("FONTNAME", (0, 0), (-1, 0), FONTS.bold),
                    ("FONTSIZE", (0, 0), (-1, 0), 17),
                    ("FONTNAME", (0, 1), (-1, 1), FONTS.bold),
                    ("FONTSIZE", (0, 1), (-1, 1), 6.7),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LINEAFTER", (0, 0), (-2, -1), 1, COLOURS["black"]),
                ]
            )
        )
        story.extend([Spacer(1, 21 * mm), table, Spacer(1, 7 * mm)])
    else:
        story.append(Spacer(1, 38 * mm))
    story.extend(
        [
            Paragraph(inline_markup(args.meta), STYLES["cover-meta"]),
            NextPageTemplate("body"),
            PageBreak(),
        ]
    )
    return story


def toc_story():
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOCLevel1", fontName=FONTS.bold, fontSize=10.2, leading=15,
            leftIndent=0, textColor=COLOURS["black"], spaceBefore=7
        ),
        ParagraphStyle(
            "TOCLevel2", fontName=FONTS.regular, fontSize=8.7, leading=12.2,
            leftIndent=12, textColor=COLOURS["grey-700"], spaceBefore=2
        ),
        ParagraphStyle(
            "TOCLevel3", fontName=FONTS.regular, fontSize=7.7, leading=10.6,
            leftIndent=24, textColor=COLOURS["grey-500"], spaceBefore=1
        ),
    ]
    return [
        Paragraph("Inside the note", STYLES["toc-title"]),
        CoralRule(width=34 * mm, height=4),
        Spacer(1, 7),
        Paragraph("A map of the argument, model, evidence, and qualifications.", STYLES["toc-note"]),
        toc,
        PageBreak(),
    ]


def extract_preamble(lines):
    title_index = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    title = sanitize(lines[title_index][2:].strip()) if title_index is not None else "GreyScienx research note"
    subtitle_index = None
    if title_index is not None:
        subtitle_index = next(
            (i for i in range(title_index + 1, min(len(lines), title_index + 8)) if lines[i].startswith("## ")),
            None,
        )
    subtitle = (
        sanitize(lines[subtitle_index][3:].strip())
        if subtitle_index is not None
        else "A clear, evidence-led research publication."
    )
    skip = {index for index in (title_index, subtitle_index) if index is not None}
    return title, subtitle, skip


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Markdown source")
    parser.add_argument("output", type=Path, help="Destination PDF")
    parser.add_argument("--css", type=Path, default=default_css_path())
    parser.add_argument("--title")
    parser.add_argument("--subtitle")
    parser.add_argument("--title-accent")
    parser.add_argument("--eyebrow", default="GreyScienx research note")
    parser.add_argument("--meta", default="GreyScienx | Research publication")
    parser.add_argument("--header-title")
    parser.add_argument("--footer-meta", default="Research note")
    parser.add_argument("--author", default="GreyScienx")
    parser.add_argument("--subject", default="GreyScienx research publication")
    parser.add_argument("--cover-stat", action="append", help="Repeat VALUE|LABEL up to three times")
    parser.add_argument("--no-toc", action="store_true")
    return parser.parse_args()


def main():
    global HEADER_TITLE, FOOTER_META
    args = parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    if not source.exists():
        raise SystemExit(f"Markdown source not found: {source}")
    configure(args.css.resolve())
    lines = source.read_text(encoding="utf-8").splitlines()
    detected_title, detected_subtitle, skip_indexes = extract_preamble(lines)
    title = sanitize(args.title or detected_title)
    subtitle = sanitize(args.subtitle or detected_subtitle)
    HEADER_TITLE = sanitize(args.header_title or title)
    FOOTER_META = sanitize(args.footer_meta)
    output.parent.mkdir(parents=True, exist_ok=True)
    content = parse_markdown(lines, source, skip_indexes)
    story = cover_story(args, title, subtitle)
    if not args.no_toc:
        story += toc_story()
    story += content
    doc = GreyDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title=title,
        author=args.author,
        subject=args.subject,
        creator="GreyScienx editorial PDF skill",
    )
    doc.multiBuild(story)
    print(output)


if __name__ == "__main__":
    main()
