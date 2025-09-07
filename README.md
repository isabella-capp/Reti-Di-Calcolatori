# Laboratorio di Reti di Calcolatori 

[![Repository](https://img.shields.io/badge/Repository-GitHub-blue)](https://github.com/isabella-capp/Reti-Di-Calcolatori)
[![Course](https://img.shields.io/badge/Course-Computer%20Networks%20Lab-green)](https://www.unimore.it)

Repository contenente le soluzioni e la documentazione del laboratorio del corso di **Reti di Calcolatori** tenuto dai professori **Ricardo Lancellotti** e **Mirko Marchetti** presso l'Università di Modena e Reggio Emilia.

## 📋 Contenuto del Repository

### 🔧 Marionnet - Simulazione di Reti
La cartella `Marionnet/` contiene 14 esercizi completi di configurazione e simulazione di reti usando **Marionnet**, un simulatore di reti virtuali basato su User Mode Linux.

#### Esercizi Principali:
- **Configurazione VLAN** e routing inter-VLAN
- **Configurazione DHCP** per l'assegnazione dinamica degli indirizzi IP
- **Routing statico e dinamico** tra sottoreti
- **Configurazione Firewall** con iptables
- **NAT e Port Forwarding**
- **Gestione di reti multi-VLAN** complesse
- **Simulazione di scenari enterprise** con DMZ e reti esterne

#### Struttura degli Esercizi Marionnet:
- `Exam_XXX/index.md` - Descrizione completa dell'esercizio e configurazioni
- `Exam_XXX/*.mar` - File di progetto Marionnet
- `img/` - Screenshot e diagrammi di rete
- `Documentation/` - Guide di riferimento per utilities, iptables e routing

### 🔌 Socket Programming
La cartella `Socket/` contiene esercizi pratici di programmazione socket in Python e C.

#### Caratteristiche:
- **Server/Client TCP** con gestione di connessioni multiple
- **Trasferimento file** via socket
- **Protocolli di comunicazione** personalizzati
- **Ambiente Docker** per testing e deployment
- **Implementazioni parallele** con fork() e threading

#### Struttura Socket Programming:
- `Docker_UNIX/` - Ambiente containerizzato per lo sviluppo
- `workspace/Exam_XXX/` - Soluzioni complete degli esercizi
- Server implementati in **Python** con supporto multi-client
- Client implementati in **Python** e **C**
- `Documentation/` - Guide per socket programming e gestione file

## 🚀 Come Utilizzare il Repository

### Prerequisiti Marionnet
- Avere accesso ai laboratori virtuali di UNIMORE
### Prerequisiti Socket Programming
```bash
# Utilizzo dell'ambiente Docker
cd Socket/Docker_UNIX
docker-compose up --build -d

# Esecuzione di un esercizio
cd workspace/Exam_XXX
python3 server.py 
python3 client.py <params>
```

## 📚 Argomenti Trattati

### Configurazione di Rete
- ✅ **VLAN Tagging** (802.1Q)
- ✅ **DHCP Server** configuration
- ✅ **Static IP** assignment
- ✅ **Routing Tables** e default gateway
- ✅ **Network Address Translation (NAT)**
- ✅ **Port Forwarding**

### Sicurezza e Firewall
- ✅ **iptables** configuration
- ✅ **Packet filtering** rules
- ✅ **DMZ** setup
- ✅ **Access Control Lists**
- ✅ **Traffic shaping**

### Programmazione Socket
- ✅ **TCP Socket** programming
- ✅ **Multi-client server** architecture
- ✅ **File transfer** protocols
- ✅ **Binary data** handling
- ✅ **JSON communication** protocols
- ✅ **Error handling** e connection management

## 🔗 Struttura delle Soluzioni

Ogni esercizio include:

### Per Marionnet:
1. **Schema di rete** con topologia completa
2. **Configurazione IP** dettagliata per ogni nodo
3. **Script di configurazione** bash automatizzati
4. **Configurazione VLAN** per switch
5. **Testing e verifica** della connettività
6. **Troubleshooting** e diagnostica

### Per Socket Programming:
1. **Specifiche** del protocollo di comunicazione
2. **Implementazione server** Python con gestione errori
3. **Implementazione client** Python/C
4. **Versione multi-client** con fork/threading
5. **Test di interoperabilità**
6. **Documentazione API**

## 🎯 Obiettivi Didattici

- Comprensione pratica dei **protocolli di rete**
- Configurazione avanzata di **infrastrutture di rete**
- Sviluppo di **applicazioni distribuite**
- Gestione della **sicurezza di rete**
- **Troubleshooting** e diagnostica di problemi di rete
- **Virtualizzazione** e containerizzazione per lo sviluppo

## 📖 Documentazione Aggiuntiva

### Guide di Riferimento:
- [`iptables.md`](Marionnet/Documentation/iptables.md) - Configurazione firewall completa
- [`routes.md`](Marionnet/Documentation/routes.md) - Routing e gestione tabelle di routing
- [`utilities.md`](Marionnet/Documentation/utilities.md) - Utilities di sistema e networking
- [`python_socket.md`](Socket/Documentation/python_socket.md) - Programmazione socket in Python
- [`python_files.md`](Socket/Documentation/python_files.md) - Gestione file in Python

## 👥 Crediti

**Docenti del Corso:**
- Prof. **Ricardo Lancellotti** - Università di Modena e Reggio Emilia
- Prof. **Mirko Marchetti** - Università di Modena e Reggio Emilia

**Repository mantenuto da:** [Isabella Cappellino](https://github.com/isabella-capp)

---

*Questo repository è stato creato a scopo educativo per il corso di Reti di Calcolatori presso l'Università di Modena e Reggio Emilia.*
