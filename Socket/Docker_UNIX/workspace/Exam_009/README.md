#  Appello del 21 luglio 2025

 Scrivere un server in grado di eseguire un semplice calcolo su un dato ricevuto via rete. Nello specifico si vuole creare un server che processa un numero in virgola mobile che può essere sia:
 - 32 bit (float a precisione singola) 
 - 64 bit (double a precisione doppia) 
 Ritorna un altro numero in virgola mobile con uguale precisione ma che rappresenta un valore doppio rispetto al valore spedito.

 ### Server

 Il server dovrà porsi in ascolto sulla porta 3000 in attesa di messaggi da parte del client. Alla ricezione dei dati del client il server dovrà leggere un messaggio strutturato come segue:

- 1 byte con valore 1 se il numero che segue è un float a 32 bit e 2 se il  numero che segue è un double a 64 bit (Nota: 1 e 2 sono numeri interi,  non il carattere '1' o '2')
- un campo di lunghezza 4 o 8 byte di dati da interpretare come numero in virgola mobile a 32/64 bit

Successivamente il server dovrà inviare sulla stessa connessione una risposta contenente un altro messaggio con lo stesso formato precedentemente descritto e con i numeri aventi la stessa dimensione del messaggio di richiesta. Il messaggio prevede che la risposta abbia la stessa precisione della richiesta. Dopo aver ricevuto la risposta del server il client chiude la connessione. In questa fase il server deve anche scrivere su standard output una frase come segue:

```bash
 Serving client request: <client-input> <server-output>
```

Si assume che client e server abbiano la stessa rappresentazione interna dei float basta sullo standard IEEE 754 e che non sia necessaria alcuna conversione. Il server deve essere in grado di servire numerose richieste da parte dei client, senza bisogno di essere lanciato nuovamente ogni volta. Tuttavia non è necessario supportare esplicitamente un sistema di concorrenza basata su `fork()` o usando
thread.

Per la verifica della correttezza dell’esercizio si può fare riferimento al client fornito