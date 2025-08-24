# Laboratorio

Si chiede di realizzare una rete come quella in figura, in cui GW fornisce connettività a una sottorete interna 
(`192.168.10.0/24`) con tre host (H1, H2, H3).
 GW deve:
 1. Fornire i parametri di configurazione per (H1, H2, H3) mediante protocollo DHCP.
     - Per H1 e H2 l’indirizzo deve essere preso dal pool: `192.168.10.10` a  `192.168.10.20`
     - Per H3 bisogna l’indirizzo deve essere `192.168.10.30`, assegnato sulla base del mac address 
`02:04:06:11:22:33`
 2. Fornire connettività con il nodo Ext per la sottorete interna
 3. Implementare un servizio di masquerading (SNAT) in modo che i nodi H1, H2, H3 possano comunicare con 
Ext
 4. Realizzare un servizio di DNAT in modo che Ext possa contattare un server su H3 alla porta 80

![image.png](/Marionnet/img/image_6.png)

**Elementi di valutazione:**
 1. Il sistema DHCP fornisce parametri corretti di configurazione della rete per i nodi H1, H2
 2. Il sistema DHCP fornisce parametri corretti di configurazione della rete per il nodo H3
 3. I nodi GW e Ext sono configurati correttamente
 4. il servizio di SNAT è configurato correttamente
 5. I nodi H1, H2, H3 comunicano correttamente con Ext (verificare con ping)
 6. Il DNAT funziona correttamente (verificare con nc)

  ## Schema di rete

 ### H1 e H2

   - **Indirizzo IP**: `192.168.10.10` a  `192.168.10.20`
   - **Netmask**: 255.255.255.0

### H3

   - **Indirizzo IP**: `192.168.10.30`
   - **Netmask**: 255.255.255.0
   - **Mac Address**: 02:04:06:11:22:33

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