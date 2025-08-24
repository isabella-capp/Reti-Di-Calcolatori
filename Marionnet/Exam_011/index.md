# Laboratorio

 Si chiede di realizzare una rete come quella in figura, in cui GW fornisce connettività a due sottoreti:
- 10.0.10.0/24 con Srv1 (MAC address 02:04:06:11:22:33)
- 10.0.20.0/24 con Srv2 (MAC address 02:04:06:11:22:44)

 GW deve fornire connettività a entrambe le reti avendo a disposizione una sola scheda di rete collegato allo 
switch SW (usare opportunamente le VLAN e le schede di rete virtuali). 

Inoltre GW deve ospitare un server DHCP che deve configurare i parametri di rete di entrambi i server.

 Si chiede inoltre di implementare sul nodo GW:
 - SNAT per ogni nodo delle reti considerate
 - DNAT per un server web sulla porta 80 di Srv1 che deve apparire sulla porta 80 di GW
 - DNAT per un server web sulla porta 80 di Srv2 che deve apparire sulla porta 8080 di GW

![image.png](/Marionnet/img/image_11.png)

  **Elementi di valutazione:**
 1. Il server DHCP è configurato correttamente (bonus se il server parte automaticamente)
 2. C’è comunicazione di ogni nodo con GW (incluso Ext – verificare con ping) ma il dominio di 
collisione è separato (verificare con arping e tcpdump)
 3. C’è comunicazione tra elementi di sottoreti diverse (Srv2 con Srv –  verificare con ping)
 4. Il SNAT su GW consente a ciascun nodo in una sottorete di contattare Ext  (verificare con ping)
 5. Il DNAT su GW consente a Ext di contattare Srv1 e Srv2 (verificare con nc)

 ## Schema di rete

### Srv1

   - **NetID**: 10.0.10.0
   - **VLANID**: 10
   - **Interfaccia**: eth0
        - **Indirizzo IP**: 10.0.10.1
        - **Netmask**: 255.255.255.0

### Srv2

   - **NetID**: 10.0.20.0
   - **VLANID**: 20
   - **Interfaccia**: eth0
        - **Indirizzo IP**: 10.0.20.1
        - **Netmask**: 255.255.255.0

### GW
- **Interfaccia**: eth0.10
   - **Indirizzo IP**: 10.0.10.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth0.20
   - **Indirizzo IP**: 10.0.20.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth1
   - **Indirizzo IP**: 1.1.1.1
   - **Netmask**: 255.255.255.255

### EXT
- **Interfaccia**: eth0
   - **Indirizzo IP**: 2.2.2.2
   - **Netmask**: 255.255.255.255