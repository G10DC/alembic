# Condensing rubric

Paste this into each sub-agent, filled in. Do not paraphrase it down.

```
You are condensing ONE section of a university textbook into dense study notes.
Section {N} of {TOTAL}: "{title}". What preceded it: {one line}.

Your only input is the text below. Invent nothing. Ignore the rest of the book —
other agents have it.

=== SECTION TEXT ===
{chunk}
=== END SECTION TEXT ===

PRESERVE, with zero loss:
- Every technical term, named concept, definition, classification, formula, law,
  theorem, named model, and the person or study the book credits for it
  (attribution is examinable).
- Every causal or logical relationship asserted: X causes Y; X implies Y; X is a
  special case of Y; X and Y are confused because Z. State them explicitly and
  compactly even where the original takes a paragraph to get there.
- Numbers, dates, thresholds and named examples ONLY where they carry the point
  (a formula's variables, a law's year, a canonical experiment's result). Drop
  purely illustrative figures.
- Emphasis. Repetition, disproportionate space, emphatic wording ("fondamentale",
  "da ricordare", "in sintesi", "the key point is"), boxed or highlighted text:
  all evidence the topic is examinable. Mark with the ⭐ callout. Never normalise
  emphasised material to the weight of a passing mention.

CUT, aggressively:
- Scene-setting, colour anecdotes, rhetorical questions, the same claim restated
  three ways, filler transitions ("as we have seen", "in this section we will").
- Compress narrative examples to a one-line takeaway — unless the example IS the
  examinable object (a worked derivation, a canonical case study), in which case
  keep it, compressed but intact.

TONE
Terse information-dense prose or tight bullets. Not a narrative summary. Write
for someone who will quiz themselves on this, not read it for pleasure. Prefer
"X is defined as Y; causes Z" over "The author explains that X, an important
concept, is generally understood to...".

LENGTH
Roughly 15-30% of the original as a guide, NOT a ceiling or a floor. A
definitions-dense chapter compresses less; a padded introductory chapter
compresses more. Completeness always overrides the ratio.

FIGURES AND TABLES
You cannot reproduce them. Where the text references a figure or table carrying
information not restated in prose, add a one-line bracketed note of what it
showed, e.g. "[Tabella 4.1: confronto dei tre modelli su costo, latenza,
accuratezza — B migliore su accuratezza]".

Output must follow the structure in format.md exactly.
```

## Notes for the orchestrating agent

- Never show a sub-agent the whole book: it will drift into covering material
  that isn't its own.
- Chunk spanning a language switch (long quoted foreign sources): tell the agent
  to keep technical terms in the original language alongside a translation —
  that pairing is often exactly what is tested.
- If the user states the exam format, adjust: oral and open-answer exams reward
  explaining reasoning chains, so relationship material must survive at least as
  reliably as bare definitions.
