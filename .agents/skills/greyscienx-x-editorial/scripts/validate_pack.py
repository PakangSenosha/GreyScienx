#!/usr/bin/env python3
"""Validate the structural and editorial invariants of a GreyScienx X pack."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to manifest.json")
    args = parser.parse_args()
    manifest_path = Path(args.manifest).expanduser().resolve()
    pack = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    publication = pack.get("publication") or {}
    paper_url = str(publication.get("url") or "").strip()
    if not publication.get("title"):
        errors.append("publication.title is required")
    if not paper_url.startswith("https://"):
        errors.append("publication.url must be a stable HTTPS URL")

    posts = pack.get("posts") or []
    claims = pack.get("claims") or []
    claim_ids = {str(claim.get("id")) for claim in claims if claim.get("id")}
    if len(posts) < 10:
        errors.append(f"at least 10 posts are required; found {len(posts)}")
    long_posts = [post for post in posts if post.get("type") == "long"]
    short_posts = [post for post in posts if post.get("type") == "short"]
    if len(long_posts) < 1:
        errors.append("at least one long post is required")
    if len(short_posts) < 9:
        errors.append(f"at least nine short posts are required; found {len(short_posts)}")

    seen_copy: set[str] = set()
    for index, post in enumerate(posts, 1):
        post_id = str(post.get("id") or index)
        copy = str(post.get("copy") or "").strip()
        normalized = " ".join(copy.lower().split())
        if not copy:
            errors.append(f"post {post_id}: copy is required")
        elif normalized in seen_copy:
            errors.append(f"post {post_id}: duplicate copy")
        seen_copy.add(normalized)
        if post.get("type") == "short" and len(copy) > 280:
            errors.append(f"post {post_id}: short copy is {len(copy)} characters")
        if post.get("type") == "long" and not (281 <= len(copy) <= 25_000):
            errors.append(f"post {post_id}: long copy must be 281–25,000 characters; found {len(copy)}")
        if paper_url and paper_url not in copy:
            errors.append(f"post {post_id}: full paper URL is missing from copy")
        image = str(post.get("image") or "").strip()
        if not image:
            errors.append(f"post {post_id}: image is required")
        elif not (manifest_path.parent / image).is_file():
            errors.append(f"post {post_id}: image not found: {image}")
        if len(str(post.get("alt") or "").strip()) < 20:
            errors.append(f"post {post_id}: useful alt text is required")
        linked_claims = post.get("claim_ids") or []
        if not linked_claims:
            errors.append(f"post {post_id}: claim_ids are required")
        for claim_id in linked_claims:
            if str(claim_id) not in claim_ids:
                errors.append(f"post {post_id}: unknown claim ID {claim_id}")

    for claim in claims:
        claim_id = str(claim.get("id") or "<missing>")
        if not claim.get("source"):
            errors.append(f"claim {claim_id}: source is required")
        if claim.get("checked") is not True:
            errors.append(f"claim {claim_id}: checked must be true")

    if errors:
        print("Pack validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Pack valid: {len(posts)} posts, {len(short_posts)} short, {len(long_posts)} long, {len(claims)} checked claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

