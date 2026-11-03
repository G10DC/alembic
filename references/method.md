# Rubrica di condensazione

Incollala in ogni sottoagente, compilata, insieme a `references/format.md`
(la rubrica ne richiede la struttura). Non riassumerla.

```
Stai condensando UNA sezione di un manuale universitario in appunti di studio
densi, in italiano (i termini tecnici restano nella lingua della fonte, con la
traduzione accanto). Sezione {N} di {TOTALE}: "{titolo}". Cosa la precede:
{una riga}.

Il tuo unico input è il testo qui sotto. Non inventare nulla oltre la fonte.
Ignora il resto del libro: lo hanno altri agenti.

=== TESTO DELLA SEZIONE ===
{chunk}
=== FINE TESTO ===

CONSERVA, senza perdite:
- Ogni termine tecnico, concetto con nome, definizione, classificazione,
  formula, legge, teorema, modello, e la persona o lo studio a cui il testo li
  attribuisce (l'attribuzione si chiede all'esame).
- Ogni relazione causale o logica affermata: X causa Y; X implica Y; X è un caso
  particolare di Y; X e Y si confondono perché Z. Scrivila in modo esplicito e
  compatto anche se la fonte ci arriva in un paragrafo.
- Numeri, date e soglie SOLO dove reggono il discorso (una legge e il suo anno,
  le variabili di una formula). Via le cifre solo illustrative.
- L'enfasi. Ripetizione, spazio sproporzionato, formule enfatiche
  ("fondamentale", "da ricordare", "in sintesi"), riquadri ed evidenziati sono
  indizi che l'argomento è d'esame: marcalo con la priorità (🔴 Sicuro,
  🟡 Frequente, 🟢 Raro) secondo format.md, mai appiattito a menzione di passaggio.

TAGLIA senza pietà:
- Scena di apertura, aneddoti di colore, domande retoriche, la stessa idea detta
  tre volte, transizioni vuote ("come abbiamo visto", "in questa sezione").
- Gli esempi narrativi diventano una riga di sintesi, a meno che l'esempio SIA
  l'oggetto d'esame (una dimostrazione, un caso canonico): allora resta,
  compresso ma intero.

AGGIUNGI, solo se il testo lo giustifica:
- Trappole (❌ "…" → ✅ …) dove la fonte segnala un errore comune o una
  confusione tra concetti.
- Frasi per l'orale (🎯 "…") dove la fonte ha una formulazione che regge da sola.
- In fondo, "## Domande di verifica": 5-10 coppie "Domanda:" / "Risposta:"
  (3-5 se la sezione è solo parte di un capitolo), con risposte ricavabili dal
  testo qui sopra.

TONO
Prosa asciutta e densa o elenchi stretti. Non un riassunto narrativo: appunti per
chi si interrogherà da solo. "X è definito come Y; causa Z", non "l'autore spiega
che X, un concetto importante, è generalmente inteso come...".

LUNGHEZZA
Circa 15-30% dell'originale come guida, NON come tetto né come minimo. Un
capitolo pieno di definizioni si comprime meno; uno introduttivo e gonfio di più.
La completezza vince sempre sul rapporto.

FIGURE E TABELLE
Non puoi riprodurle. Dove il testo rimanda a una figura o tabella con
informazioni non ripetute in prosa, una nota breve tra parentesi quadre, per
esempio "[Tabella 4.1: confronto dei tre modelli per costo e accuratezza]".

Scrivi nel file chunk_{N}.md. L'uscita segue format.md alla lettera: un solo
livello "##" per il capitolo ("## {N}. Titolo"), mai "#".
```

## Note per l'agente che orchestra

- Non mostrare mai a un sottoagente tutto il libro: finirebbe per coprire
  materiale non suo.
- Se la sezione contiene lunghe citazioni in un'altra lingua, di' all'agente di
  tenere i termini tecnici nella lingua originale accanto alla traduzione: spesso
  è proprio quell'abbinamento a essere richiesto.
- Se l'utente dichiara il formato d'esame, adatta: negli orali e nelle domande
  aperte contano i ragionamenti, quindi relazioni, trappole e frasi per l'orale
  devono sopravvivere almeno quanto le definizioni.
