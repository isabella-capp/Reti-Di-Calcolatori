# iptables

```bash
iptables [-t <table>] command [match] [target/jump]
```

**Iptables** è un'interfaccia a riga di comando per impostare, gestire ed ispezionare le tabelle delle regole di filtro dei pacchetti *IP* nel kernel Linux, ovvero un *firewall*. È strutturato in *tabelle*, ognuna con *catene* che contengono delle regole. Ogni *regola* specifica cosa bisogna fare per i pacchetti che rispettano certi requisiti.  

## Tabelle
In Linux, il framework Netfilter gestisce il traffico di rete tramite tabelle, che contengono catene (chains) di regole applicate ai pacchetti intercettati nei vari punti del percorso di inoltro (hook). Le principali tabelle
| **Tabella**  | **Uso principale**                                                      | **Hook di riferimento**                  |
| ------------ | ----------------------------------------------------------------------- | ---------------------------------------- |
| **FILTER**   | Regole di firewall (ACCEPT, DROP, FORWARD)                              | `LOCAL_IN`, `LOCAL_OUT`, `FORWARD`       |
| **NAT**      | Network Address Translation (SNAT, DNAT, masquerading, port forwarding) | `PREROUTING`, `LOCAL_OUT`, `POSTROUTING` |
| **MANGLE**   | Modifica pacchetti (header, marcatura, QoS, routing avanzato)           | Tutti gli hook                           |
| **RAW**      | Esclusione pacchetti dal connection tracking                            | `PREROUTING`, `LOCAL_OUT`                |
| **SECURITY** | Controlli Mandatory Access Control (es. SELinux)                        | `INPUT`, `OUTPUT`, `FORWARD`             |

## Catene
Ogni tabella possiede un insieme di catene predefinite, già esistenti e pronte per l'uso.
Quando si aggiunge una regola a una catena predefinita tramite iptables, quella regola verrà applicata in corrispondenza di un determinato hook di Netfilter, ovvero nel punto specifico del percorso del pacchetto in cui quella catena viene invocata.

| **Catena predefinita** | **Hook di Netfilter corrispondente** |
| --- | --- |
| **`INPUT`** | **`NF_IP_LOCAL_IN`** |
| **`OUTPUT`** | **`NF_IP_LOCAL_OUT`** |
| **`FORWARD`** | **`NF_IP_FORWARD`** |
| **`PREROUTING`** | **`NF_IP_PREROUTING`** |
| **`POSTROUTING`** | **`NF_IP_POSTROUTING`** |

## Impostare una politica di filtraggio predefinita
Ogni catena ha una **politica predefinita**, che può essere impostata usando l’opzione **`-P`** Questa politica definisce l'azione da applicare ai pacchetti che **non corrispondono ad alcuna regola** nella catena.

- **`ACCEPT`** accetta il pacchetto se nessuna regola corrisponde → quindi si aggiungono **regole per bloccare** traffico specifico.
- **`DROP`** scarta il pacchetto se nessuna regola corrisponde → quindi si aggiungono **regole per consentire** solo traffico autorizzato.

```bash
iptables [-t <tabella>] -P <catena> {ACCEPT|DROP}
```

Per cui quando ci viene chiesta una policy di blocco totale sul GW:

```bash
# Policy di default (blocco totale)
iptables -t filter -P INPUT DROP
iptables -t filter -P OUTPUT DROP
iptables -t filter -P FORWARD DROP
```
>⚠️ Se l’opzione `-t <tabella>` viene omessa, iptables opera sulla tabella FILTER (che è quella predefinita). 


## Regole di filtraggio

Le **regole di filtraggio** si aggiungono a una catena utilizzando l’opzione **`-A`** (append). Ogni regola è composta da **due parti**:

1. **Criteri di corrispondenza `matching criteria`** specificano a quali pacchetti la regola si applica. Sono indicati tramite opzioni specifiche nella riga di comando
2. **Azione**: viene applicata ai pacchetti che corrispondono ai criteri. Si specifica con l’opzione **`-j`**.

```bash
iptables [-t <tabella>] -A <catena> <matching criteria> -j <action>
```
Le azioni che possono essere utilizzate sono:
| **Azione** |**Descrizione** |
| ---------- | --------------------------------------------------------------------------------------------------------------------- |
| **DROP**   | Scarta il pacchetto silenziosamente, senza avvisare il mittente.                                                      |
| **REJECT** | Scarta il pacchetto notificando il mittente (es. TCP RST per TCP, ICMP Destination Unreachable per altri protocolli). |
| **ACCEPT** | Consente al pacchetto di proseguire normalmente nel percorso del kernel.                                              |
| **QUEUE**  | Invia il pacchetto a un’applicazione in **spazio utente** per elaborazioni aggiuntive.                                |
| **LOG**    | Registra informazioni sui pacchetti che corrispondono alla regola, senza alterarne il percorso.                       |

**Esempi:** 
> Accetta tutti i pacchetti del protocolollo *tcp* destinati alla porta *22*.  
```bash
iptables --table filter -A INPUT -p tcp --dport 22 -j ACCEPT
```
  
> Permetti al sistema di inoltrare pacchetti con protocollo *tcp* destinati alla porta *80*.  
```bash
iptables --table filter -A OUTPUT -p tcp --dport 80 -j ACCEPT
```

> Permetti il traffico tra due reti passanti da questo sistema che utilizza il protocollo *tcp* alla porta *443*.
```bash
iptables --table filter -A FORWARD -p tcp --dport 443 -j ACCEPT
```

## NAT (Network Address Translation)
Usata per la traduzione degli indirizzi IP, come il masquerading o il port forwarding.
- **DNAT**: Intercetta i pacchetti appena arrivano, prima che il *kernel* decida dove mandarli.  
> **Port Forwarding**, ad esempio, un server con *IP* pubblico *203.0.113.5* inoltra il pacchetto al server interno con *IP 192.168.1.100* sulla porta *80*.
```bash
iptables --table nat -A PREROUTING -p tcp -d 203.0.113.5 --dport 80 -j DNAT --to-destination 192.168.1.100
```

- **SNAT**: Agisce su qualsiasi pacchetto in uscita, dopo che il routing è stato deciso.  
> Un client della rete, con indirizzo *192.168.1.0/24* si maschera con l'indirizzo *IP* dell'interfaccia *eth0* del sistema locale.
```bash
iptables -t nat -A POSTROUTING -o eth0 -s 192.168.1.0/24 -j MASQUERADE
```

- **OUTPUT**: Agisce sui pacchetti generati dal sistema locale (dal *kernel* o da un programma in *user space*) ed agisce prima che il sistema decida dove instradare il pacchetto.  
> Intercetto tutto il traffico *HTTP* generato localmente e lo redireziono verso un *proxy* sulla porta *8080*
```bash
iptables --table nat -A OUTPUT -p tcp --dport 80 -j DNAT --to-destination 127.0.0.1:8080
```

## Comandi
- **-A, --append**: Aggiunge una regola alla fine di una catena esistente.  
```bash
iptables --table filter -A INPUT -p tcp --dport 22 -j ACCEPT
```

- **-D, --delete**: Elimina una regola da una catena esistente. Può essere fatto per *numero* o *specificando tutta la regola*.
```bash
iptables --table filter -D INPUT -p tcp --dport 22 -j ACCEPT
iptables --table filter -D INPUT 1
```

- **-I, --insert**: Inserisce una regola nella posizione specificata nella catena. Di default è *1*.
```bash
iptables --table filter -I INPUT -p tcp --dport 22 -j ACCEPT
```

- **-R, --replace**: Sostituisce una regola da una catena esistente in una posizione specificata.  
```bash
iptables --table filter -R INPUT 1 -p tcp --dport 22 -j ACCEPT
```

- **-L, --list**: Elenca tutte le regole presenti in una certa catena esistente.  
```bash
iptables --list INPUT
```

- **-F, --flush**: Cancella tutte le regole presenti in una certa catena esistente.  
```bash
iptables --flush INPUT
iptables --flush    # Elimina tutte le regole da tutte le catene nella tabella attiva.
```

- **-P, --policy**: Imposta la politica predefinita di una catena.  
```bash
iptables -P INPUT DROP
```

- **-N, --new-chain**: Crea una catena personalizzata.   
- **-X, --delete-chain**: Elimina una catena definita dall'utente.  

## Parametri
- **-p, --protocol protocollo**: Specifica il protocollo a cui applicare la regola
```bash
iptables -T filter -I INPUt -p tcp -j ACCEPT
```

- **-s, --source indirizzo**: Specifica un origine dei pacchetti, ad esempio un indirizzo *IP*.  
- **-d, --destination indirizzo**: Specifica una destinazione dei pacchetti, ad esempio un indirizzo *IP*.  
- **-j, --jump target**: Specifica che `target` eseguire se viene soddisfatta la regola.  
- **-i, --in-interface interfaccia**: Specifica da quale interfaccia è entrato il pacchetto.  
- **-o, --out-interface interfaccia**: Specifica da quale interfaccia uscirà il pacchetto.   

## Altre opzioni
- **-v, --verbose**: Quando utilizzato con `iptables -L`, stampa a schermo l'output verboso.  
- **-n, --numeric**: Gli indirizzi *IP* ed i numeri di porta vengono mostrati in formato numerico.  

## Match

### tcp
- **--dport porta**: Porta di destinazione.  
- **--sport porta**: Porta sorgente.  
- **--tcp-flags**: Controlla i flag tcp, ad esempio *SYN*, *ACK*.  

### udp
- **--dport porta**: Porta di destinazione.  
- **--sport porta**: Porta sorgente.  

### icmp
- **--icmp-type**: Specifica il tipo di pacchetto.  

## Match Estesi

- **-m --match modulo**: Specifica il modulo da caricare, serve per implementare regole dinamiche.  

### state
- **--state stato**: Permette di specificare uno o più stati di connessione, se associato con il monitoraggio delle connessioni, separati da virgole. Gli stati possibili sono:  
    - **INVALID**: Il pacchetto non può essere identificato per qualche motivo.  
    - **ESTABLISHED**: Il pacchetto è associato ad una connessione che ha già visto pacchetti in entrambe le direzioni. Fa parte di una connessione già aperta.    
    - **NEW**: Il pacchetto avvia una nuova connessione oppure è associato ad una connessione che non ha ancora visto traffico in entrambe le direzioni.  
    - **RELATED**: Il pacchetto avvia una nuova connessione ma ha relazioni ad una connessione già esistente (*FTP attivo* o *errore ICMP*).  

```bash
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
```

### limit
- **--limit rate**: Specifica la velocità media massima con cui i pacchetti possono corrispondere alla regola. Si indica come numero con suffisso `/second`, `/minute`, `/hour`, o `/day`.  
- **--limit-burst number**: Indica la quantità iniziale di pacchetti che è possibile far passare prima che venga applicata la regola `--limit`, ovvero il serbatoio massimo.  

```bash
iptables -t filter -A FORWARD -i eth+ -p icmp -m limit --limit 4/minute --limit-burst 3 -j ACCEPT
```

Appena parte il firewall, possono essere accettati fino a *3* pacchetti, dopo questi *3*, la ricarica del serbatorio avviene ogni *15 secondi* indicati da `4/minute` (*60 secondi / 4 = 15 secondi*).  

## Salvataggio delle configurazioni

```bash
iptables-save > iptables-config
iptables-restore < iptables-config
```