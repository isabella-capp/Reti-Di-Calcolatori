# Laboratorio

Si chiede di realizzare una rete come quella in figura, in cui GW fornisce connettività a una sottorete interna
 (`192.168.10.0/24`) con tre host (H1, H2, H3).
 GW deve:
 1. Fornire i parametri di configurazione per (H1, H2, H3) mediante protocollo DHCP. Il pool di indirizzi da attribuire è esattamente di tre elementi: da `192.168.10.1` a `192.168.10.3`
 2. Fornire connettività con il nodo Ext per la sottorete interna
 3. Implementare un servizio di masquerading (SNAT) in modo che i nodi H1, H2, H3 possano comunicare con Ext

![image.png](/Marionnet/img/image_7.png)

**Elementi di valutazione:**
 1. Il sistema DHCP fornisce parametri corretti di configurazione della rete per i tre nodi H1, H2, H3
 2. I nodi GW e Ext sono configurati correttamente
 3. il servizio di SNAT è configurato correttamente
 4. I nodi H1, H2, H3 comunicano correttamente con Ext (verificare con ping)
 5. Il traffic shaping funziona (verificare con nc)

 ## Schema di rete

 ### H1, H2 e H3

   - **Indirizzo IP**:  `192.168.10.1` a `192.168.10.3`
   - **Netmask**: 255.255.255.0

### GW
- **Interfaccia**: eth0
   - **Indirizzo IP**: 192.168.10.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth1
   - **Indirizzo IP**: 1.1.1.1
   - **Netmask**: 255.255.255.255

### EXT
- **Interfaccia**: eth0
   - **Indirizzo IP**: 2.2.2.2
   - **Netmask**: 255.255.255.255