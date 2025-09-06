## 🔹 Esercizio B — Conteggio parole da file

**Obiettivo:** lavorare con file di testo e strutture dati.

* Il **client** invia il nome di un file (stringa).
* Il **server** apre il file (locale al server), conta quante volte appare ogni parola, e risponde con un JSON del tipo:

  ```json
  {
    "wordcount": {
      "ciao": 3,
      "mondo": 1,
      "python": 2
    }
  }
  ```
* Il **client** stampa le 5 parole più frequenti.

---

## 🔹 Esercizio C — Manipolazione stringhe

**Obiettivo:** parsing e trasformazioni di stringa.

* Il **client** invia una stringa arbitraria.
* Il **server** risponde con un dizionario JSON che contiene:

  * `"uppercase"` → stringa tutta maiuscola
  * `"lowercase"` → stringa tutta minuscola
  * `"reverse"` → stringa invertita
  * `"length"` → lunghezza della stringa

Esempio:

```json
{
  "uppercase": "CIAO",
  "lowercase": "ciao",
  "reverse": "oaic",
  "length": 4
}
```

---

## 🔹 Esercizio D — Database studenti

**Obiettivo:** JSON + dizionari + gestione file.

* Il **server** mantiene un database studenti in un file JSON, es.:

  ```json
  [
    {"matricola": "123", "nome": "Luca", "voto": 28},
    {"matricola": "456", "nome": "Anna", "voto": 30}
  ]
  ```
* Il **client** può inviare richieste:

  * `{"action": "list"}`
  * `{"action": "get", "matricola": "123"}`
  * `{"action": "insert", "matricola": "789", "nome": "Marco", "voto": 25}`
* Il **server** risponde in JSON con i dati o con errori.
* Tutti gli inserimenti vengono salvati sul file per la persistenza.

---

## 🔹 Esercizio E — Calcolatrice distribuita

**Obiettivo:** gestione di numeri e operazioni.

* Il **client** invia un JSON con due numeri e un’operazione, ad esempio:

  ```json
  {"op": "mul", "a": 5, "b": 3}
  ```
* Il **server** esegue l’operazione (`add`, `sub`, `mul`, `div`) e risponde:

  ```json
  {"result": 15}
  ```
* Se l’operazione non è valida → `{"error": "invalid operation"}`
