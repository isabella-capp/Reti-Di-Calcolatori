# Esercizio 5 — Interi con segno

**Obiettivo:** introdurre la differenza tra signed e unsigned.

**Client:** invia un numero intero con segno a 16 bit (int16_t, big endian).

**Server:** riceve il numero e stampa sia il valore interpretato come int16 che come uint16. Poi rispedisce il numero incrementato di 1.

**Difficoltà aggiuntiva:** il client deve gestire anche numeri negativi e mostrare la rappresentazione binaria prima di inviarla.