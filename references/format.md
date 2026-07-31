# Required output shape per chunk

Every sub-agent returns Markdown in this shape, so chunks merge cleanly.

```markdown
## {Section number and title, as in the source, or your best reconstruction}

{Dense prose or tight bullets, per the rubric.}
```

Markers, used consistently:

- `**bold**` on a key term at first introduction, immediately followed by its
  definition — this is what the merge step harvests into the glossary, so the
  pattern must be `**term**: definition` or `**term** is/means ...`.
- `⭐` opening a line to flag anything the source emphasised, repeated or called
  important. Add one clause on *why* you flagged it.
- `>` blockquote only for a law, formula or definition the source states
  formally. Not for emphasis — that is what `⭐` is for.
- `[Tabella 2.3: ...]` bracketed note for uncapturable figures and tables.

Optional closing block, only where the section is substantial:

```markdown
### Punti chiave
- 3-8 bullets, ⭐-worthy points only, one level more compact than the body.
```

Not a recap of the section: only what decides a pass from a fail.

## Merge conventions

Section headings stay at `##` across all chunks, so the document title sits at
`#` and the generated table of contents nests correctly.
