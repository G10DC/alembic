# alembic
> Distilla un manuale fino a ciò che l'esame chiede davvero.

`alembic` trasforma un manuale o una dispensa (PDF, EPUB, DOCX, TXT, Markdown) in
una guida di studio Markdown densa: estrae e divide la fonte, affida ogni sezione a
un sottoagente con una rubrica fissa, unisce i risultati con indice, domande di
verifica e glossario, poi controlla la copertura dei termini rispetto
all'originale. Regola sopra tutte: **la completezza dei concetti vale più del
rapporto di compressione.**

È la prima metà di una catena: `/alembic` (libro -> guida Markdown) poi `/artisan`
(Markdown -> pagina HTML di studio offline) o `/stampa` per la carta. Il formato
che le collega è in [references/format.md](references/format.md). Si invoca solo
a mano.

## Installazione

```bash
git clone https://github.com/G10DC/alembic ~/.claude/skills/alembic
cd ~/.claude/skills/alembic
pip install -r requirements.txt
```

Altri percorsi possibili: `.claude/skills/alembic/` (progetto), `.agents/skills/alembic/`
(Antigravity). Su Windows usa `python`, non `python3`. Per i PDF scansionati serve
anche `ocrmypdf` (opzionale).

## Uso

> /alembic ~/Documenti/manuale.pdf

Estrae e divide il libro, condensa ogni sezione, unisce, verifica la copertura e
riporta il rapporto di compressione con ciò che il controllo ha fatto correggere.

## Test

```bash
python -m unittest discover -s tests -v
```

## Licenza
MIT, vedi [LICENSE](LICENSE).
