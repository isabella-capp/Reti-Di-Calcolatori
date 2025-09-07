
# 🔹 Esercizio D — Verifica di palindromi

**Obiettivo:** esercitarsi con la logica condizionale e la manipolazione di stringhe lato server.

* Il **client** invia al server una **parola** o una **frase arbitraria** sotto forma di stringa.

* Il **server**:

  1. Riceve la stringa.
  2. Normalizza il contenuto eliminando spazi e rendendo tutto minuscolo.
  3. Verifica se la stringa è un **palindromo** (cioè se la sequenza dei caratteri è la stessa sia letta da sinistra verso destra che da destra verso sinistra).
  4. Risponde al client con un oggetto JSON del tipo:

```json
{"palindrome": true}
```

oppure

```json
{"palindrome": false}
```

**Esempi:**

* Input: `"Anna"` → Output: `{"palindrome": true}`
* Input: `"i topi non avevano nipoti"` → Output: `{"palindrome": true}`
* Input: `"ciao"` → Output: `{"palindrome": false}`

