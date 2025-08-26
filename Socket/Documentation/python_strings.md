
# 📌 Documentazione sulle **Stringhe in Python**

## 1. Introduzione

Una **stringa** è una sequenza di caratteri. In Python, le stringhe sono **immutabili** (non si possono modificare direttamente, ma solo creare nuove stringhe).

La creazione può avvenire in tre modi:

1. **Virgolette singole**

    ```python
    s1 = "ciao"
    ```
1. **Doppie virgolette**

    ```python
    s2 = 'mondo'
    ```
1. **Triple virgolette** (per stringhe multilinea)

    ```python
    s3 = """Lorem ipsum dolor sit amet,
        consectetur adipiscing elit,
        sed do eiusmod tempor incididunt
        ut labore et dolore magna aliqua."""
    ```

## 2. Rappresentazione e indexing

Le stringhe sono sequenze, quindi supportano **indicizzazione** e **slicing**:

```python
s = "Python"
print(s[0])     # 'P' (indice positivo)
print(s[-1])    # 'n' (indice negativo)
print(s[0:4])   # 'Pyth' (slice da indice 0 a 3)
print(s[:3])    # 'Pyt' (dall’inizio a indice 2)
print(s[3:])    # 'hon' (da indice 3 alla fine)
print(s[:-1])   # 'Pytho' (tutto tranne l’ultimo carattere)
```

## 3. Concatenazione e ripetizione

```python
a = "Ciao"
b = "Mondo"
print(a + " " + b)   # concatenazione → "Ciao Mondo"
print(a * 3)         # ripetizione → "CiaoCiaoCiao"
```

## 4. Iterazione

Le stringhe sono iterabili:

```python
for ch in "ciao":
    print(ch)
```


## 5. Funzioni integrate utili (`len`, `str`, `ord`, `chr`)

```python
s = "Python"
print(len(s))      # 6
print(str(123))    # "123"
print(ord('A'))    # 65 (codice Unicode di 'A')
print(chr(65))     # "A"
```


## 6. Metodi principali delle stringhe

### 🔹 Conversione maiuscole/minuscole

```python
s = "Python"
print(s.upper())     # "PYTHON"
print(s.lower())     # "python"
print(s.capitalize()) # "Python"
print(s.title())     # "Python" (ogni parola con iniziale maiuscola)
print(s.swapcase())  # "pYTHON"
```


### 🔹 Ricerca e sostituzione

```python
s = "ciao mondo"
print(s.find("mondo"))     # 5 (indice di inizio)
print(s.rfind("o"))        # 9 (ultima occorrenza)
print(s.index("ciao"))     # 0 (come find, ma errore se non trovato)
print(s.count("o"))        # 2
print(s.replace("mondo", "Python")) # "ciao Python"
```


### 🔹 Controllo contenuto

```python
s = "python123"
print(s.isalpha())   # False (contiene numeri)
print(s.isdigit())   # False
print(s.isalnum())   # True (lettere + numeri)
print(s.islower())   # True
print(s.isupper())   # False
print("   ".isspace()) # True (solo spazi)
```

### 🔹 Gestione spazi

```python
s = "   ciao   "
print(s.strip())   # "ciao" (toglie spazi iniziali/finali)
print(s.lstrip())  # "ciao   " (toglie solo a sinistra)
print(s.rstrip())  # "   ciao" (toglie solo a destra)
```

### 🔹 Suddivisione e unione

```python
s = "uno,due,tre"
lista = s.split(",")       # ["uno", "due", "tre"]
print(" - ".join(lista))   # "uno - due - tre"

righe = "riga1\nriga2\nriga3"
print(righe.splitlines())  # ["riga1", "riga2", "riga3"]
```


### 🔹 Controllo prefissi e suffissi

```python
s = "programmazione.py"
print(s.startswith("pro"))  # True
print(s.endswith(".py"))    # True
```

## 7. Formattazione delle stringhe

### 🔹 `format()`

```python
nome = "Alice"
eta = 25
print("Ciao, mi chiamo {} e ho {} anni".format(nome, eta))
```

### 🔹 f-string (consigliata, da Python 3.6+)

```python
nome = "Alice"
eta = 25
print(f"Ciao, mi chiamo {nome} e ho {eta} anni")
```

### 🔹 Specificatori di formato

```python
pi = 3.14159
print(f"Valore di pi: {pi:.2f}")   # "Valore di pi: 3.14"
```


## 8. Raw string (utile per regex e path Windows)

```python
s = r"C:\Users\Alice\Documenti"
print(s)  # "C:\Users\Alice\Documenti" (non interpreta \ come escape)
```

## 9. Escape characters

* `\n` → nuova riga
* `\t` → tabulazione
* `\\` → backslash
* `\"` → virgolette doppie
* `\'` → virgolette singole

```python
s = "Ciao\nMondo"
print(s)
```

## 10. Slicing avanzato

```python
s = "abcdef"
print(s[::2])   # "ace" (step di 2)
print(s[::-1])  # "fedcba" (stringa invertita)
```

## 11. Operatori in e not in
Possiamo usare gli operatori in e not in per verificare se un elemento o un carattere sia presente in una lista o stringa:

```python
>>> my_list = ["spam", "spam", "spam"]
>>> new_str = "happiness"

>>> "bacon" in my_list
False
>>> "spam" in my_list
True
>>> "eggs" not in my_list
True

>>> "k" not in new_str
True
>>> "h" in new_str
True
```

## 12. Tabelle riassuntive

### 🔹 Metodi comuni

| Metodo                 | Descrizione                        |
| ---------------------- | ---------------------------------- |
| `.upper()`             | Tutto maiuscolo                    |
| `.lower()`             | Tutto minuscolo                    |
| `.capitalize()`        | Prima lettera maiuscola            |
| `.title()`             | Ogni parola con iniziale maiuscola |
| `.swapcase()`          | Inverte maiuscole/minuscole        |
| `.find()` / `.index()` | Ricerca sottostringa               |
| `.replace()`           | Sostituisce sottostringa           |
| `.strip()`             | Rimuove spazi                      |
| `.split()`             | Divide in lista                    |
| `.join()`              | Unisce lista in stringa            |
| `.startswith()`        | Controlla prefisso                 |
| `.endswith()`          | Controlla suffisso                 |
| `.count()`             | Conta occorrenze                   |

---