#!/usr/bin/env python3
"""Render GreyScienx X/Twitter profile pictures and header from the outlined wordmark."""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import time


SKILL_ASSETS = Path(__file__).resolve().parents[3] / ".agents" / "skills" / "greyscienx-x-editorial" / "assets"
LOGO_LIGHT = SKILL_ASSETS / "greyscienx-logo.svg"
LOGO_DARK = SKILL_ASSETS / "greyscienx-logo-inverse.svg"

# GREY occupies x=0..257 of the 607.813 wordmark; SCIENX occupies the remainder.
# 257 keeps the Y glyph intact (right edge ~256.4) without eating into S.
GREY_WIDTH = 257.0
LOGO_WIDTH = 607.813
LOGO_HEIGHT = 88.0
SCIENX_WIDTH = LOGO_WIDTH - GREY_WIDTH

PROFILE_SIZE = 800
HEADER_SIZE = (1500, 500)


PROFILE_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>GreyScienx X profile</title>
  <style>
    :root {{
      --black: #131200;
      --true-black: #000000;
      --coral: #f26157;
      --white: #fbfffe;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{
      width: {size}px;
      height: {size}px;
      margin: 0;
      overflow: hidden;
      background: {background};
    }}
    #avatar {{
      width: {size}px;
      height: {size}px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: {background};
    }}
    .stack {{
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .row {{
      overflow: hidden;
      height: {letter_h}px;
    }}
    .row img {{
      display: block;
      height: {letter_h}px;
      width: {logo_w}px;
      max-width: none;
    }}
    .grey {{ width: {grey_w}px; }}
    .scienx {{ width: {scienx_w}px; }}
    .scienx img {{ margin-left: -{grey_w}px; }}
    .rule {{
      width: 64px;
      height: 7px;
      margin: 22px 0 24px;
      background: var(--coral);
    }}
  </style>
</head>
<body>
  <div id="avatar">
    <div class="stack">
      <div class="row grey"><img src="{logo}" alt=""></div>
      <div class="rule"></div>
      <div class="row scienx"><img src="{logo}" alt=""></div>
    </div>
  </div>
</body>
</html>
"""


HEADER_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>GreyScienx X header</title>
  <style>
    :root {{
      --black: #131200;
      --true-black: #000000;
      --coral: #f26157;
      --white: #fbfffe;
      --grey-300: #cccccc;
    }}
    * {{ box-sizing: border-box; }}
    html, body, #header {{
      width: 1500px;
      height: 500px;
      margin: 0;
      overflow: hidden;
    }}
    body {{ background: var(--true-black); }}
    #header {{
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 28px;
      padding: 0 80px 18px;
      background: var(--true-black);
      font-family: "Segoe UI", Arial, sans-serif;
    }}
    #header::before {{
      content: "";
      position: absolute;
      inset: 0 0 auto;
      height: 10px;
      background: var(--coral);
    }}
    .logo {{
      display: block;
      width: 980px;
      height: auto;
    }}
    .meta {{
      display: flex;
      align-items: center;
      gap: 18px;
      color: var(--white);
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 0.16em;
      text-transform: uppercase;
    }}
    .division {{ color: var(--coral); }}
    .sep {{
      width: 7px;
      height: 7px;
      background: var(--coral);
    }}
    .url {{ color: var(--white); letter-spacing: 0.12em; }}
  </style>
</head>
<body>
  <div id="header">
    <img class="logo" src="{logo}" alt="GreyScienx">
    <div class="meta">
      <span class="division">Research publication</span>
      <span class="sep"></span>
      <span class="url">greyscienx.com</span>
    </div>
  </div>
</body>
</html>
"""


def browser_candidates() -> list[Path]:
    paths: list[Path] = []
    configured = os.environ.get("GREYSCIENX_BROWSER")
    if configured:
        paths.append(Path(configured))
    for name in ("msedge", "microsoft-edge", "google-chrome", "chrome", "chromium"):
        found = shutil.which(name)
        if found:
            paths.append(Path(found))
    if os.name == "nt":
        paths.extend(
            Path(value)
            for value in (
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            )
        )
    return paths


def find_browser(explicit: str | None) -> Path:
    if explicit:
        candidate = Path(explicit).expanduser().resolve()
        if candidate.is_file():
            return candidate
        raise FileNotFoundError(f"Browser executable not found: {candidate}")
    for candidate in browser_candidates():
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("No Chromium browser found. Set GREYSCIENX_BROWSER or pass --browser.")


def data_uri(path: Path) -> str:
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/svg+xml;base64,{payload}"


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Renderer did not produce a valid PNG: {path}")
    return struct.unpack(">II", data[16:24])


def screenshot(browser: Path, html: str, output: Path, width: int, height: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="greyscienx-x-profile-") as tmp:
        working_html = Path(tmp) / "asset.html"
        working_html.write_text(html, encoding="utf-8")
        command = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={output}",
            working_html.as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
        deadline = time.monotonic() + 10
        while not output.is_file() and time.monotonic() < deadline:
            time.sleep(0.1)
        if not output.is_file():
            raise RuntimeError("Browser exited before writing the PNG")
    got = png_size(output)
    if got != (width, height):
        raise ValueError(f"Expected {width}x{height}; got {got[0]}x{got[1]} for {output.name}")


def profile_html(logo: str, background: str, size: int) -> str:
    letter_h = 120
    scale = letter_h / LOGO_HEIGHT
    return PROFILE_HTML.format(
        size=size,
        background=background,
        logo=logo,
        letter_h=letter_h,
        logo_w=round(LOGO_WIDTH * scale, 3),
        grey_w=round(GREY_WIDTH * scale, 3),
        scienx_w=round(SCIENX_WIDTH * scale, 3),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", help="Path to Edge, Chrome, or Chromium")
    parser.add_argument("--out", help="Output directory; defaults to this script's directory")
    args = parser.parse_args()

    if not LOGO_LIGHT.is_file() or not LOGO_DARK.is_file():
        raise FileNotFoundError(f"Wordmarks not found in {SKILL_ASSETS}")

    out = Path(args.out).expanduser().resolve() if args.out else Path(__file__).resolve().parent
    browser = find_browser(args.browser)
    light = data_uri(LOGO_LIGHT)
    dark = data_uri(LOGO_DARK)

    jobs = [
        ("profile-light.png", profile_html(light, "#fbfffe", PROFILE_SIZE), PROFILE_SIZE, PROFILE_SIZE),
        ("profile-dark.png", profile_html(dark, "#000000", PROFILE_SIZE), PROFILE_SIZE, PROFILE_SIZE),
        ("header.png", HEADER_HTML.format(logo=dark), HEADER_SIZE[0], HEADER_SIZE[1]),
    ]

    reports = []
    for name, html, width, height in jobs:
        output = out / name
        screenshot(browser, html, output, width, height)
        reports.append(
            {
                "output": str(output),
                "width": width,
                "height": height,
                "bytes": output.stat().st_size,
            }
        )
    print(json.dumps(reports, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
