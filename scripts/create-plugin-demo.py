from __future__ import annotations

import json
import textwrap
import urllib.request
from pathlib import Path

import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public" / "media" / "greyscienx-chatgpt-demo.mp4"
ICON = ROOT / "public" / "brand" / "greyscienx-app-icon.png"
WIDTH, HEIGHT = 1920, 1080
FPS = 12

INK = "#131200"
TRUE_BLACK = "#000000"
CORAL = "#f26157"
WHITE = "#fbfffe"
GREY_100 = "#f0f1f2"
GREY_300 = "#cccccc"
GREY_500 = "#777777"
GREY_700 = "#3d3d3d"
MINT = "#72d2b3"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    family = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / family), size)


F_SMALL = font(28)
F_BODY = font(38)
F_BODY_BOLD = font(38, True)
F_LABEL = font(25, True)
F_TITLE = font(70, True)
F_HERO = font(88, True)


def live_search() -> dict:
    request_body = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "search_research",
            "arguments": {"query": "retirement at 60 worker retiree ratio"},
        },
    }
    request = urllib.request.Request(
        "https://greyscienx.com/mcp",
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "MCP-Protocol-Version": "2025-03-26",
            "User-Agent": "GreyScienx-Plugin-Demo/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return json.loads(payload["result"]["content"][0]["text"])


def base_frame(step: int, title: str, kicker: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 78), fill=INK)
    draw.rectangle((0, 78, 24, HEIGHT), fill=CORAL)
    draw.text((68, 23), "GREYSCIEnX", font=F_LABEL, fill=WHITE)
    draw.text((WIDTH - 335, 23), f"DEMO  •  {step:02d} / 06", font=F_LABEL, fill=GREY_300)
    draw.text((82, 142), kicker.upper(), font=F_LABEL, fill=CORAL)
    draw.text((82, 185), title, font=F_TITLE, fill=INK)
    draw.line((82, 286, WIDTH - 82, 286), fill=INK, width=3)
    return image, draw


def wrap(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], width_chars: int, *, fill=GREY_700, line_gap=16, f=F_BODY):
    x, y = xy
    for line in textwrap.wrap(text, width=width_chars):
        draw.text((x, y), line, font=f, fill=fill)
        y += f.size + line_gap
    return y


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, accent: str = CORAL):
    x1, y1, x2, y2 = box
    draw.rectangle(box, fill=GREY_100, outline=INK, width=3)
    draw.rectangle((x1, y1, x2, y1 + 10), fill=accent)
    draw.text((x1 + 30, y1 + 32), label.upper(), font=F_LABEL, fill=GREY_500)


def frames(search: dict) -> list[Image.Image]:
    result = search["results"][0]
    claim = result["most_relevant_claim"]
    output: list[Image.Image] = []

    image = Image.new("RGB", (WIDTH, HEIGHT), INK)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 18), fill=CORAL)
    icon = Image.open(ICON).convert("RGBA").resize((170, 170))
    image.paste(icon, (92, 110), icon)
    draw.text((92, 340), "GREYSCIEnX", font=F_LABEL, fill=CORAL)
    draw.text((92, 400), "Research that agents can inspect,", font=F_HERO, fill=WHITE)
    draw.text((92, 505), "trace and challenge.", font=F_HERO, fill=WHITE)
    draw.text((96, 675), "PUBLIC PLUGIN REVIEW DEMONSTRATION", font=F_LABEL, fill=GREY_300)
    draw.text((96, 735), "Live read-only MCP  •  22 tools  •  No authentication", font=F_BODY, fill=GREY_300)
    draw.text((96, 960), "greyscienx.com/mcp", font=F_SMALL, fill=MINT)
    output.append(image)

    image, draw = base_frame(2, "Connect the verified public server", "Developer mode")
    panel(draw, (82, 340, 1838, 825), "Connection")
    draw.text((125, 430), "Server URL", font=F_LABEL, fill=GREY_500)
    draw.text((125, 478), "https://greyscienx.com/mcp", font=F_BODY_BOLD, fill=INK)
    draw.text((125, 580), "Authentication", font=F_LABEL, fill=GREY_500)
    draw.text((125, 628), "None — the corpus is public and read-only", font=F_BODY, fill=INK)
    draw.text((1000, 430), "Discovery", font=F_LABEL, fill=GREY_500)
    draw.text((1000, 478), "22 tools detected", font=F_BODY_BOLD, fill=INK)
    draw.text((1000, 580), "Safety annotations", font=F_LABEL, fill=GREY_500)
    draw.text((1000, 628), "Read-only  •  Closed corpus  •  Non-destructive", font=F_BODY, fill=INK)
    output.append(image)

    image, draw = base_frame(3, "Ask a research question", "ChatGPT prompt")
    panel(draw, (82, 340, 1838, 760), "User")
    wrap(
        draw,
        "Find GreyScienx research about retirement sustainability and explain the assumptions behind the main result.",
        (130, 455),
        66,
        fill=INK,
        f=font(48, True),
        line_gap=24,
    )
    draw.text((125, 850), "The model can search by topic, title, claim, assumption or identifier.", font=F_BODY, fill=GREY_700)
    output.append(image)

    image, draw = base_frame(4, "The plugin chooses a bounded search tool", "Tool call")
    panel(draw, (82, 340, 1838, 830), "search_research", accent=MINT)
    draw.text((125, 430), "INPUT", font=F_LABEL, fill=GREY_500)
    draw.rounded_rectangle((125, 482, 1785, 585), radius=12, fill=TRUE_BLACK)
    draw.text((155, 515), 'query: "retirement at 60 worker retiree ratio"', font=F_BODY, fill=WHITE)
    draw.text((125, 655), "EXECUTION BOUNDARY", font=F_LABEL, fill=GREY_500)
    draw.text((125, 705), "Packaged GreyScienx registry only — no web browsing, no writes, no publication.", font=F_BODY, fill=INK)
    output.append(image)

    image, draw = base_frame(5, "A modelled result with its evidence boundary", "Live MCP response")
    panel(draw, (82, 332, 1838, 900), result["id"], accent=CORAL)
    draw.text((125, 410), result["title"], font=font(52, True), fill=INK)
    draw.text((125, 492), "PRIMARY QUESTION", font=F_LABEL, fill=GREY_500)
    wrap(draw, result["primary_question"], (125, 540), 76, fill=INK, f=F_BODY_BOLD)
    draw.text((125, 650), "MOST RELEVANT CLAIM", font=F_LABEL, fill=GREY_500)
    wrap(draw, claim["claim"], (125, 700), 100, fill=GREY_700, f=font(31), line_gap=12)
    draw.text((125, 944), f"Evidence status: {result['evidence_status']}  •  Claim type: {claim['claim_type']}", font=F_SMALL, fill=CORAL)
    output.append(image)

    image, draw = base_frame(6, "Ready for public review", "Verification")
    rows = [
        ("Live server", "https://greyscienx.com/mcp"),
        ("Verified domain", "greyscienx.com"),
        ("Search result", f"{result['id']} — {result['title']}"),
        ("Traceability", "Claims, assumptions, results, sources and limitations"),
        ("User impact", "Retrieval and analysis only; no data is stored or changed"),
    ]
    y = 350
    for label, value in rows:
        draw.line((82, y, 1838, y), fill=GREY_300, width=2)
        draw.text((90, y + 26), label.upper(), font=F_LABEL, fill=GREY_500)
        draw.text((460, y + 20), value, font=F_BODY_BOLD, fill=INK)
        y += 115
    draw.rectangle((82, 955, 1838, 1030), fill=INK)
    draw.text((115, 974), "GREYSCIEnX  •  TRACE EVIDENCE AND MODELS", font=F_LABEL, fill=WHITE)
    output.append(image)
    return output


def write_video(slides: list[Image.Image]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    writer = imageio.get_writer(
        OUTPUT,
        fps=FPS,
        codec="libx264",
        quality=8,
        macro_block_size=None,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
    )
    try:
        seconds = [3.0, 3.4, 3.4, 3.8, 5.2, 4.0]
        for slide, duration in zip(slides, seconds):
            frame = slide.convert("RGB")
            for _ in range(round(duration * FPS)):
                writer.append_data(__import__("numpy").array(frame))
    finally:
        writer.close()


def main() -> None:
    search = live_search()
    slides = frames(search)
    write_video(slides)
    print(f"Created {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
