# Esercizio 9 — File binario frammentato

**Obiettivo:** imparare a trasmettere file binari suddividendoli in pacchetti (“chunked transfer”), così da poter gestire dati di dimensione arbitraria.

---

### 📦 Formato di ciascun pacchetto inviato dal client

1. **2 byte** → lunghezza del chunk (numero di byte effettivi nel pacchetto).
2. **N byte** → i dati binari (con `N ≤ 512`).
3. **1 byte** → flag:

   * `0` → ci sono ancora pacchetti da ricevere.
   * `1` → questo è l’ultimo pacchetto del file.

---

### 🔹 Lato Client

* Legge un file binario da disco.
* Lo suddivide in blocchi da massimo 512 byte.
* Per ogni blocco costruisce un pacchetto:

  * `[lunghezza(2B)][chunk(NB)][flag(1B)]`.
* Invia i pacchetti in sequenza al server.
* Nell’ultimo pacchetto imposta il flag a `1`.

---

### 🔹 Lato Server

* Riceve i pacchetti uno alla volta.
* Per ciascun pacchetto:

  * legge la lunghezza (2 byte),
  * legge `N` byte di dati,
  * legge il flag (1 byte).
* Appende i dati ricevuti in un buffer o scrive direttamente su file.
* Quando riceve un pacchetto col flag = `1`, conclude la ricezione e salva il file ricostruito su disco.

---

### 👉 Esempio pratico

Supponiamo di inviare un file di **1100 byte**.

* Primo pacchetto: `[02 00][512 byte dati][00]` → 512 byte.
* Secondo pacchetto: `[02 00][512 byte dati][00]` → 512 byte.
* Terzo pacchetto: `[00 DC][220 byte dati][01]` → 220 byte + flag finale.

Il server ricompone i 512 + 512 + 220 = 1244 byte e salva il file ricostruito.

