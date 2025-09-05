# Esercizio 2 — Conversione stringhe

Scrivere un server che riceve dal client una stringa in UTF-8 e restituisce la stessa stringa tutta in maiuscolo.
Il messaggio ha il seguente formato:

- 2 byte (unsigned short, big endian) che rappresentano la lunghezza della stringa.
- N byte con il contenuto della stringa.

Il server deve rispondere con lo stesso formato (2 byte di lunghezza + stringa modificata).