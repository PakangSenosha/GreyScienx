#!/usr/bin/env python3
"""Render one GreyScienx social card from a JSON specification."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import time


WIDTH = 1080
HEIGHT = 1350
REQUIRED = ("edition", "eyebrow", "headline", "caption", "source", "url")


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


def image_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Renderer did not produce a valid PNG: {path}")
    return struct.unpack(">II", data[16:24])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", help="JSON card specification")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument("--browser", help="Path to Edge, Chrome, or Chromium")
    parser.add_argument("--html-out", help="Also keep the generated HTML at this path")
    args = parser.parse_args()

    spec_path = Path(args.spec).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    missing = [key for key in REQUIRED if not str(data.get(key, "")).strip()]
    if missing:
        raise ValueError(f"Missing required card fields: {', '.join(missing)}")
    visual_count = sum(bool(data.get(key)) for key in ("chartImage", "stat", "bars"))
    if visual_count != 1:
        raise ValueError("Specify exactly one of chartImage, stat, or bars")
    if data.get("chartImage"):
        chart_path = Path(data["chartImage"])
        if not chart_path.is_absolute():
            chart_path = (spec_path.parent / chart_path).resolve()
        if not chart_path.is_file():
            raise FileNotFoundError(f"Chart image not found: {chart_path}")
        data["chartImage"] = image_data_uri(chart_path)

    template_path = Path(__file__).resolve().parents[1] / "assets" / "social-card.html"
    assets_path = template_path.parent
    template = template_path.read_text(encoding="utf-8")
    logo_light = image_data_uri(assets_path / "greyscienx-logo.svg")
    logo_dark = image_data_uri(assets_path / "greyscienx-logo-inverse.svg")
    safe_json = json.dumps(data, ensure_ascii=False).replace("</script", "<\\/script")
    html = (
        template.replace("__CARD_DATA__", safe_json)
        .replace("__LOGO_LIGHT__", logo_light)
        .replace("__LOGO_DARK__", logo_dark)
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.unlink(missing_ok=True)

    with tempfile.TemporaryDirectory(prefix="greyscienx-social-") as tmp:
        working_html = Path(tmp) / "card.html"
        working_html.write_text(html, encoding="utf-8")
        browser = find_browser(args.browser)
        command = [str(browser), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", f"--window-size={WIDTH},{HEIGHT}", f"--screenshot={output_path}", working_html.as_uri()]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
        deadline = time.monotonic() + 10
        while not output_path.is_file() and time.monotonic() < deadline:
            time.sleep(0.1)
        if not output_path.is_file():
            raise RuntimeError("Browser exited before writing the PNG")

    if args.html_out:
        kept_html = Path(args.html_out).expanduser().resolve()
        kept_html.parent.mkdir(parents=True, exist_ok=True)
        kept_html.write_text(html, encoding="utf-8")

    width, height = png_size(output_path)
    if (width, height) != (WIDTH, HEIGHT):
        raise ValueError(f"Expected {WIDTH}x{HEIGHT}; got {width}x{height}")
    size_bytes = output_path.stat().st_size
    if size_bytes > 5_000_000:
        raise ValueError(f"PNG exceeds ordinary X image limit: {size_bytes} bytes")
    print(json.dumps({"output": str(output_path), "width": width, "height": height, "bytes": size_bytes}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
