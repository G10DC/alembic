#!/usr/bin/env python3
"""
chunk.py — Split an oversized section (from extract.py's manifest, one whose
word count is too large to condense in one pass) into paragraph-aligned
chunks of roughly --max-words each, and rewrite that entry into the manifest
as multiple chunk entries.

Usage:
    python3 chunk.py <section_txt_file> --outdir <dir_containing_manifest.json> [--max-words 4000]
"""

import argparse
import json
from pathlib import Path


def word_count(text):
    return len(text.split())


def chunk_paragraphs(text, max_words=4000):
    """Split text into paragraph-aligned chunks, each at most ~max_words words
    (a chunk can exceed max_words only if a single paragraph does)."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current_chunk = []
    current_words = 0

    for p in paragraphs:
        p_words = word_count(p)
        if current_words + p_words > max_words and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_words = p_words
        else:
            current_chunk.append(p)
            current_words += p_words

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def chunk_title(chunk_text, index):
    lines = chunk_text.splitlines()
    first_line = lines[0].strip() if lines else ""
    title = first_line[:50] if first_line else f"Chunk {index}"
    return title


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("section_file", help="Path to the oversized section .txt file to split")
    parser.add_argument("--outdir", required=True, help="Directory containing sections/ and manifest.json")
    parser.add_argument("--max-words", type=int, default=4000, help="Target max words per chunk")
    args = parser.parse_args()

    src_file = Path(args.section_file)
    outdir = Path(args.outdir)
    sec_dir = outdir / "sections"
    sec_dir.mkdir(parents=True, exist_ok=True)

    text = src_file.read_text(encoding="utf-8")
    chunks = chunk_paragraphs(text, args.max_words)

    # Remove the original oversized file now that it's split.
    src_file.unlink()

    new_entries = []
    for i, chunk_text in enumerate(chunks, start=1):
        fname = f"{i:03d}_chunk_{i:02d}.txt"
        path = sec_dir / fname
        path.write_text(chunk_text, encoding="utf-8")
        title = chunk_title(chunk_text, i)
        new_entries.append({
            "index": i,
            "title": f"Section {i} - {title}" if title else f"Section {i}",
            "path": str(path),
            "word_count": word_count(chunk_text),
            "detection_method": "paragraph_window",
        })

    manifest_path = outdir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
    manifest.extend(new_entries)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Split {src_file.name} into {len(new_entries)} chunks.")


if __name__ == "__main__":
    main()
