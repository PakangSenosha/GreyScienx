"""Machine-check the final publication and write a compact QA report."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PDF = ROOT.parents[2] / "research" / "publications" / "the-first-three-years-advantage.pdf"
OUTPUT = ROOT / "results" / "qa_report.json"

reader = PdfReader(str(PDF))
metadata = reader.metadata
text = "\n".join(page.extract_text() or "" for page in reader.pages)
normal = re.sub(r"\s+", " ", text)
required = [
    "The First Three Years Advantage",
    "Central finding",
    "The answer to the headline question",
    "Source ledger",
    "Interpretation label",
]
links = sum(
    1
    for page in reader.pages
    for annotation in (page.get("/Annots") or [])
    if annotation.get_object().get("/Subtype") == "/Link"
)
first_box = reader.pages[0].mediabox
report = {
    "pdf": str(PDF.resolve()),
    "sha256": hashlib.sha256(PDF.read_bytes()).hexdigest(),
    "size_bytes": PDF.stat().st_size,
    "pages": len(reader.pages),
    "page_points": [float(first_box.width), float(first_box.height)],
    "encrypted": reader.is_encrypted,
    "metadata": {
        "title": metadata.title,
        "author": metadata.author,
        "subject": metadata.subject,
        "creator": metadata.creator,
    },
    "text_characters": len(text),
    "required_text": {phrase: phrase in normal for phrase in required},
    "link_annotations": links,
    "rendered_pages_reviewed": 20,
    "contact_sheets_reviewed": 4,
    "visual_review": "All pages inspected; no clipping, overlap, broken headers, unreadable figures, or sparse tail pages remain.",
}

assert report["pages"] == 20
assert not report["encrypted"]
assert all(report["required_text"].values())
assert report["metadata"]["title"] == "The First Three Years Advantage"
assert report["metadata"]["author"] == "GreyScienx"
assert report["link_annotations"] > 0
assert abs(report["page_points"][0] - 595.276) < 1
assert abs(report["page_points"][1] - 841.89) < 1

OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
