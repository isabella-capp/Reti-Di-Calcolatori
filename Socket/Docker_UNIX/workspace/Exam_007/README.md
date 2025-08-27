# Laboratorio

Si chiede di realizzare un client e un server di rete.
Il **server** deve mettersi in ascolto sulla porta 5000.
Il **client** si connette al server e invia una stringa ottenuta concatenando la stringa "token from client: " a una stringa definita dall'utente e passata al client come parametro linea di comando. 

>Inviare solo il messaggio dell'utente, senza l'intera stringa "token from..." è considerato un errore.

Il **server** riceve la stringa, estrae la sottostringa indicata dall'utente, la trasforma con l'algoritmo ROT13, la concatena alla stringa "token from server: " e la rispedisce al client.
Il **client** riceve il messaggio del server, estrae la sottostringa, la stampa e chiude la connessione.
Per l'implementazione dell'algoritmo di ROT13 può fare riferimento alla seguente funzione python:

```python
def rot13(x):
    x = x.lower()
    alpha = "abcdefghijklmnopqrstuvwxyz"
    return "".join([alpha[(alpha.find(c)+13)%26] for c in x])
```

L'algoritmo ROT13 è descritto su wikipedia: https://it.wikipedia.org/wiki/ROT13

Di seguito un esempio di funzionamento. Invocazione di server e client:
- Invocazione server:
    ```bash
    python server.py
    ```
- Invocazione client:
    ```bash
    python client.py 127.0.0.1 prova
    ```
Scambio d' messaggi sulla rete:
- **(client -> server)** token from client: prova
- **(server -> client)** token from server: cebin

**Output client:**
```python
Spedito token: "prova"
Ricevuto token: "cebin"
```

Non ci sono vincoli per l'output del server.

**Questo aggiuntivo:** implementare una ulteriore versione del server che applichi l'algoritmo ROT11 (il cui
funzionamento è analogo a ROT13) su un alfabeto di 22 lettere che non comprende caratteri: "k", "w", "x", "y"

**Elementi di valutazione:**
1. Il server si mette in ascolto sulla porta 5000 (verificare con SS -I)
2. Il client si connette con successo (verificare con tcpdump)
3. Il client invia il messaggio al server con il formato indicato (verificare con tcpdump)
4. Il server risponde al client con il formato indicato (verificare con tcpdump)
5. L'output prodotto dal client è conforme ai requisiti
6. Qualità del codice
7. Quesito aggiuntivo
8. Penalità per discrepanze rispetto ai requisiti