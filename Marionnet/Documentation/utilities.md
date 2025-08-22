## Firewall

Quando si lavora con i firewall, è buona pratica seguire un approccio graduale: pulizia delle regole esistenti, definizione di policy di default, e apertura selettiva del traffico necessario.

### Scenario di riferimento

Per coerenza, tutti gli esempi utilizzano questo schema di rete:

- **Firewall (gateway)**
    - `eth0` → `10.0.1.1`
    - `eth1` → `192.168.0.1`
    - `eth2` → `5.4.3.2`
- LAN `10.0.1.0/25`
    - H1: `10.0.1.10`
    - H2: `10.0.1.11`
- DMZ `192.168.0.0/24`
    - Web server: `192.168.0.100`
    - FTP server: `192.168.0.101`
    - DNS server: `192.168.0.102`
- Internet
    - EXT `2.3.4.5`

### Pulizia delle regole esistenti

```bash
#!/bin/bash

# Svuota tutte le regole esistenti
iptables -F
iptables -t nat -F
iptables -t mangle -F

# Elimina tutte le catene personalizzate
iptables -X
iptables -t nat -X
iptables -t mangle -X

# Ripristina le policy di default (tutto ACCETTATO)
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

echo "Firewall reset: tutte le regole rimosse, traffico consentito."

```

### Policy di blocco totale

Per implementare la negazione implicita del traffico, si possono impostare le policy di default a DROP:

```bash
# Policy di default (blocco totale)
iptables -t filter -P INPUT DROP
iptables -t filter -P OUTPUT DROP
iptables -t filter -P FORWARD DROP
```
> ⚠️ Con queste regole, tutto il traffico è bloccato se non esistono eccezioni specifiche.

### DHCP

Quando blocchiamo esplicitamente tutto il traffico per permettere l'assegnamento degli IP in modo dinamico agli host della LAN dobbiamo consentire il traffico DHCP

**Regole per un client DHCP su eth0**

1. Accettare le risposte del server DHCP (porta 67 → 68)
    ```bash
   iptables -A INPUT -i eth0 -p udp --sport 67 --dport 68 -j ACCEPT
   ```
   - **Catena:** `INPUT` → pacchetti diretti alla macchina.
   - **Interfaccia:** `-i eth0` → solo pacchetti in arrivo su eth0.
   - **Protocollo:** `-p udp` (DHCP usa UDP).
   - **Porte:**  `--sport 67 --dport 68` → dal server DHCP (67) al client (68).
   - **Significato:** consente le **risposte del server** 
   - **Azione:** `ACCEPT` → lascia passare queste risposte verso lo stack locale.

2. Consentire l’inoltro delle richieste DHCP (porta 68 → 67)
    ```bash
   iptables -A OUTPUT -o eth0 -p udp --sport 68 --dport 67 -j ACCEPT
   ```

   * **Catena:** `OUTPUT` → pacchetti originati dalla macchina.
   * **Interfaccia:** `-o eth0` → inviati su `eth0`.
   * **Porte:** `--sport 68 --dport 67` → **dal client (68) al server (67)**.
   * **Significato:** consente le richieste del client(DHCPDISCOVER, DHCPREQUEST).

**Note utili**:

* Le porte **67/68** sono quelle standard DHCPv4 (**server 67**, **client 68**).
* Queste regole valgono per un client o per un firewall che agisce da relay DHCP.
* Se la macchina fosse un server DHCP, le regole INPUT/OUTPUT si invertirebbero:
   ```bash 
    INPUT: --sport 68 --dport 67
    OUTPUT: --sport 67 --dport 68
    ```
***Verifica del funzionamento***:
```bash
ifdown -a   # Su un host che utilizza DHCP
ifup -a     # Su un host che utilizza il DHCP
```


### DNS
Il DNS è il servizio che permette di risolvere nomi di dominio in indirizzi IP. Per garantire la connettività tra client e server DNS, è necessario configurare correttamente il firewall, consentendo sia le richieste dei client sia le risposte del server.
| Catena      | Quando si usa                                             | Esempio DNS                                                                           |
| ----------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **INPUT**   | Pacchetti destinati al firewall stesso                    | Richieste DNS che il firewall deve processare localmente (server DNS sul firewall)    |
| **OUTPUT**  | Pacchetti generati dal firewall                           | Risposte DNS generate dal firewall verso i client                                     |
| **FORWARD** | Pacchetti che **attraversano il firewall** tra due subnet | Richieste DNS dai client della DMZ verso un server DNS nella LAN, e relative risposte |
> 🗝️ il FORWARD si usa solo se il traffico non è destinato al firewall, ma deve passare da una rete all’altra.

1. **Traffico DNS verso il firewall (INPUT/OUTPUT):**

    Per consentire ai client della LAN o DMZ di interrogare il server DNS sul firewall:
    ```bash
    # Richieste in ingresso al firewall (porta destinazione 53)
    iptables -A INPUT -i eth0 -p udp -s 10.0.1.0/25 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT

    # Risposte generate dal firewall verso i client
    iptables -A OUTPUT -o eth0 -p udp -d 10.0.1.0/25 --sport 53 -m state --state ESTABLISHED -j ACCEPT
    ```
    Spiegazione porte:

    * Le richieste DNS dei client partono generalmente da porte alte casuali verso porta 53 del server.
    * Le risposte del server DNS vengono inviate dalla porta 53 verso la porta alta del client.
    * Questo schema spiega perché in INPUT si usa `--dport 53` e in OUTPUT `--sport 53`.

2. **Regole DNS per traffico tra subnet (FORWARD)**
    Se il firewall deve inoltrare le richieste DNS dalla DMZ verso un server DNS nella LAN:
    ```bash
    # Richieste DNS LAN -> DMZ
    iptables -t filter -A FORWARD -i eth0 -o eth1 -p udp --dport 53 -s 10.0.1.0/25 -d 192.168.0.102 -m state --state NEW,ESTABLISHED -j ACCEPT

    # Risposte DNS DMZ -> LAN
    iptables -t filter -A FORWARD -i eth1 -o eth0 -p udp --sport 53 -s 192.168.0.102 -d 10.0.1.0/25 -m state --state ESTABLISHED -j ACCEPT
    ```

    Spiegazione:

    - **Il traffico DNS attraversa il firewall:** i pacchetti non sono destinati al firewall stesso, ma devono essere inoltrati tra subnet diverse.
    - `--dport 53` per le richieste (arrivano alla porta 53 del server)
    - `--sport 53` per le risposte (partono dalla porta 53 del server verso la porta alta del client)
    - La connessione viene tracciata con state `NEW,ESTABLISHED` per le richieste e `ESTABLISHED` per le risposte.

***Verifica del funzionamento***:
```bash
dig google.com
```
Se ricevi una risposta corretta, significa che le regole INPUT, OUTPUT e FORWARD consentono correttamente le richieste e le risposte DNS

### SHH

Il servizio SSH permette di gestire in modo sicuro i dispositivi della rete tramite accesso remoto. Per consentire connessioni SSH verso il firewall o server dalla LAN, è necessario configurare correttamente le regole del firewall.

```bash
# Consentire connessioni SSH in ingresso dalla LAN
iptables -A INPUT -i eth0 -p tcp -s 10.0.1.0/25 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT

# Consentire risposte SSH in uscita verso il client
iptables -A OUTPUT -o eth0 -p tcp -d 10.0.1.0/25 --sport 22 -m state --state ESTABLISHED -j ACCEPT
```

**Spiegazione delle regole:**

- **INPUT**
    - `-i eth0` → pacchetti in arrivo sull’interfaccia della LAN.
    - `-p tcp` → SSH utilizza TCP.
    - `--dport 22` → porta standard SSH.
    - `-s <subnet>>` → solo il client autorizzato può connettersi.
    - `--state NEW,ESTABLISHED` → permette nuove connessioni e pacchetti di sessioni già stabilite.
    - `-j ACCEPT` → accetta i pacchetti corrispondenti.

- **OUTPUT**
   - `-o eth0` → pacchetti in uscita sull’interfaccia LAN.
   - `--sport 22` → pacchetti generati dal firewall/host SSH.
   - `-d <subnet>` → verso il client autorizzato.
   - `--state ESTABLISHED` → solo pacchetti di sessioni già aperte.
   - `-j ACCEPT` → accetta i pacchetti di risposta.

***Verifica del funzionamento***:
```bash
ssh <ip> #DALLA LAN
```

### HTTP
Il servizio HTTP utilizza il protocollo TCP sulla porta 80. Per permettere l’accesso a un server web da Internet o dalla LAN, è necessario configurare correttamente le regole FORWARD del firewall.
1. **Connessioni da Internet verso il server web**

    Consentire a qualunque host esterno su Internet di connettersi al server web pubblico:

    ```bash
    iptables -t filter -A FORWARD -i eth2 -o eth1 -d 192.168.0.100 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -t filter -A FORWARD -i eth1 -o eth2 -s 192.168.0.100 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT
    ```
    Spiegazione:
    - `eth2 → eth1`: traffico proveniente da Internet verso la DMZ.
    - `--dport 80`: pacchetti destinati al server web.
    - `--state NEW,ESTABLISHED`: consente sia nuove connessioni sia pacchetti di sessioni già aperte.
    - Regola inversa (`--sport 80`): consente le risposte del server verso l’host esterno.

    > ⚠️ Se non conosci l’IP sorgente di Internet, puoi omettere la specifica dell’IP sorgente (come in questo esempio).

2. **Connessioni dalla LAN verso il server web**
    Consentire agli host della LAN di raggiungere il server web pubblico:
    ```bash
    iptables -t filter -A FORWARD -i eth0 -o eth1 -s 10.0.1.0/25 -d 192.168.0.100 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -t filter -A FORWARD -i eth1 -o eth0 -s 192.168.0.100 -d 10.0.1.0/25 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT
    ```
    Spiegazione:
    - `-i eth0 -o eth1` → traffico originato dalla LAN verso la DMZ.
    - `--dport 80` → porta di destinazione HTTP.
    - Risposte tracciate con `--sport 80` e stato ESTABLISHED.

3. **Connessioni da un host pubblico EXT verso un server privato SRV**
    Se il server web è privato (es. DMZ), devi consentire a uno specifico host pubblico di contattarlo:
    ```bash
    iptables -t filter -A FORWARD -i eth2 -o eth1 -s 2.3.4.5 -d 192.168.0.100 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -t filter -A FORWARD -o eth1 -i eth2 -d 192.168.0.100 -d 2.3.4.5 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT
    ```
    > ⚠️ se il server è privato, devi anche configurare la regola di PREROUTING per il NAT, in modo che il traffico in ingresso venga inoltrato correttamente al server privato.

**Spiegazione**

- Le richieste partono da porte alte casuali dei client verso la porta 80 del server web (`--dport 80`).

- Le risposte del server partono dalla porta 80 verso le porte alte dei client (`--sport 80`).

- Il modulo state (`NEW,ESTABLISHED`) traccia lo stato delle connessioni TCP, consentendo solo pacchetti validi.

***Verifica del funzionamento***: <!-- Probabilmente non va bene, va usato nc -->
```bash
nc -l -p 80         # Server
nc -vz <IP> 80      # Client
```
- `-l -p 80` → ascolta sulla porta 80 del server
- `-vz` → connessione di test dal client (verbose + scan della porta)

Se la connessione viene stabilita, significa che le regole FORWARD permettono correttamente il traffico HTTP tra client e server.

### ICMP

Il protocollo ICMP viene utilizzato per scopi diagnostici e di controllo, ad esempio:
- **Ping** (echo request/echo reply) per verificare la raggiungibilità di un host.
- **Messaggi di errore** (es. destination unreachable, time exceeded) necessari al corretto funzionamento della rete.

Per questo motivo, solitamente si consente il traffico ICMP sia in ingresso, che in uscita, che in inoltro.

```bash
iptables -t filter -A INPUT   -p icmp -j ACCEPT
iptables -t filter -A OUTPUT  -p icmp -j ACCEPT
iptables -t filter -A FORWARD -p icmp -j ACCEPT
```
Spiegazione:

- **INPUT**: consente che l’host firewall possa ricevere richieste ICMP (es. venga “pingato”).

- **OUTPUT**: consente che il firewall possa generare richieste ICMP (es. fare ping a un altro host).

- **FORWARD**: permette che i pacchetti ICMP possano attraversare il firewall (utile se i client della LAN devono pingare host su Internet o viceversa).

***Verifica del funzionamento***
```bash
ping <IP_destinazione>
```

Se ricevi risposta, significa che le regole ICMP permettono correttamente la comunicazione.

### NAT
Il NAT (Network Address Translation) viene utilizzato per tradurre indirizzi IP (sorgente o destinazione) nei pacchetti che attraversano il firewall/router.

**La logica generale:**

- **Da Internet → Rete privata**

    Si utilizza **PREROUTING** → DNAT per tradurre l’IP di destinazione pubblico in un IP privato (es. port forwarding).

    Il **DNAT** (Destination NAT) permette di pubblicare un servizio interno rendendolo raggiungibile da Internet tramite l’IP pubblico del firewall.

    ```bash
    # Port forwarding SSH: host esterno 2.3.4.5 prova a fare SSH su 5.4.3.2 (IP pubblico firewall)
    # Il traffico viene inoltrato al server privato in DMZ 192.168.0.100
    iptables -t nat -A PREROUTING -p tcp --dport 22 -i eth2 -s 2.3.4.5 -d 5.4.3.2 -j DNAT --to-destination 192.168.0.100
    ```
    ***Verifica del funzionamento***
    ```bash
    ssh 5.4.3.2   # Da host esterno 2.3.4.5
    # Il firewall inoltra la connessione verso 192.168.0.100
    ```

- **Da Rete privata → Internet**

    Si utilizza **POSTROUTING** → SNAT o MASQUERADE per sostituire l’IP sorgente privato con l’IP pubblico del gateway.

    Il **MASQUERADE** è una forma speciale di SNAT usata quando l’IP pubblico è dinamico (tipico negli accessi domestici o tramite PPPoE).

    ```bash
    # Tutti i pacchetti provenienti dalla LAN 10.0.1.0/25 o DMZ 192.168.0.0/24,
    # quando escono su eth2 verso Internet, assumono come sorgente l’IP pubblico 5.4.3.2
    iptables -t nat -A POSTROUTING -o eth2 -s 10.0.1.0/25 -j MASQUERADE
    iptables -t nat -A POSTROUTING -o eth2 -s 192.168.0.0/24 -j MASQUERADE
    ```
    ***Verifica del funzionamento***
    ```bash
    tcpdump -i eth2
    # Controllare che i pacchetti in uscita abbiano come IP sorgente quello pubblico del firewall
    ```

### FTP

L’FTP utilizza due connessioni TCP:

- **Porta 21 (control connection):** usata dal client per inviare comandi al server.

- **Porta 20 (ftp-data) o porte dinamiche (>1023)**: usate per il trasferimento dati, a seconda della modalità.

Esistono due modalità operative:

- **Active mode**: il server apre la connessione dati da porta 20 verso una porta effimera del client.

- **Passive mode**: il server comunica al client una porta >1023 su cui aprire la connessione dati, ed è il client ad avviarla.

> Consentire connessioni *TCP* sulla porta 21 da Internet verso il server *FTP ftp.fake.com* e consentire le risposte
```bash
# Connessione control (porta 21)
iptables -t filter -A FORWARD -i eth2 -o eth1 -d 192.168.0.101 -p tcp --dport 21 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -t filter -A FORWARD -i eth1 -o eth2 -s 192.168.0.101 -p tcp --sport 21 -m state --state ESTABLISHED -j ACCEPT

```
> Per il trasferimento dati il server apre una nuova connessione TCP da porta 20 (ftp-data) verso una porta sul client
```bash
# Trasferimento dati (porta 20, active mode)
iptables -t filter -A FORWARD -p tcp --sport 20 -i eth1 -o eth2 -s 192.168.0.101 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -t filter -A FORWARD -p tcp --dport 20 -i eth2 -o eth1 -d 192.168.0.101 -m state --state ESTABLISHED -j ACCEPT
```

***Verifica del funzionamento***:
```bash
ftp 5.4.3.2    # Da host esterno
# Controllare che login e trasferimento dati funzionino correttamente
```


