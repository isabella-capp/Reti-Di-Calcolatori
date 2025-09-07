
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

