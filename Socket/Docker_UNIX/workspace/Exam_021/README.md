
# 🔹 Esercizio C — Manipolazione di stringhe

### 🎯 Obiettivo

L’esercizio ha lo scopo di esercitarsi con **operazioni di parsing e trasformazione di stringhe** utilizzando comunicazione client-server.

---

### 📌 Funzionamento

* **Client**

  * legge da linea di comando una stringa arbitraria (anche contenente spazi).
  * invia la stringa al server tramite socket TCP.

* **Server**

  * riceve la stringa inviata dal client.
  * applica una serie di trasformazioni alla stringa.
  * restituisce al client un **oggetto JSON** con i seguenti campi:

    * `"uppercase"` → la stringa convertita tutta in **maiuscolo**
    * `"lowercase"` → la stringa convertita tutta in **minuscolo**
    * `"reverse"` → la stringa **invertita** (caratteri in ordine inverso)
    * `"length"` → un intero che rappresenta la **lunghezza della stringa**

---

### 📊 Esempio di input/output

**Input del client:**

```
ciao
```

**Risposta del server (JSON):**

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
