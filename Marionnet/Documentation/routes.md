# Routes

Il routing è il processo con cui un sistema operativo (es. Linux) decide dove inoltrare un pacchetto IP in base alla destinazione (`IP di destinazione`).

Il kernel consulta la **tabella di routing**, che contiene regole del tipo:

```
Destinazione       Gateway/Nexthop   Interfaccia
```

* **Destinazione (network/host)**: la rete o l’host che vogliamo raggiungere (es. `192.168.1.0/24`, `8.8.8.8/32`).
* **Gateway (via)**: il router successivo a cui passare i pacchetti, se la destinazione non è direttamente collegata.
* **Interfaccia (dev)**: la scheda di rete su cui spedire i pacchetti (se non si usa un gateway).

## Sintassi

Una riga di routing in Linux ha tre elementi principali:

```php-template
ip route add <rete_destinazione> via <next-hop> dev <interfaccia>
```

- **rete_destinazione** → es. `192.168.200.0/24`, `0.0.0.0/0`, `2.2.2.2/32`
- **via** `<next-hop>` → l’indirizzo IP del gateway successivo (deve essere raggiungibile su una rete direttamente connessa)
- **dev** `<interfaccia>` → opzionale, serve quando vuoi forzare su quale scheda mandare i pacchetti o quando non c’è un “via” (rotta diretta).


## Tipi di rotte

### 🔹 Rotte dirette (connected)

Quando un’interfaccia ha un IP, la rete a cui appartiene è automaticamente raggiungibile.
Esempio:

```
auto eth0
iface inet static
    address 192.168.100.254
    netmask 255.255.255.0
```

In questo caso non ho bisogno di regole aggiuntive per raggiungere un host all'interno della mia stessa rete 192.168.100.0/24.

### 🔹 Rotte statiche

Aggiunte manualmente con:

```
ip route add <rete_destinazione> via <next-hop>
```

Si usano quando la rete non è direttamente collegata, ma si trova dietro un router intermedio (next-hop).

**Esempio:**

```
ip route add 192.168.200.0/24 via 1.1.1.1
```

👉 **Significa:** “per raggiungere la rete `192.168.200.0/24`, manda i pacchetti al router `1.1.1.1`. Poi sarà quel router a proseguire il cammino.

Qui serve `via` perché non posso mandare i pacchetti direttamente: quella rete non è connessa alla mia scheda.

### 🔹 Default route

Usata quando non esiste una regola più specifica.
Esempio:

```
ip route add default via 192.168.100.1
```

→ tutti i pacchetti per reti “sconosciute” vanno a `192.168.100.1`.

### 🔹 Rotte host

Valide solo per un singolo IP:

```
ip route add 2.2.2.2 dev eth1
```

👉 **Significa:** “per parlare con l’host `2.2.2.2`, manda i pacchetti direttamente sulla scheda `eth1`.

Queste si usano tipicamente quando:
- hai un **link punto-punto** (es. PPP, VPN, /32)**
- vuoi creare eccezioni particolari (es. dire che un host singolo deve essere raggiunto via una strada diversa da tutta la sua rete).


## FAQ
### Perché non posso usare via con indirizzi /32?

Un indirizzo `/32` (maschera `255.255.255.255`) non rappresenta una rete, ma un singolo host.
Esempio:

```bash
iface eth0 inet static
    address 1.1.1.1
    netmask 255.255.255.255
```

Questo significa che la macchina “conosce” solo sé stessa (1.1.1.1).

**Non esiste una “rete” comune dove trovare un vicino** → quindi non puoi usare via 1.1.1.1 come next hop, perché il kernel non saprebbe come raggiungerlo (non è su una rete condivisa).

➡️ **Per poter usare via**, il next hop deve appartenere a una rete direttamente connessa.


Perfetto 👍, ti preparo una **documentazione dettagliata e organica sul routing in Linux**, con esempi pratici e collegamenti al tuo laboratorio (router GWC e GWS).

### Differenza `via` vs `dev`

* **`via` (gateway/next-hop)**
  Serve quando il pacchetto deve essere consegnato a un router vicino.
  Il next-hop deve appartenere a una rete **direttamente connessa**.

* **`dev` (interfaccia)**
  Si usa quando la destinazione è direttamente collegata (es. host su punto-punto o con indirizzo /32).
  Qui non serve un router intermedio → il kernel invierà ARP sull’interfaccia per cercare quell’host.

📌 Regola:

* Se la destinazione è una **rete** → `via`
* Se la destinazione è un **host punto-punto** → `dev`

## Errori comuni

* `RTNETLINK answers: File exists` → stai aggiungendo una rotta che c’è già.
* Usare `via` con un host non raggiungibile → il kernel non sa come inviare i pacchetti.
* **Mancanza di rotta di ritorno** → il ping non funziona anche se il pacchetto parte.
* `via` indica l’IP del router next-hop, non una rete, per cui è sbagliato inserire la netmask.