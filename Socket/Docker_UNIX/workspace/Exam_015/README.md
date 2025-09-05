# Esercizio 6 — Stringhe + lunghezza binaria

**Obiettivo:** lavorare con campi di lunghezza variabile.

**Client:** legge una stringa da linea di comando. La invia come:

- uint16 (2 byte, big endian) che indica la lunghezza.
- N byte con la stringa in UTF-8.

**Server:** riceve, converte in maiuscolo e risponde nello stesso formato.

**Nota:** come quello che mi hai chiesto prima, ma esplicitamente con controllo di UTF-8 (se byte non validi → errore).