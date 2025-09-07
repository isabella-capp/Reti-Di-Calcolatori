# 🔹 Esercizio B — Conteggio parole da file

**Obiettivo:** esercitarsi nella gestione di **file di testo**, nell’uso di **dizionari** per il conteggio delle frequenze, e nello scambio di dati strutturati in **JSON** tra client e server.

---

## 📦 Specifiche del protocollo

### Messaggio del client → server

Il client invia al server una stringa contenente il **nome di un file** (es. `"testo.txt"`).
Il file si trova **sul filesystem del server** (non viene trasferito dal client).

---

### Comportamento del server

1. Si mette in ascolto su una porta TCP (es. `3000`).
2. Riceve dal client il nome del file.
3. Apre il file in sola lettura. Se il file non esiste → risponde con un JSON:

   ```json
   { "error": "file not found" }
   ```
4. Se il file esiste:

   * Legge il contenuto.
   * Divide il testo in parole (puoi usare come separatori: spazi, punteggiatura, newline).
   * Conta quante volte appare ogni parola, usando un dizionario (`word → count`).
   * Crea una risposta in formato JSON del tipo:

     ```json
     {
       "wordcount": {
         "ciao": 3,
         "mondo": 1,
         "python": 2
       }
     }
     ```
5. Invia la risposta al client.

---

### Comportamento del client

1. Prende il nome del file da **parametro linea di comando**.

   ```bash
   python3 client.py testo.txt
   ```
2. Invia il nome del file al server.
3. Riceve la risposta JSON.
4. Se c’è `"error"` → stampa il messaggio di errore.
5. Se c’è `"wordcount"` → elabora il dizionario e stampa le **5 parole più frequenti**, ordinate per frequenza decrescente.

   * A parità di frequenza, si può ordinare in ordine alfabetico.

---

## 👉 Esempio di interazione

Supponiamo che il file `testo.txt` sul server contenga:

```
ciao mondo
ciao python
ciao python ciao
```

### Client invia:

```
"testo.txt"
```

### Server risponde:

```json
{
  "wordcount": {
    "ciao": 4,
    "mondo": 1,
    "python": 2
  }
}
```

### Output del client:

```
Le 5 parole più frequenti:
1. ciao → 4
2. python → 2
3. mondo → 1
```

