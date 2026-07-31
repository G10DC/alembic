---
name: alembic
description: Distills an entire book or textbook (PDF, EPUB, DOCX, TXT, Markdown) into a dense Markdown study guide that keeps every concept, key term, definition and the author's own emphasis while cutting verbosity. Splits the source into sections, condenses each with a dedicated sub-agent, then verifies keyword coverage against the original. Use for textbooks, dispense, manuali, lecture notes, exam prep, and any request to condense, riassumere or sintetizzare a book into study notes or LLM-ready context for Socratic questioning. Never write a narrative summary; never drop a term the source repeats or emphasizes.
---

# alembic

A textbook is mostly scaffolding: the same claim said three ways, anecdotes for
colour, transitions that carry no information. Compress it naively and you lose
the exam with the padding. One rule above all others:
**completeness of concepts outranks the compression ratio — always.**

## Golden rules

1. **Fidelity beats brevity.** If a term, definition, formula, classification or
   causal link would be needed to answer an exam question, it survives — even if
   that section barely shrinks. A ratio target is a guide, never a quota.
2. **Emphasis is signal, not style.** Repetition, disproportionate page count,
   emphatic wording, boxed text: the author is telling you what gets tested.
   Mark it with `⭐`. Flattening emphasis destroys the most valuable layer in
   the book.
3. **Cut verbosity, never substance.** Anecdotes used as colour, rhetorical
   questions, restatements, throat-clearing transitions go. The claims they
   wrap around stay.
4. **One sub-agent per section, and only its own text.** Feeding the whole book
   to each agent dilutes attention and bleeds section boundaries. Isolation is
   what keeps quality flat across 600 pages instead of decaying after chapter 3.
5. **You decide the chunking, not the script.** Detection is heuristic. Read the
   manifest, then cut at natural boundaries — never mid-definition, mid-proof or
   mid-worked-example.
6. **Relationships are exam material.** `X causes Y`, `X is a special case of Y`,
   `X and Y are confused because Z`. Restate them explicitly and compactly, even
   when the source takes a paragraph to arrive there.
7. **Verify recall, then judge it.** Run the coverage check and read the flagged
   terms yourself. The script has no semantics: it proposes, you decide what was
   filler and what was a dropped concept.
8. **Patch in place, never bolt on.** A concept recovered at QA goes back into
   its own section, where its context is. An appendix of orphaned terms is
   useless for studying.

## Pipeline

### 1. Extract

```bash
pip install pypdf python-docx ebooklib beautifulsoup4 lxml
python3 scripts/extract.py "<input_file>" --outdir work/extracted
```

Writes one `.txt` per detected section into `work/extracted/sections/`, plus
`manifest.json` with `{index, title, path, word_count, detection_method}`.
Detection uses PDF bookmarks, DOCX heading styles, EPUB spine, Markdown headers
or `Capitolo|Chapter N` patterns, in that order of reliability.

### 2. Chunk

Read the manifest, then decide the real boundaries:

- **2,000–6,000 words** per chunk: small enough to hold the whole argument in
  mind, large enough not to fragment a concept across two agents.
- Merge fragments (a 300-word preface joins its neighbour).
- Split oversized chapters at a sub-heading, never inside a definition,
  derivation or worked example.
- No structure detected at all? Chunk on paragraph-aligned word windows and say
  so in the delivery note, so the missing chapter titles are explained.

### 3. Condense

For each chunk, spawn a sub-agent (any parallel sub-task mechanism; if the
environment has none, process sequentially yourself — sequential is acceptable,
skipping the rubric is not). Give it exactly three things:

- its own chunk text, nothing else;
- the rubric from `references/method.md`, pasted verbatim;
- its position in the book (title, number, one line on what preceded it).

Each returns one Markdown file shaped by `references/format.md`.

### 4. Merge

Concatenate in order, then build on top — these need the whole-book view a
sub-agent never had:

- a table of contents linking each section heading;
- one deduplicated glossary from every `**term**` + definition. Same term
  defined differently in two chapters: keep both, labelled by chapter. That
  divergence is exam-relevant nuance, not a merge conflict.

### 5. Verify

```bash
python3 scripts/coverage.py --original work/extracted/sections \
  --condensed <merged.md> --report work/coverage.json
```

Lists high-frequency source terms absent from the output. Read them: a one-off
character name is noise, a recurring technical term is a dropped concept — patch
it back into its own section.

### 6. Deliver

Markdown by default: the output is destined for an LLM context window, not a
printer. Produce `.docx` or `.txt` only on request. Report to the user: number
of chunks, compression ratio, what the coverage check forced you to patch.
Nothing else — they can read the file.

## Safety

- Never write into the source file or its directory; all work goes to a separate
  output tree.
- Never delete extracted intermediates before the user has the final file: they
  are the only way to re-run a bad chunk without re-parsing the book.
- Copyrighted material stays local — never upload chunks to third-party services
  not already part of the user's environment.

## When to use

Condensing a book, textbook, `dispensa`, manual or long lecture notes into study
material; preparing exam notes; producing LLM-ready context for self-quizzing.

## When NOT to use

- **Short documents** (papers, articles, single chapters under ~3,000 words):
  the orchestration costs more than it returns — condense directly.
- **Fitting text into a token budget**, where the goal is size rather than
  study: use `sieve` instead. The distinction is the purpose of the resulting
  text, not its length — `alembic` optimises for what a reader must be able to
  recall, `sieve` for what a context window can hold.
- **Verbatim extraction or translation**: nothing here preserves original
  wording — the rubric rewrites by design.
- **Parsing raw scans or image-only documents**: If the source text is an image or a scanned PDF, do not write custom OCR extraction logic. Instead, reference the guidelines and validation loops of `scribe` to handle preprocessing, schema validation, and field-level repairs before chunking.
- **Parsing raw scans or image-only documents**: If the source text is an image or a scanned PDF, do not write custom OCR extraction logic. Instead, reference the guidelines and validation loops of `scribe` to handle preprocessing, schema validation, and field-level repairs before chunking.
