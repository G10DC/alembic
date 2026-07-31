# alembic
> Distils a book down to what the exam actually asks for.

`alembic` turns a full textbook into a dense Markdown study guide: it extracts
and sections the source (PDF, EPUB, DOCX, TXT, Markdown), hands each section to
its own sub-agent under a fixed condensing rubric, merges the results with a
table of contents and a deduplicated glossary, then checks keyword recall
against the original. The output is built to be fed back into an LLM for
Socratic questioning. One rule above all others: **completeness of concepts
outranks the compression ratio.**

## Install

| Environment | Path |
|---|---|
| Claude Code, project | `.claude/skills/alembic/` |
| Claude Code, personal | `~/.claude/skills/alembic/` |
| Antigravity, workspace | `.agents/skills/alembic/` (legacy: `.agent/skills/`) |
| Antigravity IDE, global | `~/.gemini/antigravity/skills/alembic/` |
| Antigravity CLI, global | `~/.gemini/antigravity-cli/skills/alembic/` |

```bash
unzip alembic.zip -d ~/.claude/skills/
pip install --break-system-packages pypdf python-docx ebooklib beautifulsoup4 lxml
```

## Usage

> Condense this textbook for my exam.

The skill extracts and sections the book, condenses each section through a
dedicated sub-agent, merges the result, and reports the compression ratio plus
anything the coverage check flagged as possibly dropped.

## License
MIT — see [LICENSE](LICENSE).
