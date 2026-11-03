#!/usr/bin/env python3
"""
chunk.py — Spezza una sezione troppo lunga (dal manifest di extract.py) in
blocchi allineati ai paragrafi di circa --max-words parole. Il file originale
NON viene cancellato: finisce in sections/_split/ (che coverage.py non legge,
così il testo non è contato due volte); nel manifest la sua voce è sostituita
dai nuovi blocchi e gli indici sono rinumerati da 1 senza collisioni. Un secondo
lancio sullo stesso percorso dà errore (il file non c'è più).

Uso:
    python chunk.py <file_sezione.txt> --outdir <cartella_con_manifest.json> [--max-words 4000]
"""

import argparse
import json
import shutil
import sys
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
    parser.add_argument("section_file", help="Percorso del file .txt della sezione da spezzare")
    parser.add_argument("--outdir", required=True, help="Cartella con sections/ e manifest.json")
    parser.add_argument("--max-words", type=int, default=4000, help="Parole massime per blocco")
    args = parser.parse_args()

    src_file = Path(args.section_file)
    outdir = Path(args.outdir)
    sec_dir = outdir / "sections"
    sec_dir.mkdir(parents=True, exist_ok=True)

    if not src_file.is_file():
        done = sec_dir / "_split" / src_file.name
        hint = f" (già spezzato? l'originale è in {done})" if done.is_file() else ""
        sys.exit(f"Errore: file non trovato: {src_file}{hint}")

    text = src_file.read_text(encoding="utf-8")
    chunks = chunk_paragraphs(text, args.max_words)
    if len(chunks) <= 1:
        print(f"{src_file.name}: nessuna divisione necessaria (max {args.max_words} parole).")
        return

    manifest_path = outdir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []

    # Voce originale da sostituire (confronto sui percorsi risolti).
    src_resolved = src_file.resolve()
    pos = next((i for i, m in enumerate(manifest) if Path(m["path"]).resolve() == src_resolved), None)
    base_title = manifest[pos]["title"] if pos is not None else None

    # Nomi derivati dal file d'origine: nessuna collisione con altre sezioni.
    new_entries = []
    for i, chunk_text in enumerate(chunks, start=1):
        path = sec_dir / f"{src_file.stem}_parte_{i:02d}.txt"
        path.write_text(chunk_text, encoding="utf-8")
        title = f"{base_title} (parte {i}/{len(chunks)})" if base_title else chunk_title(chunk_text, i)
        new_entries.append({
            "index": 0,  # assegnato sotto
            "title": title,
            "path": str(path),
            "word_count": word_count(chunk_text),
            "detection_method": "paragraph_window",
        })

    if pos is None:
        manifest.extend(new_entries)
    else:
        manifest[pos:pos + 1] = new_entries
    for n, entry in enumerate(manifest, start=1):
        entry["index"] = n
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # L'originale esce da sections/ (coverage.py legge i *.txt di quella cartella).
    split_dir = sec_dir / "_split"
    split_dir.mkdir(exist_ok=True)
    dest = split_dir / src_file.name
    shutil.move(str(src_file), str(dest))

    print(f"{src_file.name} spezzato in {len(new_entries)} blocchi (originale spostato in {dest}).")
    print(f"Manifest aggiornato: {manifest_path} ({len(manifest)} voci).")


if __name__ == "__main__":
    main()
