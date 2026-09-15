"""Build a GreyScienx-styled PDF from the canonical Markdown research note."""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
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

from greyscienx_theme import (
    BLACK,
    CORAL,
    GREY_100,
    GREY_300,
    GREY_500,
    GREY_700,
    PAPER,
    TRUE_BLACK,
    WHITE,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "outputs" / "economics-of-living-together-v0.5.md"
OUTPUT = ROOT / "outputs" / "greyscienx-economics-of-living-together.pdf"
ASSETS = ROOT / "work" / "pdf" / "assets"

PAGE_W, PAGE_H = A4
LEFT = 19 * mm
RIGHT = 18 * mm
TOP = 20 * mm
BOTTOM = 19 * mm
FRAME_W = PAGE_W - LEFT - RIGHT


def register_fonts():
    candidates = {
        "GS-Regular": Path("C:/Windows/Fonts/segoeui.ttf"),
        "GS-Bold": Path("C:/Windows/Fonts/segoeuib.ttf"),
        "GS-Italic": Path("C:/Windows/Fonts/segoeuii.ttf"),
        "GS-BoldItalic": Path("C:/Windows/Fonts/segoeuiz.ttf"),
    }
    fallback = {
        "GS-Regular": Path("C:/Windows/Fonts/arial.ttf"),
        "GS-Bold": Path("C:/Windows/Fonts/arialbd.ttf"),
        "GS-Italic": Path("C:/Windows/Fonts/ariali.ttf"),
        "GS-BoldItalic": Path("C:/Windows/Fonts/arialbi.ttf"),
    }
    for name, path in candidates.items():
        target = path if path.exists() else fallback[name]
        pdfmetrics.registerFont(TTFont(name, str(target)))
    pdfmetrics.registerFontFamily(
        "GS",
        normal="GS-Regular",
        bold="GS-Bold",
        italic="GS-Italic",
        boldItalic="GS-BoldItalic",
    )


register_fonts()
C_BLACK = colors.HexColor(BLACK)
C_TRUE_BLACK = colors.HexColor(TRUE_BLACK)
C_CORAL = colors.HexColor(CORAL)
C_WHITE = colors.HexColor(WHITE)
C_PAPER = colors.HexColor(PAPER)
C_G100 = colors.HexColor(GREY_100)
C_G300 = colors.HexColor(GREY_300)
C_G500 = colors.HexColor(GREY_500)
C_G700 = colors.HexColor(GREY_700)


class CoralRule(Flowable):
    def __init__(self, width=FRAME_W, height=4):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return min(self.width, availWidth), self.height

    def draw(self):
        self.canv.setFillColor(C_CORAL)
        self.canv.rect(0, 0, self.width, self.height, stroke=0, fill=1)


class SectionBanner(Flowable):
    def __init__(self, title, label):
        super().__init__()
        self.title = title
        self.label = label
        self.height = 42 * mm

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(C_TRUE_BLACK)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.setFillColor(C_CORAL)
        c.rect(0, self.height - 4, self.width, 4, stroke=0, fill=1)
        c.setFont("GS-Bold", 8)
        c.drawString(14, self.height - 19, self.label.upper())
        c.setFillColor(C_WHITE)
        c.setFont("GS-Bold", 23)
        max_width = self.width - 28
        words = self.title.split()
        lines, current = [], ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if pdfmetrics.stringWidth(candidate, "GS-Bold", 23) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        y = self.height - 42
        for line in lines[:2]:
            c.drawString(14, y, line)
            y -= 25


class GreyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        from reportlab.platypus import Frame

        cover_frame = Frame(LEFT, BOTTOM, FRAME_W, PAGE_H - TOP - BOTTOM, id="cover-frame",
                            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        body_frame = Frame(LEFT, BOTTOM, FRAME_W, PAGE_H - TOP - BOTTOM, id="body-frame",
                           leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
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
    canvas.setFillColor(C_TRUE_BLACK)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#adadad"))
    canvas.ellipse(-110 * mm, PAGE_H - 46 * mm, 110 * mm, PAGE_H + 17 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#6e6e6e"))
    canvas.ellipse(35 * mm, PAGE_H - 53 * mm, 180 * mm, PAGE_H + 12 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#ededed"))
    canvas.ellipse(135 * mm, PAGE_H - 45 * mm, 290 * mm, PAGE_H + 18 * mm, stroke=0, fill=1)
    canvas.setFillColor(C_CORAL)
    canvas.rect(0, 0, PAGE_W, 4, stroke=0, fill=1)
    canvas.rect(0, PAGE_H - 4, PAGE_W, 4, stroke=0, fill=1)
    canvas.restoreState()


def draw_body_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(C_CORAL)
    canvas.rect(0, PAGE_H - 4, PAGE_W, 4, stroke=0, fill=1)
    canvas.setStrokeColor(C_G300)
    canvas.setLineWidth(0.5)
    canvas.line(LEFT, PAGE_H - 15 * mm, PAGE_W - RIGHT, PAGE_H - 15 * mm)
    canvas.setFont("GS-Bold", 7.4)
    canvas.setFillColor(C_BLACK)
    canvas.drawString(LEFT, PAGE_H - 11.3 * mm, "GREY")
    grey_width = pdfmetrics.stringWidth("GREY", "GS-Bold", 7.4)
    canvas.setFillColor(C_CORAL)
    canvas.drawString(LEFT + grey_width, PAGE_H - 11.3 * mm, "SCIENX")
    canvas.setFillColor(C_G500)
    canvas.setFont("GS-Regular", 7.1)
    canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 11.3 * mm, "THE ECONOMICS OF LIVING TOGETHER")
    canvas.setStrokeColor(C_G300)
    canvas.line(LEFT, 13.7 * mm, PAGE_W - RIGHT, 13.7 * mm)
    canvas.setFont("GS-Regular", 7.2)
    canvas.setFillColor(C_G500)
    canvas.drawString(LEFT, 9.5 * mm, "Research note | constant 2026 rand")
    canvas.setFont("GS-Bold", 7.2)
    canvas.setFillColor(C_BLACK)
    canvas.drawRightString(PAGE_W - RIGHT, 9.5 * mm, f"{doc.page:02d}")
    canvas.restoreState()


def make_styles():
    base = getSampleStyleSheet()
    styles = {}
    styles["body"] = ParagraphStyle(
        "body",
        parent=base["BodyText"],
        fontName="GS-Regular",
        fontSize=9.35,
        leading=13.7,
        textColor=C_BLACK,
        spaceAfter=5.8,
        allowWidows=0,
        allowOrphans=0,
    )
    styles["lead"] = ParagraphStyle(
        "lead",
        parent=styles["body"],
        fontSize=11.2,
        leading=16.0,
        textColor=C_G700,
        spaceAfter=11,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet",
        parent=styles["body"],
        leftIndent=13,
        firstLineIndent=-9,
        bulletIndent=0,
        spaceAfter=3.1,
    )
    styles["number"] = ParagraphStyle(
        "number",
        parent=styles["body"],
        leftIndent=18,
        firstLineIndent=-15,
        spaceAfter=4,
    )
    styles["quote"] = ParagraphStyle(
        "quote",
        parent=styles["body"],
        fontName="GS-Bold",
        fontSize=10.1,
        leading=14.7,
        textColor=C_WHITE,
        backColor=C_TRUE_BLACK,
        borderColor=C_CORAL,
        borderWidth=0,
        borderPadding=(10, 13, 10, 15),
        leftIndent=0,
        rightIndent=0,
        spaceBefore=6,
        spaceAfter=12,
    )
    styles["h1"] = ParagraphStyle(
        "TOC-H1",
        parent=base["Heading1"],
        fontName="GS-Bold",
        fontSize=20,
        leading=22,
        textColor=C_BLACK,
        spaceBefore=0,
        spaceAfter=12,
        keepWithNext=True,
    )
    styles["h2"] = ParagraphStyle(
        "TOC-H2",
        parent=base["Heading2"],
        fontName="GS-Bold",
        fontSize=16.2,
        leading=19,
        textColor=C_BLACK,
        spaceBefore=14,
        spaceAfter=7,
        keepWithNext=True,
    )
    styles["h3"] = ParagraphStyle(
        "TOC-H3",
        parent=base["Heading3"],
        fontName="GS-Bold",
        fontSize=11.8,
        leading=14.4,
        textColor=C_BLACK,
        spaceBefore=10,
        spaceAfter=4.5,
        borderColor=C_CORAL,
        borderWidth=0,
        borderPadding=(0, 0, 0, 0),
        keepWithNext=True,
    )
    styles["caption"] = ParagraphStyle(
        "caption",
        parent=styles["body"],
        fontName="GS-Italic",
        fontSize=7.8,
        leading=10.5,
        textColor=C_G500,
        spaceBefore=4,
        spaceAfter=10,
    )
    styles["table"] = ParagraphStyle(
        "table",
        parent=styles["body"],
        fontSize=7.35,
        leading=9.55,
        textColor=C_BLACK,
        spaceAfter=0,
    )
    styles["table-head"] = ParagraphStyle(
        "table-head",
        parent=styles["table"],
        fontName="GS-Bold",
        textColor=C_WHITE,
    )
    styles["cover-kicker"] = ParagraphStyle(
        "cover-kicker",
        fontName="GS-Bold",
        fontSize=8.4,
        leading=10,
        textColor=C_CORAL,
        spaceAfter=14,
    )
    styles["cover-title"] = ParagraphStyle(
        "cover-title",
        fontName="GS-Bold",
        fontSize=37,
        leading=34,
        textColor=C_WHITE,
        spaceAfter=18,
    )
    styles["cover-subtitle"] = ParagraphStyle(
        "cover-subtitle",
        fontName="GS-Regular",
        fontSize=13.2,
        leading=19,
        textColor=colors.HexColor("#c8c8c8"),
        spaceAfter=22,
    )
    styles["cover-meta"] = ParagraphStyle(
        "cover-meta",
        fontName="GS-Bold",
        fontSize=8,
        leading=11,
        textColor=C_WHITE,
        spaceAfter=4,
    )
    styles["toc-title"] = ParagraphStyle(
        "toc-title",
        fontName="GS-Bold",
        fontSize=26,
        leading=29,
        textColor=C_BLACK,
        spaceAfter=8,
    )
    styles["toc-note"] = ParagraphStyle(
        "toc-note",
        fontName="GS-Regular",
        fontSize=9.4,
        leading=14,
        textColor=C_G500,
        spaceAfter=18,
    )
    return styles


STYLES = make_styles()


def sanitize(text):
    return (
        text.replace("—", " - ")
        .replace("–", "-")
        .replace("−", "-")
        .replace("…", "...")
        .replace(" ", " ")
    )


def inline_markup(text):
    text = sanitize(text.strip())
    links = []

    def hold_link(match):
        label, url = match.group(1), match.group(2)
        token = f"@@LINK{len(links)}@@"
        links.append((label, url))
        return token

    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", hold_link, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for index, (label, url) in enumerate(links):
        safe_label = html.escape(sanitize(label), quote=False)
        safe_url = html.escape(url, quote=True)
        replacement = f'<a href="{safe_url}" color="{CORAL}"><u>{safe_label}</u></a>'
        text = text.replace(f"@@LINK{index}@@", replacement)
    return text


def table_flowable(rows):
    parsed = []
    for row_index, row in enumerate(rows):
        style = STYLES["table-head"] if row_index == 0 else STYLES["table"]
        parsed.append([Paragraph(inline_markup(cell), style) for cell in row])
    cols = len(rows[0])
    first_header = sanitize(rows[0][0]).lower()
    if cols == 2:
        widths = [FRAME_W * 0.34, FRAME_W * 0.66]
    elif cols == 3:
        widths = [FRAME_W * 0.40, FRAME_W * 0.30, FRAME_W * 0.30]
    elif cols == 4:
        widths = [FRAME_W * 0.31, FRAME_W * 0.23, FRAME_W * 0.23, FRAME_W * 0.23]
    else:
        widths = [FRAME_W / cols] * cols
    if "age" in first_header and cols == 4:
        widths = [FRAME_W * 0.14, FRAME_W * 0.285, FRAME_W * 0.285, FRAME_W * 0.29]
    table = LongTable(parsed, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), C_TRUE_BLACK),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "GS-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, 0), 3, C_CORAL),
        ("LINEBELOW", (0, 1), (-1, -2), 0.35, C_G300),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, C_BLACK),
    ]
    for row_index in range(2, len(rows), 2):
        commands.append(("BACKGROUND", (0, row_index), (-1, row_index), C_G100))
    if cols > 2:
        commands.append(("ALIGN", (1, 0), (-1, -1), "RIGHT"))
    table.setStyle(TableStyle(commands))
    return table


FIGURE_MAP = {
    "lifetime-wealth-trajectories": ASSETS / "figure-1-lifetime-trajectories.png",
    "ten-year-head-start": ASSETS / "figure-2-ten-year-head-start.png",
    "expanded-model-lifetime-pressures": ASSETS / "figure-3-lifetime-pressures.png",
}


def image_flowable(path):
    image = Image(str(path))
    max_w = FRAME_W
    if "figure-1" in path.name:
        max_h = 160 * mm
    elif "figure-2" in path.name:
        max_h = 90 * mm
    else:
        max_h = 96 * mm
    scale = min(max_w / image.imageWidth, max_h / image.imageHeight)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    image.hAlign = "CENTER"
    return image


def parse_markdown(lines):
    story = []
    paragraph = []
    i = 0
    part_index = 0

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            joined = " ".join(piece.strip() for piece in paragraph)
            story.append(Paragraph(inline_markup(joined), STYLES["body"]))
            paragraph = []

    while i < len(lines):
        raw = lines[i].rstrip()
        line = raw.strip()
        if not line:
            flush_paragraph()
            i += 1
            continue
        if line == "---":
            flush_paragraph()
            story.extend([Spacer(1, 4), CoralRule(height=2.6), Spacer(1, 8)])
            i += 1
            continue
        if line.startswith("| "):
            flush_paragraph()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
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
            source_path = image_match.group(2)
            mapped = None
            for key, figure_path in FIGURE_MAP.items():
                if key in source_path:
                    mapped = figure_path
                    break
            if mapped is None or not mapped.exists():
                raise FileNotFoundError(f"Missing mapped figure for {source_path}")
            figure_group = [Spacer(1, 6), image_flowable(mapped), Spacer(1, 2)]
            caption_index = i + 1
            while caption_index < len(lines) and not lines[caption_index].strip():
                caption_index += 1
            caption_line = lines[caption_index].strip() if caption_index < len(lines) else ""
            if caption_line.startswith("*Figure ") and caption_line.endswith("*"):
                figure_group.append(Paragraph(inline_markup(caption_line[1:-1]), STYLES["caption"]))
                i = caption_index + 1
            else:
                i += 1
            story.append(KeepTogether(figure_group))
            continue
        if line.startswith("# "):
            flush_paragraph()
            title = sanitize(line[2:].strip())
            if title in ("The Economics of Living Together",):
                i += 1
                continue
            part_index += 1
            if part_index > 1:
                story.append(PageBreak())
            part_label, _, part_title = title.partition(":")
            story.append(SectionBanner(part_title.strip() or title, part_label.strip()))
            story.append(Spacer(1, 11))
            story.append(Paragraph(inline_markup(title), STYLES["h1"]))
            i += 1
            continue
        if line.startswith("## "):
            flush_paragraph()
            title = sanitize(line[3:].strip())
            if title == "From the cohabitation dividend to a hypothetical lifetime model":
                i += 1
                continue
            story.append(Paragraph(inline_markup(title), STYLES["h2"]))
            i += 1
            continue
        if line.startswith("### "):
            flush_paragraph()
            title = sanitize(line[4:].strip())
            heading = Paragraph(f'<font color="{CORAL}">/</font> {inline_markup(title)}', STYLES["h3"])
            story.append(heading)
            i += 1
            continue
        if line.startswith("> "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[2:]), STYLES["quote"]))
            i += 1
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if numbered:
            flush_paragraph()
            story.append(
                Paragraph(
                    f'<font color="{CORAL}"><b>{numbered.group(1)}.</b></font> '
                    f'{inline_markup(numbered.group(2))}',
                    STYLES["number"],
                )
            )
            i += 1
            continue
        if line.startswith("- "):
            flush_paragraph()
            story.append(Paragraph(f'<font color="{CORAL}"><b>-</b></font> {inline_markup(line[2:])}', STYLES["bullet"]))
            i += 1
            continue
        if line.startswith("*Figure ") and line.endswith("*"):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[1:-1]), STYLES["caption"]))
            i += 1
            continue
        paragraph.append(line)
        i += 1

    flush_paragraph()
    return story


def cover_story():
    metrics = Table(
        [
            ["R50,000", "10 YEARS", "R1.9m - R11.3m"],
            ["combined monthly salary", "difference in move-in age", "lead at 75 across scenarios"],
        ],
        colWidths=[FRAME_W / 3] * 3,
        rowHeights=[18 * mm, 13 * mm],
    )
    metrics.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), C_CORAL),
                ("TEXTCOLOR", (0, 0), (-1, -1), C_BLACK),
                ("FONTNAME", (0, 0), (-1, 0), "GS-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 17),
                ("FONTNAME", (0, 1), (-1, 1), "GS-Bold"),
                ("FONTSIZE", (0, 1), (-1, 1), 6.7),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LINEAFTER", (0, 0), (-2, -1), 1, C_BLACK),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return [
        Spacer(1, 44 * mm),
        Paragraph("GREYSCIENX RESEARCH NOTE / ECONOMICS", STYLES["cover-kicker"]),
        CoralRule(width=28 * mm, height=4),
        Spacer(1, 10 * mm),
        Paragraph(
            f'The Economics of <font color="{CORAL}">Living Together</font>',
            STYLES["cover-title"],
        ),
        Paragraph(
            "From the cohabitation dividend to a hypothetical lifetime model for two Gauteng couples, ages 25 to 75.",
            STYLES["cover-subtitle"],
        ),
        Paragraph("SALARIES / R30,000 + R20,000 PER MONTH", STYLES["cover-meta"]),
        Paragraph("SCENARIOS / BEST, AVERAGE AND WORST CASE", STYLES["cover-meta"]),
        Spacer(1, 25 * mm),
        metrics,
        Spacer(1, 7 * mm),
        Paragraph("Version 0.6 | 12 September 2026 | Constant 2026 rand", STYLES["cover-meta"]),
        NextPageTemplate("body"),
        PageBreak(),
    ]


def toc_story():
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOCLevel1",
            fontName="GS-Bold",
            fontSize=10.2,
            leading=15,
            leftIndent=0,
            firstLineIndent=0,
            textColor=C_BLACK,
            spaceBefore=7,
        ),
        ParagraphStyle(
            "TOCLevel2",
            fontName="GS-Regular",
            fontSize=8.7,
            leading=12.2,
            leftIndent=12,
            firstLineIndent=0,
            textColor=C_G700,
            spaceBefore=2,
        ),
        ParagraphStyle(
            "TOCLevel3",
            fontName="GS-Regular",
            fontSize=7.7,
            leading=10.6,
            leftIndent=24,
            firstLineIndent=0,
            textColor=C_G500,
            spaceBefore=1,
        ),
    ]
    return [
        Paragraph("Inside the note", STYLES["toc-title"]),
        CoralRule(width=34 * mm, height=4),
        Spacer(1, 7),
        Paragraph(
            "The first part develops the armchair economic argument. The second tests it with a transparent lifetime scenario rather than presenting the model as a forecast.",
            STYLES["toc-note"],
        ),
        toc,
        PageBreak(),
    ]


def build():
    raw_lines = SOURCE.read_text(encoding="utf-8").splitlines()
    # The title, subtitle and version line are represented on the designed cover.
    start = next(i for i, line in enumerate(raw_lines) if line.startswith("# Part I:"))
    content = parse_markdown(raw_lines[start:])
    story = cover_story() + toc_story() + content
    doc = GreyDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="The Economics of Living Together",
        author="GreyScienx",
        subject="Household consolidation through cohabitation and a Gauteng lifetime model",
        creator="GreyScienx research note",
    )
    doc.multiBuild(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
