# Esercizio 7 — Pacchetti con checksum

**Obiettivo:** introdurre un meccanismo di controllo di integrità dei dati durante la comunicazione.

### 📦 Formato del messaggio inviato dal client:

1. **2 byte** → lunghezza del payload (numero di byte della stringa, codificata in UTF-8).
2. **N byte** → il payload vero e proprio (la stringa).
3. **2 byte** → checksum, calcolato come segue:

$$
\text{checksum} = \Big(\sum_{i=1}^{N} \text{payload}[i]\Big) \bmod 65536
$$

Cioè: si sommano i valori interi (byte) di tutti i caratteri del payload, e si prende il risultato **modulo 65536** (per tenerlo in 2 byte).


### 🔹 Lato Client

* Legge una stringa da tastiera.
* Calcola la lunghezza (`N`) e la inserisce nei primi 2 byte.
* Converte la stringa in byte (UTF-8).
* Calcola il **checksum** sommando tutti i byte del payload, modulo 65536.
* Costruisce il messaggio: `[lunghezza][payload][checksum]`.
* Invia il messaggio al server.


### 🔹 Lato Server

* Riceve i 2 byte di lunghezza.
* Riceve `N` byte di payload.
* Riceve i 2 byte di checksum.
* **Ricalcola** il checksum sul payload ricevuto.
* Se il valore coincide con quello inviato dal client → risponde con `"ACK"`.
* Altrimenti risponde con `"NACK"`.


👉 In pratica:

* Se il payload è `"ABC"` → i byte sono `65 66 67`.
* La somma è `65+66+67 = 198`.
* Checksum = `198 mod 65536 = 198`.
* Il client invia: `[00 03][41 42 43][00 C6]`

(`00 03` = lunghezza 3, `41 42 43` = "ABC", `00 C6` = 198 in esadecimale).