# Laboratorio

Si chiede di realizzare una rete come quella in figura, in cui GW fornisce connettività a tutti gli host all'interno
di un'unica rete `192.168.1.0/25`.

**La rete LAN contiene:**
- H1 (indirizzo IP dinamico fornito dal server DHCP)
- H2 (indirizzo IP dinamico fornito dal server DHCP)
- SRV (indirizzo IP statico fornito dal server DHCP, corrispondente al primo indirizzo valido della
sottorete)
- GW (indirizzo IP statico corrispondente al più alto indirizzo valido della sottorete)

**GW ha due interfacce di rete:**
- eth0, connessa a sw1.
- eth1, connessa a sw2, con indirizzo IP `9.8.7.6/32`

La rete comprende anche un esterno (EXT) con indirizzo IP `2.1.3.4/32`, connesso a sw2.

GW deve:
- eseguire il server DHCP e DNS per la configurazione degli host all'interno della sottorete.
- essere default gateway per la rete LAN
- effettuare il routing in modo che la connettività fra tutti gli host della rete sia garantita
- implementare le opportune regole di NAT e filtro di pacchetto necessarie per il corretto funzionamento.

![image.png](/Marionnet/img/image_13.png)

Politiche di filtraggio sul firewall:
- Utilizzare una policy di negazione implicita per tutti i pacchetti in transito, ingresso e uscita da GW
- Consentire flussi di comunicazione UDP per il corretto funzionamento del protocollo DHCP
- Consentire flussi di comunicazione UDP per il corretto funzionamento del protocollo DNS
- Consentire connessioni SSH generate dalla macchina H1 (usare l'ip ottenuto dal DHCP) verso GW
- Consentire alle macchine della rete LAN di contattare un server Web in esecuzione su EXT
- Consentire a EXT di contattare un server Web in esecuzione su SRV utilizzando l'ip pubblico associato all'interfaccia eth1 di GW
- Consentire a EXT di contattare un server SSH in esecuzione su H1 (usare l'ip ottenuto dal DHCP) utilizzando l'indirizzo IP pubblico associato all'interfaccia eth1 di GW
- Testare l'invio di file da EXT a SRV con nc

**Elementi di valutazione:**
1. I nodi della rete sono configurati correttamente
2. Le regole di routing sono corrette
3. GW blocca tutto il traffico non espressamente consentito
4. I protocolli DHCP e DNS sono correttamente configurati e forniscono i parametri adeguati
5. H1 riesce a contattare il server SSH in esecuzione su GW
6. I nodi comunichino correttamente con un server Web sul nodo EXT (verificare con nc)
7. EXT può accedere al servizio Web erogato da SRV (verificare con nc)
8. EXT riesce a raggiungere il server SSH su H1 contattando GW (ssh root@9.8.7.6)


 ## Schema di rete

### H1

   - **NetID**: 192.168.1.0
   - **Interfaccia**: eth0
        - **Indirizzo IP**: ---
        - **Netmask**: 255.255.255.255

### H2

   - **NetID**: 192.168.1.0
   - **Interfaccia**: eth0
        - **Indirizzo IP**: ---
        - **Netmask**: 255.255.255.255

### Srv

   - **NetID**: 192.168.1.0
   - **Interfaccia**: eth0
        - **Indirizzo IP**: ---
        - **Netmask**: 255.255.255.255

### GW
- **Interfaccia**: eth0.10
   - **Indirizzo IP**: 10.0.10.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth0.20
   - **Indirizzo IP**: 10.0.20.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth1
   - **Indirizzo IP**: 9.8.7.6
   - **Netmask**: 255.255.255.255

### EXT
- **Interfaccia**: eth0
   - **Indirizzo IP**: 2.1.3.4
   - **Netmask**: 255.255.255.255