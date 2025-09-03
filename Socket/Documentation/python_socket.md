# 📘 Documentazione funzioni principali della libreria `socket`

La libreria `socket` di Python fornisce un’interfaccia per la comunicazione tra processi via rete (TCP/IP, UDP, ecc.) e per la manipolazione di indirizzi, host e servizi.
Di seguito sono riportate le funzioni utili per la risoluzione dei nomi, la conversione di indirizzi e altre utilità di basso livello.


## Funzioni di risoluzione dei nomi e host

- ### `socket.getfqdn([name])`

    Restituisce il **Fully Qualified Domain Name (FQDN)** per un host.

    * Se `name` non è specificato, viene usato l’hostname locale.
    * Se `name` è già un FQDN, viene restituito tale valore.

    ```python
    import socket

    print("FQDN locale:", socket.getfqdn())  
    print("FQDN per www.google.com:", socket.getfqdn("www.google.com"))

    ```

    ```bash
    FQDN locale: mypc.localdomain
    FQDN per www.google.com: mil04s52-in-f4.1e100.net
    ```

- ### `socket.gethostbyname(hostname)`

    Restituisce l’indirizzo IPv4 corrispondente a un hostname.

    * `hostname`: può essere un nome DNS o `"localhost"`.
    * Restituisce una stringa con l’IP (es. `"93.184.216.34"`).

    ```python
    import socket

    ip = socket.gethostbyname("www.example.com")
    print("IP di www.example.com:", ip)
    ```

    ```bash
    IP di www.example.com: 93.184.216.34
    ```

- ### `socket.gethostbyname_ex(hostname)`

    Restituisce una tupla:

    ```
    (canonical_name, alias_list, ip_address_list)
    ```

    * `canonical_name`: nome canonico dell’host.
    * `alias_list`: lista di alias.
    * `ip_address_list`: lista di indirizzi IPv4.

    ```python
    import socket

    info = socket.gethostbyname_ex("www.google.com")
    print("Nome canonico:", info[0])
    print("Alias:", info[1])
    print("Indirizzi IP:", info[2])
    ```
    ```
    Nome canonico: mil04s52-in-f14.1e100.net
    Alias: []
    Indirizzi IP: ['142.250.186.196', '142.250.186.228']
    ```


- ### `socket.gethostname()`

    Restituisce il **nome dell’host locale** (il nome configurato sul sistema).

    ```python
    import socket

    print("Hostname locale:", socket.gethostname())
    ```

-   ### `socket.gethostbyaddr(ip_address)`

    Restituisce una tupla:

    ```
    (hostname, alias_list, ip_address_list)
    ```

    Esegue il **reverse lookup**: da un indirizzo IP restituisce il nome dell’host.

    ```python
    import socket

    info = socket.gethostbyaddr("8.8.8.8")
    print("Nome host:", info[0])
    print("Alias:", info[1])
    print("Indirizzi:", info[2])
    ```
    ```python
    Nome host: dns.google
    Alias: []
    Indirizzi: ['8.8.8.8']

    ```

- ### `socket.getnameinfo(sockaddr, flags)`

    Restituisce una tupla:

    ```
    (hostname, service)
    ```

    * `sockaddr`: una coppia `(indirizzo, porta)`.
    * `flags`: permette di specificare opzioni (es. `NI_NUMERICHOST` per avere solo l’indirizzo numerico).
    
    ```python
    import socket

    # Reverse lookup: IP + porta → nome host + servizio
    print(socket.getnameinfo(("8.8.8.8", 53), 0))

    # Con flag NI_NUMERICHOST → forzare formato numerico
    print(socket.getnameinfo(("8.8.8.8", 53), socket.NI_NUMERICHOST))
    ```
    ```python
    ('dns.google', 'domain')
    ('8.8.8.8', 'domain')
    ```


## Servizi e protocolli

- ### `socket.getprotobyname(protocolname)`

    Restituisce il **numero identificativo** di un protocollo (es. `6` per TCP, `17` per UDP).

    ```python
    import socket

    tcp_proto = socket.getprotobyname("tcp")
    udp_proto = socket.getprotobyname("udp")

    print("Numero protocollo TCP:", tcp_proto)
    print("Numero protocollo UDP:", udp_proto)
    ```

    ```python
    Numero protocollo TCP: 6
    Numero protocollo UDP: 17
    ```

- ### `socket.getservbyname(servicename[, protocolname])`

    Restituisce il **numero di porta** associato a un servizio.
    - Se non si specifica `protocolname`, di solito viene usato tcp.
    - Se si specifica, il risultato può differire (es. `http` su `tcp` è `80`, ma alcuni servizi hanno porte diverse per udp).

    ```python
    import socket

    http_port = socket.getservbyname("http")            # di default TCP
    dns_port_udp = socket.getservbyname("domain", "udp")
    dns_port_tcp = socket.getservbyname("domain", "tcp")

    print("Porta HTTP (TCP):", http_port)
    print("Porta DNS (UDP):", dns_port_udp)
    print("Porta DNS (TCP):", dns_port_tcp)
    ```
    ```python
    Porta HTTP (TCP): 80
    Porta DNS (UDP): 53
    Porta DNS (TCP): 53
    ```

- ### `socket.getservbyport(port[, protocolname])`

    Restituisce il **nome del servizio** associato a una porta.
    - Se non si specifica `protocolname`, di solito viene usato tcp.
    - Se si specifica deve corrispondere(es. `53` → `"domain"` sia per TCP che per UDP)

    ```python
    import socket

    service_22 = socket.getservbyport(22)
    service_80 = socket.getservbyport(80)
    service_53_udp = socket.getservbyport(53, "udp")

    print("Servizio su porta 22:", service_22)
    print("Servizio su porta 80:", service_80)
    print("Servizio su porta 53 UDP:", service_53_udp)
    ```
    ```python
    Servizio su porta 22: ssh
    Servizio su porta 80: http
    Servizio su porta 53 UDP: domain
    ```

## Conversioni host/network byte order

Queste funzioni convertono numeri interi tra:
* **Host Byte Order**: l’ordine dei byte usato dalla macchina su cui gira il programma.
  * Architetture *little-endian* (es. x86, ARM) salvano i byte meno significativi per primi.
  * Architetture *big-endian* (alcuni processori di rete) salvano i byte più significativi per primi.

* **Network Byte Order**: per convenzione, **big-endian** (MSB → Most Significant Byte per primo).
  Tutti i protocolli TCP/IP usano questo formato.

- ### `socket.htonl(x)`→ *Host TO Network Long*
    
    Converte un intero a 32 bit (`long`) da **host byte order** a **network byte order**.

    ```python
    import socket
    import sys

    num = 0x12345678  # 32 bit

    print("Host order:", hex(num))
    print("Network order:", hex(socket.htonl(num)))
    print("Endianness della macchina:", sys.byteorder)
    ```

    Output tipico su architettura **little-endian**:

    ```
    Host order: 0x12345678
    Network order: 0x78563412
    Endianness della macchina: little
    ```

- ### `socket.htons(x)` → *Host TO Network Short*

    Converte un intero a 16 bit (`short`) da **host byte order** a network byte order.
    Usato ad esempio per le **porte** (che sono numeri a 16 bit).

    **Esempio:**

    ```python
    import socket

    port = 8080  # porta in host byte order
    net_port = socket.htons(port)

    print("Porta originale:", port)
    print("Porta in network order:", net_port)
    ```

    Output tipico:

    ```
    Porta originale: 8080
    Porta in network order: 36895
    ```

    >(Il numero appare diverso perché viene letto con l’ordine dei byte invertito).

- ### `socket.ntohl(x)` → *Network TO Host Long*

    Inverso di `htonl`. Converte un intero a 32 bit da **network** a **host byte order**.

    **Esempio:**

    ```python
    import socket

    net_num = socket.htonl(0x12345678)  # prima lo porto in network order
    host_num = socket.ntohl(net_num)    # ora lo riporto in host order

    print("Network order:", hex(net_num))
    print("Host order:", hex(host_num))
    ```

    Output tipico:

    ```
    Network order: 0x78563412
    Host order: 0x12345678
    ```

- ### `socket.ntohs(x)` → *Network TO Host Short*

    Inverso di `htons`. Converte un intero a 16 bit da network a host byte order.

    **Esempio:**

    ```python
    import socket

    net_port = socket.htons(80)     # HTTP in network order
    host_port = socket.ntohs(net_port)

    print("Porta in network order:", net_port)
    print("Porta in host order:", host_port)
    ```

    **Output tipico:**

    ```
    Porta in network order: 20480
    Porta in host order: 80
    ```

## Conversioni indirizzi IP

Queste funzioni servono a convertire indirizzi IP tra formato **testuale leggibile** (`"192.168.1.1"`) e formato **binario packed** usato nelle strutture di rete.

- ### `socket.inet_aton(ip_string)`

    Converte un indirizzo IPv4 in **forma testuale** (`"192.168.1.1"`) in formato **binario compatto**.

    **Esempio:**

    ```python
    import socket

    ip_str = "192.168.1.1"
    packed_ip = socket.inet_aton(ip_str)

    print("IP stringa:", ip_str)
    print("IP packed (binario):", packed_ip)
    print("IP packed (esadecimale):", packed_ip.hex())
    ```

    Output tipico:

    ```
    IP stringa: 192.168.1.1
    IP packed (binario): b'\xc0\xa8\x01\x01'
    IP packed (esadecimale): c0a80101
    ```

- ### `socket.inet_ntoa(packed_ip)`

    Inverso di `inet_aton()`.
    Converte un indirizzo IPv4 **packed (binario)** in **stringa leggibile**.

    **Esempio:**

    ```python
    import socket

    packed_ip = b'\xC0\xA8\x01\x01'
    ip_str = socket.inet_ntoa(packed_ip)

    print("IP packed:", packed_ip)
    print("IP stringa:", ip_str)
    ```

    📌 Output tipico:

    ```
    IP packed: b'\xc0\xa8\x01\x01'
    IP stringa: 192.168.1.1
    ```
- ### `socket.inet_pton(address_family, ip_string)`

    Converte un indirizzo IP (IPv4 o IPv6) in **forma binaria packed**.

    * `socket.AF_INET` → IPv4
    * `socket.AF_INET6` → IPv6

    **Esempio:**

    ```python
    import socket

    ipv4_str = "8.8.8.8"
    ipv6_str = "2001:4860:4860::8888"

    packed_ipv4 = socket.inet_pton(socket.AF_INET, ipv4_str)
    packed_ipv6 = socket.inet_pton(socket.AF_INET6, ipv6_str)

    print("IPv4 stringa:", ipv4_str, "→ packed:", packed_ipv4.hex())
    print("IPv6 stringa:", ipv6_str, "→ packed:", packed_ipv6.hex())
    ```

    📌 Output tipico:

    ```
    IPv4 stringa: 8.8.8.8 → packed: 08080808
    IPv6 stringa: 2001:4860:4860::8888 → packed: 20014860486000000000000000008888
    ```

- ### `socket.inet_ntop(address_family, packed_ip)`

    Inverso di `inet_pton()`.
    Converte da **forma binaria** a **stringa leggibile**.

    **Esempio:**

    ```python
    import socket

    packed_ipv4 = b"\x08\x08\x08\x08"
    packed_ipv6 = bytes.fromhex("20014860486000000000000000008888")

    ip4_str = socket.inet_ntop(socket.AF_INET, packed_ipv4)
    ip6_str = socket.inet_ntop(socket.AF_INET6, packed_ipv6)

    print("IPv4 packed:", packed_ipv4, "→ stringa:", ip4_str)
    print("IPv6 packed:", packed_ipv6.hex(), "→ stringa:", ip6_str)
    ```

    📌 Output tipico:

    ```
    IPv4 packed: b'\x08\x08\x08\x08' → stringa: 8.8.8.8
    IPv6 packed: 20014860486000000000000000008888 → stringa: 2001:4860:4860::8888
    ```

## Messaggi di controllo (Ancillary Data)

Quando si usano socket di basso livello (es. UNIX domain sockets), può essere necessario inviare dati “extra” oltre al messaggio, detti **ancillary data** (ad esempio i file descriptor).
- ### `socket.CMSG_LEN(length)`

    Restituisce la **lunghezza corretta** di un messaggio di controllo che trasporta `length` byte di dati.
    Serve per calcolare la dimensione effettiva di un ancillary message.

    **Esempio:**

    ```python
    import socket

    print("CMSG_LEN(4):", socket.CMSG_LEN(4))
    print("CMSG_LEN(100):", socket.CMSG_LEN(100))
    ```

    📌 Output tipico:

    ```
    CMSG_LEN(4): 20
    CMSG_LEN(100): 116
    ```

- ### 🔹 `socket.CMSG_SPACE(length)`

    Restituisce lo **spazio totale richiesto**, inclusi padding e allineamento, per contenere un messaggio di controllo con `length` byte di dati.

    **Esempio:**

    ```python
    import socket

    print("CMSG_SPACE(4):", socket.CMSG_SPACE(4))
    print("CMSG_SPACE(100):", socket.CMSG_SPACE(100))
    ```

    📌 Output tipico:

    ```
    CMSG_SPACE(4): 24
    CMSG_SPACE(100): 120
    ```

## Timeout e configurazione host

- ### `socket.getdefaulttimeout()`

    Restituisce il valore di **timeout predefinito** (in secondi) per tutte le nuove socket.
    Se non è impostato, ritorna `None`.

    **Esempio:**

    ```python
    import socket

    print("Timeout predefinito:", socket.getdefaulttimeout())
    ```

    📌 Output tipico:

    ```
    Timeout predefinito: None
    ```


- ### `socket.setdefaulttimeout(timeout)`

    Imposta il **timeout predefinito** per tutte le nuove socket.

    * `timeout` in secondi (float o int).
    * `None` → rimuove il timeout.

    **Esempio:**

    ```python
    import socket

    socket.setdefaulttimeout(5)
    print("Timeout predefinito impostato a:", socket.getdefaulttimeout())

    socket.setdefaulttimeout(None)
    print("Timeout rimosso:", socket.getdefaulttimeout())
    ```

    📌 Output tipico:

    ```
    Timeout predefinito impostato a: 5.0
    Timeout rimosso: None
    ```

- ### `socket.sethostname(name)`

    Imposta il nome dell’host locale.
    >⚠️ **Richiede privilegi di amministratore/root** e funziona solo su sistemi Unix-like.

    **Esempio (da usare con cautela):**

    ```python
    import socket
    import os

    if os.geteuid() == 0:  # controlla se sei root
        socket.sethostname("nuovo-host")
        print("Hostname cambiato!")
    else:
        print("Serve essere root per cambiare hostname.")
    ```

    📌 Output:

    ```
    Serve essere root per cambiare hostname.
    ```


## Interfacce di rete

- ### `socket.if_nameindex()`

    Restituisce una lista di tuple `(index, name)` delle interfacce di rete disponibili.

    **Esempio:**

    ```python
    import socket

    interfaces = socket.if_nameindex()
    print("Interfacce disponibili:", interfaces)
    ```

    📌 Output tipico:

    ```
    Interfacce disponibili: [(1, 'lo'), (2, 'eth0'), (3, 'wlan0')]
    ```

- ### `socket.if_nametoindex(if_name)`

    Restituisce l’**indice numerico** dell’interfaccia dato il suo nome.

    **Esempio:**

    ```python
    import socket

    idx = socket.if_nametoindex("lo")
    print("Indice interfaccia 'lo':", idx)
    ```

    📌 Output tipico:

    ```
    Indice interfaccia 'lo': 1
    ```

- ### `socket.if_indextoname(if_index)`

    Restituisce il **nome** dell’interfaccia dato il suo indice.

    **Esempio:**

    ```python
    import socket

    name = socket.if_indextoname(1)
    print("Interfaccia con indice 1:", name)
    ```

    📌 Output tipico:

    ```
    Interfaccia con indice 1: lo
    ```



## Passaggio di file descriptor

Queste funzioni sono usate solo su **Unix domain sockets** (`AF_UNIX`) e permettono a un processo di **condividere file descriptor** con un altro processo.


- ### `socket.send_fds(sock, buffers, fds[, flags[, address]])`

    Invia **dati normali** (`buffers`) e **file descriptor** (`fds`) tramite un socket Unix.

    **Esempio (semplificato):**

    ```python
    import socket
    import os

    # Crea una coppia di socket collegati
    parent_sock, child_sock = socket.socketpair()

    # Invia un FD (stdout = 1) dal padre al figlio
    socket.send_fds(parent_sock, [b"ciao"], [1])

    # Riceve nel figlio
    data, fds, flags, addr = socket.recv_fds(child_sock, 1024, 1)
    print("Dati ricevuti:", data)
    print("File descriptor ricevuti:", fds)
    ```

    📌 Output tipico:

    ```
    Dati ricevuti: [b'ciao']
    File descriptor ricevuti: [1]
    ```



- ### `socket.recv_fds(sock, bufsize, maxfds[, flags])`

    Riceve dati e file descriptor da un socket Unix.
    Restituisce una tupla:

    ```
    (data, fds, msg_flags, address)
    ```

    👉 Nell’esempio sopra, il processo figlio riceveva `[b'ciao']` e il file descriptor `1` (stdout).

