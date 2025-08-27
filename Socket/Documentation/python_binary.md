# 📘 Documentazione su `struct` in Python

La libreria **`struct`** di Python fornisce strumenti per **convertire** dati Python (interi, float, stringhe di byte) in **rappresentazioni binarie** (`bytes`) e viceversa.
È molto utile quando si lavora con protocolli di rete, formati di file binari (es. immagini, WAV, BMP, eseguibili) o interfacce a basso livello (es. C, sistemi embedded).


## Importazione

```python
import struct
```


## Concetti chiave

### Pack (impacchettamento)
   
   Converte valori Python → sequenze di byte (`bytes`).

   ```python
   struct.pack(format, v1, v2, ...)
   ```

   * `format` = stringa che descrive come tradurre i valori.
   * `v1, v2, ...` = valori Python da impacchettare.

### Unpack (spacchettamento)
   Converte sequenze di byte → valori Python.

   ```python
   struct.unpack(format, buffer)
   ```

   * `format` = deve corrispondere a quello usato nel `pack`.
   * `buffer` = oggetto `bytes` con i dati binari.

### Calcolo dimensione
   Prima di leggere un blocco binario, è utile sapere quanti byte servono.

   ```python
   struct.calcsize(format)
   ```


## Il formato (`format string`)

Il parametro `format` indica **tipo di dato** e **endianness**.
È composto da un **prefisso opzionale** e da una sequenza di **specifier**.



### 📌 Prefissi per **endianness** e allineamento

| Simbolo       | Significato                                                                      |
| ------------- | -------------------------------------------------------------------------------- |
| `@` (default) | Ordine nativo della macchina, allineamento nativo (dipende da CPU e C compiler). |
| `=`           | Ordine nativo, **senza** allineamento.                                           |
| `<`           | Little-endian (byte meno significativo prima).                                   |
| `>`           | Big-endian (byte più significativo prima).                                       |
| `!`           | Network order (big-endian), usato nei protocolli di rete.                        |

👉 Esempio:

```python
struct.pack("<I", 100)   # intero senza segno a 32 bit in little endian
struct.pack(">I", 100)   # intero senza segno a 32 bit in big endian
```


### 📌 Tipi di dati supportati

| Codice | Tipo C corrispondente   | Tipo Python       | Dimensione (byte)       |
| ------ | ----------------------- | ----------------- | ----------------------- |
| `x`    | padding byte            | -                 | 1                       |
| `c`    | char                    | `bytes(1)`        | 1                       |
| `b`    | signed char             | `int`             | 1                       |
| `B`    | unsigned char           | `int`             | 1                       |
| `?`    | *bool* (C99)            | `bool`            | 1                       |
| `h`    | short                   | `int`             | 2                       |
| `H`    | unsigned short          | `int`             | 2                       |
| `i`    | int                     | `int`             | 4                       |
| `I`    | unsigned int            | `int`             | 4                       |
| `l`    | long                    | `int`             | 4                       |
| `L`    | unsigned long           | `int`             | 4                       |
| `q`    | long long               | `int`             | 8                       |
| `Q`    | unsigned long long      | `int`             | 8                       |
| `f`    | float                   | `float`           | 4                       |
| `d`    | double                  | `float`           | 8                       |
| `s`    | char\[]                 | `bytes`           | definita da un numero   |
| `p`    | char\[] (Pascal string) | `bytes`           | definita da un numero   |
| `P`    | void\*                  | `int` (indirizzo) | dipende da architettura |

👉 È possibile specificare quantità:

* `"4s"` → stringa di 4 byte.
* `"10p"` → Pascal string di max 10 byte.
* `"2i"` → due interi consecutivi.



## 🔹 Esempi pratici

### 🔸 1. Pack e Unpack di un intero

```python
data = struct.pack("i", 12345)   # intero in 4 byte
print(data)  # b'90\x00\x00' su little endian

value = struct.unpack("i", data)
print(value)  # (12345,)
```

---

### 🔸 2. Più valori

```python
data = struct.pack("i f s", 42, 3.14, b"A")
print(data)  

values = struct.unpack("i f s", data)
print(values)  # (42, 3.14, b'A')
```

---

### 🔸 3. Stringhe fisse e Pascal string

```python
# stringa fissa da 10 byte
data = struct.pack("10s", b"ciao")
print(data)  # b'ciao\x00\x00\x00\x00\x00\x00'

# Pascal string (lunghezza + contenuto)
data = struct.pack("10p", b"ciao")
print(data)  # b'\x04ciao\x00\x00\x00\x00\x00\x00'
```

---

### 🔸 4. Lettura di file binari

Supponiamo un file che contiene una **struttura C**:

```c
struct header {
    unsigned int id;
    unsigned short version;
    float value;
};
```

Per leggerlo in Python:

```python
fmt = "<I H f"   # little-endian: unsigned int, unsigned short, float
size = struct.calcsize(fmt)

with open("file.bin", "rb") as f:
    block = f.read(size)
    id, version, value = struct.unpack(fmt, block)

print(id, version, value)
```

---

## 🔹 Funzioni principali

* **`struct.pack(fmt, v1, v2, ...)`** → bytes
* **`struct.unpack(fmt, buffer)`** → tuple
* **`struct.iter_unpack(fmt, buffer)`** → iteratore che spacchetta più volte il buffer (utile per file grandi)
* **`struct.pack_into(fmt, buffer, offset, v1, v2, ...)`** → inserisce i dati direttamente in un `bytearray` esistente
* **`struct.unpack_from(fmt, buffer, offset=0)`** → spacchetta leggendo da un offset in un buffer
* **`struct.calcsize(fmt)`** → ritorna la dimensione in byte richiesta dal formato



## 🔹 Differenza `s` vs `p`

* `"Ns"` → **stringa fissa** di N byte (riempita con `\x00` se più corta).
* `"Np"` → **Pascal string**, il primo byte indica la lunghezza, seguito dai dati, riempito fino a N.

---

## 🔹 Errori comuni

1. **Mismatch tra formato e buffer**

   ```python
   struct.unpack("i", b"\x01\x02")  # ValueError: buffer too small
   ```

2. **Endianness sbagliato**

   * `<I` vs `>I` danno risultati diversi.
   * Sempre chiarire con quale endian il file/protocollo è stato scritto.

3. **Stringhe troppo lunghe**

   * `"4s"` → accetta max 4 byte.
   * Se passi `b"ciao!"` viene **troncata** a `b"ciao"`.



## 🔹 Quando usare `struct`

* Parsing di **formati binari** (WAV, PNG, BMP, eseguibili).
* Comunicazioni con dispositivi hardware o **protocolli binari**.
* Implementazioni di protocolli di rete a basso livello.
* Conversioni tra strutture C e Python.

