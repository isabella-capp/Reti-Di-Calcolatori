# Esercizio 3 — Operazioni matematiche

Scrivere un server che riceve un messaggio contenente:

- 1 byte che rappresenta l’operazione (1 = somma, 2 = sottrazione, 3 = moltiplicazione, 4 = divisione).

- 2 campi consecutivi a 4 byte ciascuno (float 32 bit, IEEE 754).

Il server deve eseguire l’operazione richiesta e restituire un messaggio con:

- 1 byte che ripete il codice dell’operazione.

- 4 byte contenenti il risultato (float 32 bit).