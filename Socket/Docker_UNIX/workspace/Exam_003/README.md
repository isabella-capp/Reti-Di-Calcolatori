# 7.3 Specifiche

Si vuole realizzare un’applicazione client/server che consente a un client di scaricare un file dal server.

Il server dovrà porsi in attesa di richieste da parte del client sulla porta TCP `8080`. 

Una richiesta è costituita da una stringa JSON (una notazione che può essere usata per rappresentare dictionary). La richiesta deve essere strutturata come di seguito: se si vuole scaricare il file file.txt la richiesta sarà strutturata come: 
```bash
{
"filename": "file.txt"
}
```

A questa richiesta il server dovrà rispondere con una struttura JSON seguita dal contenuto del file. La risposta dovrà contenere le seguenti informazioni:

``` bash
{
"filename": "file.txt"
"filesize": "853"
}
<853 bytes of file content>
``` 
A fronte di questa risposta il client dovrà creare un file con il nome indicato e riempirlo con i dati trasferiti dal server, quindi chiudere la connessione con il server.
Per la gestione delle informazioni in formato JSON si rimanda al modulo json disponibile per il linguaggio Python.
