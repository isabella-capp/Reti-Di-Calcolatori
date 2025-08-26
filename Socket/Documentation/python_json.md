
# 📌 Documentazione su **JSON in Python**

**JSON** (*JavaScript Object Notation*) è un formato standard per scambiare dati strutturati (simile a un dizionario Python).
In Python si lavora con JSON usando il modulo **`json`**.

```python
import json
```


## Metodi principali

| Metodo         | Input                 | Output                 | Quando usarlo                                                                                                          |
| -------------- | --------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `json.dumps()` | Oggetto Python        | **Stringa JSON**       | Quando vuoi convertire un oggetto Python (es. `dict`, `list`) in una stringa JSON (per stamparlo o inviarlo via rete). |
| `json.dump()`  | Oggetto Python + file | Scrittura su file JSON | Quando vuoi salvare un oggetto Python direttamente in un file JSON.                                                    |
| `json.loads()` | Stringa JSON          | **Oggetto Python**     | Quando ricevi una stringa JSON (es. da API o da un file letto come testo) e vuoi convertirla in un oggetto Python.     |
| `json.load()`  | File JSON aperto      | **Oggetto Python**     | Quando vuoi leggere un file JSON e trasformarlo in un oggetto Python.                                                  |



## Da Python → JSON

### 🔹 `dumps()` → Oggetto Python → Stringa JSON

```python
import json

persona = {
    "nome": "Alice", 
    "eta": 25, 
    "is_student": False
}

json_string = json.dumps(persona)   # converto in stringa JSON
print(json_string)
# {"nome": "Alice", "eta": 25, "is_student": false}
```
👉 Usalo quando devi inviare JSON come **stringa** (es. via API, socket, salvataggio in file di testo).

### 🔹 `dump()` → Oggetto Python → File JSON

```python
persona = {"nome": "Bob", "eta": 30}

with open("persona.json", "w") as f:
    json.dump(persona, f, indent=4)   # scrivo direttamente su file
```

👉 Usalo quando devi salvare su file.


## Da JSON → Python

### 🔹 `loads()` → Stringa JSON → Oggetto Python

```python
json_string = '{"nome": "Alice", "eta": 25, "is_student": false}'
dati = json.loads(json_string)
print(dati["nome"])  # Alice
```

👉 Usalo quando ricevi JSON come **stringa** (es. da API, socket, file letto con `read()`).


### 🔹 `load()` → File JSON → Oggetto Python

```python
with open("persona.json", "r") as f:
    dati = json.load(f)
print(dati["nome"])  # Bob
```

👉 Usalo quando hai un **file JSON** già salvato.

## Opzioni utili

### 🔹 Indentazione e leggibilità

Serve per rendere il JSON più leggibile, aggiungendo spazi e a capo.
- Senza `indent`, il JSON è scritto tutto su una riga.

- Con `indent`, ogni livello di annidamento è indentato di n spazi.

```python
print(json.dumps(persona, indent=4))
```
**output**

```python
{
    "nome": "Alice",
    "eta": 25,
    "corsi": [
        "Python",
        "AI"
    ]
}
```

### 🔹 Ordinamento delle chiavi

Per default, le chiavi di un dizionario mantengono l’ordine di inserimento.
Con `sort_keys=True`, Python ordina alfabeticamente le chiavi del JSON.

```python
print(json.dumps(persona, sort_keys=True, indent=2))
```

### 🔹 Separatore personalizzato

Per default, JSON usa:
- `,` (virgola + spazio) tra elementi

- `:` (due punti + spazio) tra chiave e valore

Con `separators=(item_separator, key_separator)` puoi cambiare questi simboli/spazi.

```python
persona = {"nome": "Alice", "eta": 25}

# Default (con spazi)
print(json.dumps(persona))
# {"nome": "Alice", "eta": 25}

# Separatore compatto (nessuno spazio)
print(json.dumps(persona, separators=(",", ":")))
# {"nome":"Alice","eta":25}

# Separatore personalizzato
print(json.dumps(persona, separators=(", ", " = ")))
# {"nome" = "Alice", "eta" = 25}
```

## Tipi supportati

| Python          | JSON     |
| --------------- | -------- |
| `dict`          | `object` |
| `list`, `tuple` | `array`  |
| `str`           | `string` |
| `int`, `float`  | `number` |
| `True`          | `true`   |
| `False`         | `false`  |
| `None`          | `null`   |

⚠️ Tipi non supportati (es. `set`) generano errore.

## 7. Gestione errori

```python
import json

try:
    dati = json.loads('{"nome": "Alice", "eta": 25,}')  # JSON non valido
except json.JSONDecodeError as e:
    print("Errore nel parsing JSON:", e)
```

