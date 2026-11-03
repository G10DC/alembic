#!/usr/bin/env python3
"""
merge.py — Unisce i file chunk_<N>.md in un'unica guida di studio nel formato
condiviso (vedi references/format.md): un solo "# Titolo", indice, capitoli
"## N. Titolo", sezione "## Domande di verifica" e "## Glossario" generato
dalle righe "**Termine**: definizione."

Uso:
    python merge.py <cartella_chunk> --output guida.md [--title "Titolo"]
"""

import argparse
import re
import sys
from pathlib import Path

CHUNK_NAME = re.compile(r"^chunk_(\d+)\.md$")
QUESTIONS_HEADING = re.compile(r"^(#{2,3})\s+Domande di verifica\s*$", re.IGNORECASE)
# Definizione: riga che INIZIA con "**Termine**:" (dopo un eventuale "- " o "* ").
DEFINITION_LINE = re.compile(r"^(?:[-*•]\s+)?\*\*([^*]+)\*\*\s*:\s*(.*)$")
MARKERS = ("🔴", "🟡", "🟢")


def extract_terms_from_text(text, section_idx):
    """Raccoglie le definizioni: solo righe "**Termine**: definizione" (anche come
    voce di elenco). Niente grassetti in mezzo alla frase né marcatori di priorità."""
    terms = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = DEFINITION_LINE.match(line)
        if not m:
            continue
        term, definition = m.group(1).strip(), m.group(2).strip()
        if any(mk in definition for mk in MARKERS):
            continue
        definition = re.sub(
            r"^(si\s+definisce\s+come|significa|è|significano|sono|si\s+intende\s+per|si\s+riferisce\s+a)\s+",
            "", definition, flags=re.IGNORECASE).strip()
        if term and len(definition) > 3:
            terms.setdefault(term, []).append(definition)
    return terms


def github_slug(heading):
    """Ancora in stile GitHub: minuscolo, via la punteggiatura (restano lettere
    accentate, cifre, '-' e '_'), spazi in '-'."""
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def split_questions(content):
    """Separa il blocco 'Domande di verifica' dal corpo del capitolo."""
    body, questions = [], []
    level = None
    for line in content.splitlines():
        m = QUESTIONS_HEADING.match(line)
        if m:
            level = len(m.group(1))
            continue
        if level is not None:
            h = re.match(r"^(#+)\s", line)
            if h and len(h.group(1)) <= level:
                level = None
            else:
                questions.append(line)
                continue
        body.append(line)
    return "\n".join(body).strip(), [q.strip() for q in questions if q.strip()]


def list_chunks(condensed_dir, output):
    if not condensed_dir.is_dir():
        sys.exit(f"Errore: cartella non trovata: {condensed_dir}")
    files = sorted(f for f in condensed_dir.glob("*.md") if f.resolve() != output.resolve())
    bad = [f.name for f in files if not CHUNK_NAME.match(f.name)]
    if bad:
        sys.exit(
            "Errore: nomi file non conformi (atteso chunk_<N>.md, es. chunk_1.md): "
            + ", ".join(bad)
        )
    if not files:
        sys.exit(f"Errore: nessun file chunk_<N>.md in {condensed_dir}")
    return sorted(files, key=lambda p: int(CHUNK_NAME.match(p.name).group(1)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("condensed_dir", help="Cartella con i file chunk_<N>.md")
    parser.add_argument("--output", required=True, help="Percorso del file Markdown da scrivere")
    parser.add_argument("--title", default="Guida di studio",
                        help="Titolo della guida (consigliato: nome del libro o della dispensa)")
    args = parser.parse_args()

    chunk_files = list_chunks(Path(args.condensed_dir), Path(args.output))

    chapters, toc, questions_out = [], [], []
    glossary = {}
    seen_slugs = {}

    for idx, path in enumerate(chunk_files, start=1):
        body, questions = split_questions(path.read_text(encoding="utf-8"))
        lines = body.splitlines()

        # Intestazione del capitolo: "## N. Titolo". Se manca o non è numerata la sistemo.
        pos = next((i for i, l in enumerate(lines) if l.startswith("## ")), None)
        if pos is None:
            lines.insert(0, f"## {idx}. Sezione {idx}")
            pos = 0
        heading = lines[pos][3:].strip()
        if not re.match(r"^\d+\.\s", heading):
            heading = f"{idx}. {heading}"
            lines[pos] = f"## {heading}"
        body = "\n".join(lines)
        chapters.append(body)

        slug = github_slug(heading)
        n = seen_slugs.get(slug, 0)
        seen_slugs[slug] = n + 1
        toc.append(f"- [{heading}](#{slug}{f'-{n}' if n else ''})")

        if questions:
            block = [f"### Domande — {re.sub(r'^\d+\.\s*', '', heading)}", ""]
            for q in questions:
                if q.startswith("Domanda:") and block[-1] != "":
                    block.append("")
                block.append(q)
            questions_out.append("\n".join(block))

        for term, defs in extract_terms_from_text(body, idx).items():
            entry = glossary.setdefault(term.lower(), {"term": term, "defs": []})
            entry["defs"].extend((idx, d) for d in defs)

    out = [f"# {args.title}", "## Indice\n\n" + "\n".join(toc), "\n\n".join(chapters)]
    if questions_out:
        out.append("## Domande di verifica\n\n" + "\n\n".join(questions_out))

    if glossary:
        gl = ["## Glossario"]
        for key in sorted(glossary):
            info = glossary[key]
            unique, seen = [], set()
            for sec, d in info["defs"]:
                if d.lower() not in seen:
                    seen.add(d.lower())
                    unique.append((sec, d))
            for sec, d in unique:
                d = d if d.endswith((".", "!", "?")) else d + "."
                label = f" (cap. {sec})" if len(unique) > 1 else ""
                gl.append(f"**{info['term']}**: {d}{label}")
        out.append("\n\n".join(gl))

    Path(args.output).write_text("\n\n".join(out) + "\n", encoding="utf-8")
    print(f"Guida scritta in {args.output}: {len(chapters)} capitoli, {len(glossary)} termini nel glossario.")


if __name__ == "__main__":
    main()
