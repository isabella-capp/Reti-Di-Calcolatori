# Laboratorio

Si chiede di realizzare una rete come quella in figura, in cui GW fornisce connettività a due sottoreti: 
- `192.168.20.0/24` con due host (H1, H2) 
- `192.168.10.0/24` con un host (Srv).

**GW deve:**
 1. Connetere gli host usando le VLAN come indicato in figura.
 2. Fornire i parametri di configurazione per (H1, H2) mediante protocollo DHCP. 
3. **Srv** deve essere configurato in modo statico (IP `192.168.10.1/24`)
 4. Fornire connettività tra i nodi
 5. Configurare SNAT in modo che i nodi H1, H2, Srv possano comunicare con Ext
 6. Fornire un servizio di DNAT per consentire a Ext di contattare un server Web sul nodo Srv (il 
numero di porta è fornito dal servizio)

![image.png](/Marionnet/img/image_8.png)

**Elementi di valutazione:**
 1. Il sistema DHCP fornisce parametri corretti di configurazione della rete per i nodi H1, H2
 2. Gli altri nodi sono configurati correttamente
 3. Le VLAN sono configurate in modo adeguato (verificare con arping)
 4. il servizio di SNAT è configurato correttamente
 5. I nodi H1, H2, Srv comunicano correttamente con Ext (verificare con ping)
 6. Ext può accedere al servizio Web erogato da Srv mediante DNAT (verificare con nc)

  ## Schema di rete

 ### H1 e H2

   - **NetID**: 192.168.20.0
   - **VLANID**: 20
   - **Interfaccia**: eth0
        - **Indirizzo IP**: DHCP
        - **Netmask**: 255.255.255.0

### H3
   - **NetID**: 192.168.10.0
   - **VLANID**: 10
   - **Interfaccia**: eth0
        - **Indirizzo IP**: 192.168.10.1
        - **Netmask**: 255.255.255.0

### GW
- **Interfaccia**: eth0.10
   - **Indirizzo IP**: 192.168.10.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth0.20
   - **Indirizzo IP**: 192.168.20.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth1
   - **Indirizzo IP**: 3.3.3.3
   - **Netmask**: 255.255.255.255

### EXT
- **Interfaccia**: eth0
   - **Indirizzo IP**: 5.5.5.5
   - **Netmask**: 255.255.255.255