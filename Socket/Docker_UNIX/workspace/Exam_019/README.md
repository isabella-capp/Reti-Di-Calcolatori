## 🔹 Esercizio A — Dizionario JSON remoto

**Obiettivo:** lavorare con i dizionari Python e la serializzazione JSON.

* Il **client** prende da linea di comando due parametri: una **chiave** e un **valore**.
* Invia al server una struttura JSON del tipo:

  ```json
  {"action": "insert", "key": "nome", "value": "Mario"}
  ```
* Il **server** mantiene un dizionario in memoria condiviso tra i client.

  * Se `action=insert` inserisce la coppia chiave/valore.
  * Se `action=get`, restituisce il valore associato alla chiave.
* Le risposte devono essere in JSON, ad esempio:

  ```json
  {"status": "ok", "key": "nome", "value": "Mario"}
  ```

  oppure

  ```json
  {"status": "error", "message": "key not found"}
  ```

