
# Esercizio 8 — Protocollo con multipli record

**Obiettivo:** introdurre la gestione di messaggi che contengono più strutture (record), per imparare a fare parsing e aggregazione dei dati.

---

### 📦 Formato del messaggio inviato dal client

1. **1 byte** → numero di record presenti nel messaggio (`N`).
2. Per ciascun record (`N` volte):

   * **1 byte** → tipo del sensore (intero non firmato).

     * Esempio: `1 = temperatura`, `2 = umidità`, `3 = pressione`, ecc.
   * **4 byte** → valore del sensore, codificato come *float* a 32 bit in formato IEEE 754 (big-endian).

---

### 🔹 Lato Client

* Legge da input diversi valori di sensori (con il loro tipo).
* Costruisce il messaggio:

  * primo byte = numero totale di sensori inviati.
  * poi, per ogni sensore: `[tipo][valore]`.
* Invia il messaggio al server in un’unica `send()`.

---

### 🔹 Lato Server

* Riceve il messaggio.
* Legge il primo byte → numero di record (`N`).
* Itera su ciascun record e:

  * legge il tipo,
  * legge il valore float.
* Raggruppa i valori per tipo di sensore.
* Calcola la **media dei valori per ciascun tipo**.
* Risponde al client con un messaggio che contiene le medie, ad esempio in formato testuale:

  ```
  Tipo 1 → media = 21.3
  Tipo 2 → media = 48.7
  ...
  ```

---

### 👉 Esempio pratico

Il client vuole inviare 3 sensori:

* Tipo `1` (temperatura) = 20.5
* Tipo `2` (umidità) = 50.0
* Tipo `1` (temperatura) = 22.0

Il messaggio sarà:

```
[03]                  # numero di record = 3
[01][41 A4 00 00]     # tipo=1, valore=20.5
[02][42 48 00 00]     # tipo=2, valore=50.0
[01][41 B0 00 00]     # tipo=1, valore=22.0
```

Il server raggruppa:

* Tipo 1 → valori \[20.5, 22.0] → media = 21.25
* Tipo 2 → valori \[50.0] → media = 50.0

Risposta:

```
Tipo 1: 21.25
Tipo 2: 50.0
```

