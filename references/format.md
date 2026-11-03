# Formato condiviso (alembic -> artisan)

Contratto tra l'uscita di alembic e l'ingresso di `/artisan` (che trasforma il
Markdown in una pagina HTML di studio). Ogni sottoagente lo rispetta alla
lettera; `scripts/merge.py` assembla i blocchi su queste convenzioni.

## Forma del file di un blocco (`chunk_<N>.md`)

```markdown
## {N}. {Titolo del capitolo o della sezione, come nella fonte}

Testo denso o elenchi stretti, secondo la rubrica.

**Termine**: definizione.

🔴 Sicuro: punto che quasi certamente esce all'esame, con una clausola sul perché.

### Sottosezione

...

### Punti chiave
- 3-8 punti, solo i decisivi per superare o no l'esame.

## Domande di verifica

Domanda: testo
Risposta: testo
```

Nel file finale c'è un solo `# Titolo` (lo scrive il merge: i blocchi non usano
mai `#`). Capitoli `## N. Titolo`, sottosezioni `###`.

## Marcatori

- **Definizione**: riga a sé `**Termine**: definizione.` Il grassetto serve solo
  per i termini definiti, mai per enfasi: il merge ne ricava il `## Glossario`.
- **Priorità d'esame**: paragrafo o voce che inizia con `🔴 Sicuro`,
  `🟡 Frequente` o `🟢 Raro`. Il sicuro è ciò che la fonte enfatizza, ripete o a
  cui dedica molto spazio; il raro è un dettaglio vero ma marginale. Non marcare
  tutto: se tutto è rosso, nulla lo è.
- **Trappola**: riga `❌ "formulazione sbagliata" → ✅ formulazione corretta`.
  Solo se la fonte segnala un errore comune o una confusione tra concetti.
- **Frase per l'orale**: riga `🎯 "frase"`. Solo se la fonte contiene una
  formulazione che regge da sola come risposta d'esame (definizione canonica,
  classificazione, catena causale).
- **Domande di verifica**: sezione `## Domande di verifica` in fondo al blocco,
  coppie di righe consecutive `Domanda: testo` e `Risposta: testo` (testo
  semplice, senza grassetto sulle etichette), 5-10 coppie per capitolo (3-5 se il
  blocco è solo una parte di capitolo). Ogni risposta deve essere ricavabile dal
  testo del blocco.
- `>` solo per una legge, formula o definizione che la fonte enuncia in modo
  formale.
- `[Tabella 2.3: ...]` nota tra parentesi per figure e tabelle non riproducibili.

Trappole, frasi per l'orale e domande vengono dalla fonte: se il testo non le
giustifica non si scrivono, e non si inventa nulla oltre ciò che la fonte dice.

## Cosa aggiunge il merge

`# Titolo` (da `--title`), `## Indice`, i capitoli in ordine, un'unica
`## Domande di verifica` (le domande dei blocchi, raggruppate per capitolo con
`###`) e `## Glossario` con le definizioni, in ordine alfabetico. Un termine
definito in modo diverso in due capitoli compare due volte, con `(cap. N)`.
