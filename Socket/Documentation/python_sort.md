
# 📘 Documentazione `sorted()`

## Descrizione

La funzione built-in **`sorted()`** di Python restituisce una **nuova lista ordinata** contenente tutti gli elementi di un iterabile.
Non modifica l’oggetto originale (a differenza di `list.sort()` che agisce in-place).

---

## 📌 Sintassi

```python
sorted(iterable, *, key=None, reverse=False)
```

### Parametri

* **`iterable`** (obbligatorio):
  Qualsiasi oggetto iterabile (lista, tupla, stringa, dizionario, set, generatore, ecc.).

* **`key`** (opzionale):
  Una funzione che accetta un singolo argomento e restituisce il valore usato per confrontare e ordinare gli elementi.
  Se non specificato, gli elementi vengono confrontati direttamente.

* **`reverse`** (opzionale, default `False`):

  * `False` → ordine crescente (default)
  * `True` → ordine decrescente

### Ritorno

* Una **nuova lista** con gli elementi ordinati.

---

## 🔹 Esempi di base

```python
sorted([5, 2, 3, 1, 4])
# ➡️ [1, 2, 3, 4, 5]

sorted("python")
# ➡️ ['h', 'n', 'o', 'p', 't', 'y']

sorted({3, 1, 2})
# ➡️ [1, 2, 3]

sorted({'b': 2, 'a': 1, 'c': 3})
# ➡️ ['a', 'b', 'c']  (ordina le chiavi del dict)
```

---

## 🔹 Uso del parametro `key`

Il parametro `key` permette di specificare una funzione che **trasforma ogni elemento** prima del confronto.
La funzione viene chiamata **una sola volta per elemento**.

### Esempi:

🔸 Ordinamento case-insensitive

```python
parole = ["banana", "Apple", "cherry"]
sorted(parole, key=str.lower)
# ➡️ ['Apple', 'banana', 'cherry']
```

🔸 Ordinamento per lunghezza delle stringhe

```python
nomi = ["Luca", "Giovanni", "Anna"]
sorted(nomi, key=len)
# ➡️ ['Luca', 'Anna', 'Giovanni']
```

🔸 Ordinamento di tuple per un campo specifico

```python
studenti = [("Luca", 20), ("Anna", 18), ("Marco", 22)]
sorted(studenti, key=lambda stud: stud[1])  # ordina per età
# ➡️ [('Anna', 18), ('Luca', 20), ('Marco', 22)]
```

---

## 🔹 Uso del parametro `reverse`

```python
numeri = [1, 4, 2, 5]
sorted(numeri, reverse=True)
# ➡️ [5, 4, 2, 1]
```

---

## 🔹 Ordinamenti complessi (più chiavi)

Si possono combinare più criteri di ordinamento usando **tuple** o funzioni dal modulo `operator`.

```python
from operator import itemgetter

studenti = [
    ("Luca", "B", 20),
    ("Anna", "A", 22),
    ("Marco", "A", 19),
]

# Ordina prima per voto (colonna 1), poi per età (colonna 2)
sorted(studenti, key=itemgetter(1, 2))
# ➡️ [('Marco', 'A', 19), ('Anna', 'A', 22), ('Luca', 'B', 20)]
```

---

## 🔹 Stabilità dell’ordinamento

Python garantisce che `sorted()` sia **stabile**:
se due elementi hanno lo stesso valore di ordinamento, **mantengono l’ordine relativo originale**.

```python
dati = [("rosso", 1), ("blu", 1), ("rosso", 2)]
sorted(dati, key=itemgetter(0))
# ➡️ [('blu', 1), ('blu', 2), ('rosso', 1), ('rosso', 2)]
```

---

## 🔹 Casi d’uso comuni

* Ordinare stringhe ignorando maiuscole/minuscole.
* Ordinare numeri in ordine crescente o decrescente.
* Ordinare oggetti complessi in base a uno o più attributi.
* Ordinare strutture non list (set, dict, generatori).
* Ordinare tenendo conto della localizzazione (`locale`).

---

## 🔹 Differenza con `list.sort()`

| `sorted()`                                     | `list.sort()`                           |
| ---------------------------------------------- | --------------------------------------- |
| Funzione built-in                              | Metodo delle liste                      |
| Ritorna una **nuova lista**                    | Modifica la lista **in-place**          |
| Accetta qualsiasi iterabile                    | Solo oggetti `list`                     |
| Più sicuro quando serve conservare l’originale | Più efficiente se non serve l’originale |

---

## 📌 Conclusione

`sorted()` è uno strumento **generico, potente e flessibile** per ordinare qualsiasi iterabile in Python. Grazie al supporto di `key` e `reverse`, permette di implementare rapidamente ordinamenti semplici e complessi mantenendo leggibilità ed efficienza.

---
