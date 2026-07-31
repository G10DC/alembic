#!/usr/bin/env python3
"""
keyword_coverage.py — Flags high-frequency, non-generic terms from the
original book text that are missing from the condensed Markdown output.

This is a recall net, not a verdict: the orchestrating agent should skim the
flagged list and judge which misses are real (a dropped concept) vs. noise
(a one-off character name, boilerplate).

Usage:
    python3 keyword_coverage.py --original <dir_or_file> --condensed <file.md> \
        --report <out.json> [--top-n 150] [--min-len 4]
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path

STOPWORDS = set(
    """
    a ad al alla alle allo agli allora altre altri altro anche ancora avere aveva
    avevano ben che chi ci cioe come con contro cui da dai dal dalla dalle dallo
    degli dei del della delle dello dentro di dov dove e ecco ed egli era erano
    esse essere essi fare fatto fino fra gia giu gli ha hai hanno ho il in
    invece io la le lei lo loro lui ma mentre mio molta molti molto nei nel
    nella nelle nello nessuna nessuno niente no noi non nostra nostre nostri
    nostro o ogni oppure ora ove per perche però piu poco proprio puo quale
    quali quando quanta quante quanti quanto quasi quella quelle quelli quello
    questa queste questi questo qui quindi se sei sembra sempre senza si sia
    sono sopra sotto sta stai stando stata state stati stato stesso su sua
    subito sue sugli sui sul sulla sulle sullo suo suoi tra tuo tua tue tuoi
    tutta tutte tutti tutto un una uno vai vostra vostre vostri vostro
    the and or of to in a is are was were be been being this that these those
    with for on at by from as it its it's not but if then than so such can
    could would should will shall may might must about into over under again
    further once here there when where why how all any both each few more
    most other some such no nor only own same too very s t just don now
    """.split()
)


def tokenize(text):
    # Split Italian elisions (l', d', dell', un', sull', ...) so "l'energia"
    # yields "energia", not the glued "l'energia". Keep internal hyphens.
    text = re.sub(r"\b[a-zA-Zà-öø-ÿ]{1,4}'", " ", text)
    return re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ-]+", text.lower())


def significant_terms(text, min_len=4):
    tokens = tokenize(text)
    return [t for t in tokens if len(t) >= min_len and t not in STOPWORDS]


def load_original(original_path):
    p = Path(original_path)
    if p.is_dir():
        texts = []
        for f in sorted(p.glob("*.txt")):
            texts.append(f.read_text(encoding="utf-8", errors="ignore"))
        return "\n".join(texts)
    return p.read_text(encoding="utf-8", errors="ignore")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", required=True, help="Dir of section .txt files, or a single text file")
    parser.add_argument("--condensed", required=True, help="Path to the merged condensed .md file")
    parser.add_argument("--report", required=True, help="Path to write the JSON report")
    parser.add_argument("--top-n", type=int, default=150, help="How many top original terms to check")
    parser.add_argument("--min-len", type=int, default=4, help="Minimum token length to consider")
    args = parser.parse_args()

    original_text = load_original(args.original)
    condensed_text = Path(args.condensed).read_text(encoding="utf-8", errors="ignore")

    original_terms = significant_terms(original_text, args.min_len)
    condensed_terms_set = set(significant_terms(condensed_text, args.min_len))

    freq = Counter(original_terms)
    top_terms = [t for t, _ in freq.most_common(args.top_n)]

    missing = [t for t in top_terms if t not in condensed_terms_set]
    present = [t for t in top_terms if t in condensed_terms_set]

    coverage_pct = round(100 * len(present) / len(top_terms), 1) if top_terms else 100.0

    report = {
        "original_word_count": len(original_text.split()),
        "condensed_word_count": len(condensed_text.split()),
        "compression_ratio_pct": round(
            100 * len(condensed_text.split()) / max(1, len(original_text.split())), 1
        ),
        "top_terms_checked": len(top_terms),
        "coverage_pct": coverage_pct,
        "missing_terms": [{"term": t, "original_frequency": freq[t]} for t in missing],
        "note": "This is a recall net based on raw word frequency, not semantics. "
        "Review 'missing_terms' yourself — some will be irrelevant (names, boilerplate), "
        "others may be real dropped concepts worth patching back in.",
    }

    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Coverage: {coverage_pct}% of top {len(top_terms)} original terms found in condensed text.")
    print(f"   Compression ratio: {report['compression_ratio_pct']}% of original word count.")
    if missing:
        print(f"   ⚠️  {len(missing)} terms flagged as possibly missing (see {args.report}):")
        for m in report["missing_terms"][:20]:
            print(f"      - {m['term']} (appeared {m['original_frequency']}x in original)")
        if len(missing) > 20:
            print(f"      ... and {len(missing) - 20} more in the report file")
    else:
        print("   No flagged terms — top original terms all appear in the condensed text.")


if __name__ == "__main__":
    main()
