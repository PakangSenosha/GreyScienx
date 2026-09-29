"""Generate deterministic QA records for the final Inherited Geography PDF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PDF = ROOT / "research/publications/inherited-geography-racial-property-wealth-dividend.pdf"
TEXT = HERE / "extracted-text.txt"
QA = HERE / "qa"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def image_count(page) -> int:
    resources = page.get("/Resources")
    if not resources:
        return 0
    resources = resources.get_object()
    xobjects = resources.get("/XObject")
    if not xobjects:
        return 0
    return sum(
        1
        for obj in xobjects.get_object().values()
        if obj.get_object().get("/Subtype") == "/Image"
    )


def link_count(page) -> int:
    annotations = page.get("/Annots") or []
    return sum(
        1
        for annotation in annotations
        if annotation.get_object().get("/Subtype") == "/Link"
    )


def link_targets(page) -> list[str]:
    targets = []
    for annotation in page.get("/Annots") or []:
        annotation = annotation.get_object()
        if annotation.get("/Subtype") != "/Link":
            continue
        action = annotation.get("/A")
        if action:
            uri = action.get_object().get("/URI")
            if uri:
                targets.append(str(uri))
    return targets


def main() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(PDF))
    metadata = reader.metadata or {}
    first = reader.pages[0]
    width_pt = float(first.mediabox.width)
    height_pt = float(first.mediabox.height)

    metadata_report = {
        "file": str(PDF),
        "bytes": PDF.stat().st_size,
        "sha256": sha256(PDF),
        "pages": len(reader.pages),
        "encrypted": reader.is_encrypted,
        "page_size_points": [round(width_pt, 3), round(height_pt, 3)],
        "page_size_mm": [round(width_pt * 25.4 / 72, 2), round(height_pt * 25.4 / 72, 2)],
        "metadata": {
            "title": metadata.get("/Title"),
            "author": metadata.get("/Author"),
            "subject": metadata.get("/Subject"),
            "creator": metadata.get("/Creator"),
            "producer": metadata.get("/Producer"),
        },
    }
    (QA / "metadata.json").write_text(
        json.dumps(metadata_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    text = TEXT.read_text(encoding="utf-8", errors="replace")
    required = [
        "Inherited Geography",
        "PART I: The answer",
        "PART V: Matched descendants",
        "PART VII: Agricultural property",
        "PART XI: Limits and falsification",
        "PART XII: Final answer",
        "APPENDIX: Model reading guide",
        "References",
    ] + [f"Figure {number}." for number in range(1, 9)]
    forbidden = ["TODO", "TBD", "PLACEHOLDER", "turn0search", "turn1search"]
    text_report = {
        "characters": len(text),
        "words": len(text.split()),
        "required_strings": {item: item in text for item in required},
        "forbidden_strings": {item: item in text for item in forbidden},
        "all_required_present": all(item in text for item in required),
        "no_forbidden_present": not any(item in text for item in forbidden),
    }
    (QA / "text-check.json").write_text(
        json.dumps(text_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    inventory = []
    for number, page in enumerate(reader.pages, start=1):
        inventory.append(
            {
                "page": number,
                "images": image_count(page),
                "links": link_count(page),
                "external_links": len(link_targets(page)),
                "text_characters": len(page.extract_text() or ""),
            }
        )
    (QA / "render-inventory.json").write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    citations = json.loads((HERE / "citations.json").read_text(encoding="utf-8"))
    expected_urls = sorted({item["url"] for item in citations})
    reference_annotations = link_targets(reader.pages[-1])
    reference_urls = sorted(set(reference_annotations))
    reference_link_report = {
        "reference_page": len(reader.pages),
        "bibliography_entries": len(citations),
        "link_annotations": len(reference_annotations),
        "unique_external_urls": len(reference_urls),
        "expected_urls": expected_urls,
        "linked_urls": reference_urls,
        "missing_urls": sorted(set(expected_urls) - set(reference_urls)),
        "unexpected_urls": sorted(set(reference_urls) - set(expected_urls)),
        "all_references_linked": set(expected_urls) == set(reference_urls),
    }
    (QA / "reference-link-check.json").write_text(
        json.dumps(reference_link_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    tracked = [
        PDF,
        HERE / "model.py",
        HERE / "model_results.json",
        HERE / "parameters.csv",
        HERE / "citations.json",
        HERE / "manuscript.md",
        HERE / "sources.md",
        HERE / "data-notes.md",
    ]
    checksum_lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in tracked]
    (QA / "checksums.sha256").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {"metadata": metadata_report, "text": text_report, "references": reference_link_report},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
