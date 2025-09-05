# Esercizio 1 — Conversione interi

Si vuole realizzare un **server TCP** che riceve da un client un numero intero **senza segno** e restituisce lo stesso numero **moltiplicato per 10**.

Il messaggio inviato dal client ha il seguente formato:

* **1 byte** che indica la lunghezza dell’intero:

  * `1` → intero a 8 bit (`uint8_t`)
  * `2` → intero a 16 bit (`uint16_t`)
  * `4` → intero a 32 bit (`uint32_t`)
* **N byte** (1, 2 o 4) che rappresentano il numero in **formato big endian** (network byte order).

Il server deve rispondere con un messaggio nello stesso formato, in cui il valore numerico è stato moltiplicato per 10.

## 📌 Funzionamento del server

1. Il server si mette in ascolto su una porta specificata a riga di comando (es. `3000`).
2. Quando riceve una connessione, legge il messaggio inviato dal client.
3. Decodifica la lunghezza e il numero ricevuto.
4. Calcola il valore moltiplicato per 10.
5. Invia al client la risposta nello stesso formato.
6. Stampa su standard output una riga del tipo:

```bash
Serving client request: <valore_input> <valore_output>
```

dove `<valore_input>` è il numero ricevuto e `<valore_output>` è il risultato.

7. Il server deve essere in grado di servire più richieste consecutive, senza essere riavviato ogni volta.
   Non è richiesto l’uso di `fork()` o thread.

---

## 📌 Esempi di esecuzione

### Avvio del server

Il server accetta la porta come parametro:

```bash
./server 3000
```

Il programma resta in ascolto sulla porta `3000`.

---

### Invio da parte del client (esempi)

#### Caso 1: invio di un intero `25` su 1 byte (`uint8`)

* Messaggio inviato dal client:

  ```
  0x01 0x19
  ```

  * `0x01` → indica `uint8`
  * `0x19` → 25 in esadecimale

* Risposta del server:

  ```
  0x01 0xFA
  ```

  * `0x01` → stesso tipo (`uint8`)
  * `0xFA` → 250 in esadecimale

* Output stampato dal server:

  ```
  Serving client request: 25 250
  ```

---

#### Caso 2: invio di un intero `1000` su 2 byte (`uint16`)

* Messaggio inviato:

  ```
  0x02 0x03 0xE8
  ```

  * `0x02` → indica `uint16`
  * `0x03E8` → 1000 in big endian

* Risposta:

  ```
  0x02 0x27 0x10
  ```

  * `0x02` → stesso tipo
  * `0x2710` → 10000 in big endian

* Output server:

  ```
  Serving client request: 1000 10000
  ```

---

#### Caso 3: invio di un intero `123456789` su 4 byte (`uint32`)

* Messaggio inviato:

  ```
  0x04 0x07 0x5B 0xCD 0x15
  ```

  * `0x04` → indica `uint32`
  * `0x075BCD15` → 123456789 in big endian

* Risposta:

  ```
  0x04 0x49 0x96 0x02 0xDA
  ```

  * `0x04` → stesso tipo
  * `0x499602DA` → 1234567890 in big endian

* Output server:

  ```
  Serving client request: 123456789 1234567890
  ```

---

Vuoi che ti scriva anche il **sorgente del server in C** pronto da compilare, oppure ti basta il testo così formulato come se fosse un enunciato d’esame?
