# 📂 Gestione dei file in Python

Python fornisce funzioni integrate per lavorare con i file (testo e binari).
Le operazioni principali sono: 
- **apertura**
- **lettura**
- **scrittura**
- **chiusura**



## Apertura di un file

Per aprire un file si utilizza la funzione integrata `open()`, che restituisce un **oggetto file**.

```python
file = open("nomefile.txt", "modalità")
```

### Modalità di apertura più comuni:

* `"r"` → lettura (default)
     >⚠️ Errore se il file non esiste.
* `"w"` → scrittura
     >⚠️ Crea il file se non esiste, altrimenti il file viene **sovrascritto**.
* `"a"` → append 
     >⚠️ Aggiunge contenuto alla fine del file.
* `"x"` → crea un nuovo file
     >⚠️ errore se esiste già.
* `"b"` → modalità binaria (es. `"rb"`, `"wb"`).
* `"t"` → modalità testo (default, es. `"rt"`, `"wt"`).
* `"r+"` → lettura e scrittura.


## Creazione di un file

Se si vuole **creare un nuovo file**:

```python
with open("nuovo.txt", <mode>) as file:
    pass
```

**or**

```python
file = open("nuovo.txt", <mode>)
file.write(<text>)
file.close()
```

Le modalità disponibili per la creazione di file sono:
- `"x"` → crea un nuovo file
- `"w"` → crea un nuovo file (sovrascrive se esiste già)
- `"a"` → crea un nuovo file (aggiunge se esiste già)

## Scrittura su un file

```python
file = open("dati.txt", "w")   # apre in scrittura
file.write("Prima riga\n")
file.write("Seconda riga\n")
file.close()
```

Per aggiungere senza cancellare il contenuto esistente:

```python
file = open("dati.txt", "a")   # append
file.write("Nuova riga\n")
file.close()
```



## Lettura da un file

### Leggere tutto il contenuto:

```python
file = open("dati.txt", "r")
contenuto = file.read()
print(contenuto)
file.close()
```

### Leggere una riga alla volta:

```python
file = open("dati.txt", "r")
riga1 = file.readline()
riga2 = file.readline()
file.close()
```

### Leggere tutte le righe in una lista:

```python
file = open("dati.txt", "r")
righe = file.readlines()
for riga in righe:
    print(riga.strip())
file.close()
```

## Chiusura di un file

Dopo aver finito di leggere/scrivere, è buona pratica chiudere il file:

```python
file.close()
```

## Uso di `with` (gestione automatica)

In Python si usa spesso `with` per gestire i file:
il file viene **aperto** e chiuso automaticamente.

```python
with open("dati.txt", "r") as file:
    contenuto = file.read()
    print(contenuto)
# qui il file è già chiuso
```


## Modalità binaria

Per lavorare con immagini, audio o file binari:

```python
# Lettura binaria
with open("immagine.png", "rb") as file:
    dati = file.read()

# Scrittura binaria
with open("copia.png", "wb") as file:
    file.write(dati)
```

## Posizionamento nel file (`seek` e `tell`)

* `file.tell()` → restituisce la posizione corrente (in byte).
* `file.seek(offset)` → sposta il cursore alla posizione indicata.

```python
with open("dati.txt", "r") as f:
    print(f.read(5))      # leggo 5 caratteri
    print(f.tell())       # posizione corrente
    f.seek(0)             # torno all’inizio
    print(f.read(5))      # rileggo i primi 5 caratteri
```

## Gestione eccezioni

Quando si lavora con file, è utile usare il **try/except** per gestire errori (es. file inesistente):

```python
try:
    with open("inesistente.txt", "r") as f:
        contenuto = f.read()
except FileNotFoundError:
    print("Il file non esiste!")
```
