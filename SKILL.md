---
name: alembic
description: Condensa un manuale o una dispensa (PDF, EPUB, DOCX, TXT, MD) in una guida di studio Markdown per l'esame, senza perdere concetti, con priorità d'esame, trappole, domande di verifica e glossario. Da usare per preparare un esame da un libro lungo; poi /artisan per l'HTML.
disable-model-invocation: true
---

# alembic

Un manuale è in gran parte impalcatura: la stessa idea detta tre volte, aneddoti,
transizioni. Comprimerlo alla cieca fa perdere l'esame insieme al riempitivo.
Regola sopra tutte: **la completezza dei concetti vale più del rapporto di
compressione.** L'uscita segue il formato condiviso (sotto) ed è l'ingresso di
`/artisan`.

## Regole d'oro

1. **Fedeltà prima della brevità.** Termine, definizione, formula, classificazione
   o legame causale che servirebbe a rispondere a un esame sopravvive, anche se la
   sezione non si accorcia. Il rapporto è una guida, non una quota.
2. **L'enfasi è un segnale.** Ripetizione, spazio sproporzionato, formule
   enfatiche, riquadri: l'autore indica cosa si chiede. Si traduce nella priorità
   `🔴 Sicuro` / `🟡 Frequente` / `🟢 Raro`; appiattirla distrugge lo strato più utile.
3. **Taglia la prolissità, mai la sostanza.** Aneddoti, domande retoriche,
   ripetizioni, transizioni vuote vanno; le affermazioni che avvolgono restano.
4. **Un sottoagente per sezione, solo il suo testo.** Dare tutto il libro a ognuno
   diluisce l'attenzione e sfuma i confini.
5. **I confini li decidi tu, non lo script.** La rilevazione è euristica: leggi il
   manifest, taglia ai confini naturali, mai dentro una definizione o un esempio svolto.
6. **Le relazioni sono materia d'esame.** "X causa Y", "X è caso particolare di Y",
   "X e Y si confondono perché Z": riscrivile in modo esplicito e compatto.
7. **Verifica la copertura e giudicala.** Lo script non ha semantica: propone, decidi tu.
8. **Correggi sul posto.** Un concetto recuperato va nella sua sezione, non in
   un'appendice di orfani.
9. **Niente invenzioni.** Trappole, frasi per l'orale e domande ci sono solo se il
   testo le giustifica; nessun contenuto oltre la fonte.

## Formato di uscita (condiviso con /artisan)

Dettaglio in `references/format.md`. In breve: un solo `# Titolo`; capitoli
`## N. Titolo`, sottosezioni `###`; definizione su riga a sé `**Termine**: definizione.`;
priorità con `🔴 Sicuro` / `🟡 Frequente` / `🟢 Raro` a inizio paragrafo;
trappola `❌ "sbagliato" → ✅ corretto`; frase per l'orale `🎯 "frase"`; sezione
`## Domande di verifica` con coppie `Domanda:` / `Risposta:`; `## Glossario` finale
generato dal merge.

## Pipeline

Su Windows usa `python`, non `python3`. I comandi usano la skill installata in `~/.claude/skills/alembic/`; `work/` è la cartella di lavoro dell'utente, cioè quella da cui si sta lavorando (la cartella corrente), non la cartella della skill.

### 1. Extract

```bash
pip install -r ~/.claude/skills/alembic/requirements.txt
python ~/.claude/skills/alembic/scripts/extract.py "<file>" --outdir work/extracted
```

Scrive una `.txt` per sezione in `work/extracted/sections/` e `manifest.json`
(`index`, `title`, `path`, `word_count`, `detection_method`). Rilevazione: segnalibri
PDF, stili di titolo DOCX, spine EPUB, intestazioni Markdown o `Capitolo N`.
Per PDF scansionati (solo immagini) lo script si ferma: serve `ocrmypdf`
(dipendenza opzionale, non in `requirements.txt`): `ocrmypdf --skip-text in.pdf out.pdf`.

### 2. Chunk

Leggi il manifest e decidi i confini veri:

- **2.000-6.000 parole** per blocco; una prefazione di 300 parole si unisce alla vicina.
- Capitolo troppo lungo: `python ~/.claude/skills/alembic/scripts/chunk.py work/extracted/sections/<file>.txt --outdir work/extracted --max-words 4000`
  spezza per paragrafi, sostituisce la voce nel manifest e rinumera; l'originale va in `sections/_split/` (non cancellato, ma fuori dalla copertura: `coverage.py` non lo legge, e un secondo lancio sullo stesso percorso dà errore).
- Nessuna struttura rilevata (una sola sezione enorme): usa `chunk.py` come sopra e
  dillo nel resoconto, così si spiegano i titoli mancanti.

### 3. Condensa

Per ogni blocco un sottoagente (se non ci sono, procedi tu in sequenza: saltare la
rubrica no). Passagli esattamente:

- il testo del suo blocco, nient'altro;
- la rubrica di `references/method.md`, incollata intera;
- `references/format.md`;
- la posizione nel libro (titolo, numero, una riga su cosa precede).

Ognuno scrive **`work/condensed/chunk_<N>.md`** (N = numero del blocco: il merge
accetta solo questi nomi).

### 4. Merge

```bash
python ~/.claude/skills/alembic/scripts/merge.py work/condensed --output work/guida.md --title "<titolo del manuale>"
```

Unisce i blocchi in ordine con indice, un'unica sezione `## Domande di verifica` e
`## Glossario` dalle righe `**Termine**: definizione.` Stesso termine definito in modo
diverso in due capitoli: restano entrambe, con `(cap. N)`: è sfumatura d'esame.
Il default del titolo è "Guida di studio": passa sempre `--title`.

### 5. Verifica

```bash
python ~/.claude/skills/alembic/scripts/coverage.py --original work/extracted/sections --condensed work/guida.md --report work/coverage.json
```

Elenca i termini frequenti della fonte assenti nella guida. Leggili: un nome
isolato è rumore, un termine tecnico ricorrente è un concetto perso da rimettere
nella sua sezione.

### 6. Consegna

Riporta: numero di blocchi, rapporto di compressione, cosa la copertura ha costretto
a correggere. Poi suggerisci il passo successivo: **`/artisan`** per la pagina HTML di
studio offline, oppure **`/stampa`** per la carta. Solo se richiesto: `.docx` o `.txt`.

## Sicurezza

- Non scrivere mai nel file sorgente o nella sua cartella: tutto va in un albero di
  lavoro a parte (`work/`).
- Non cancellare gli intermedi (`work/extracted`) finché l'utente non ha il file
  finale: servono a rifare un blocco senza rileggere il libro.
- Il materiale protetto da copyright resta in locale: niente blocchi su servizi
  esterni che non fanno già parte dell'ambiente dell'utente.

## Quando non usarla

- **Testi brevi** (articoli, un capitolo sotto ~3.000 parole): condensa direttamente.
- **Far entrare un testo in un budget di token**: qui conta ciò che serve ricordare, non la dimensione.
- **Estrazione letterale o traduzione**: la rubrica riscrive per costruzione.
- **Video o podcast**: lo script legge documenti. Per le lezioni video usa `yt-digest`
  e condensa la trascrizione solo se è abbastanza lunga da servire il chunking.
