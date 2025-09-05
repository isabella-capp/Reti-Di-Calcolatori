# Esercizio 4 — Conversione temperatura

Scrivere un server che riceve una misura di temperatura dal client e restituisce la conversione:

Il messaggio in ingresso è:
- 1 byte che indica l’unità (1 = Celsius, 2 = Fahrenheit).
- 4 byte (float 32 bit) che rappresentano la misura.

Il server deve convertire:
- Se input è Celsius, output in Fahrenheit.
- Se input è Fahrenheit, output in Celsius.

Il messaggio di risposta deve avere lo stesso formato: 1 byte (unità di destinazione) + 4 byte (float).