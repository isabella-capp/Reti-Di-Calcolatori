Si chiede di realizzare una rete come quella in figura in due versioni diverse, La prima versione (NOVLAN)
usando solo schede di rete e switch senza supporto di VLAN. La seconda versione (VLAN), si basa su VLAN,
usando un solo switch (che unisce SW1 e SW2) e usando un'unica scheda di rete su GW che unisce eth1 e
eth2. Si chiede inoltre di implementare SNAT per ogni nodo e DNAT per un server che si trova sulla porta
80 di Srv1 che deve apparire sulla porta 80 di GW e per un server sulla porta 80 di Srv2 che deve apparire
sulla porta 8080 di GW.

**Elementi di valutazione**
1. [NOVLAN] C'è comunicazione all'interno di ogni sottorete (Srv2 con H2, Srv1 con H1) •
2. [NOVLAN] C'è comunicazione di ogni nodo con GW (incluso Ext) •
3. [NOVLAN] C'è comunicazione tra elementi di sottoreti diverse (Srv2 con H1, Srv1 con H2).
4. [NOVLAN] II SNAT su GW consente a un nodo in una sottorete di contattare Ext.
5. [NOVLAN] II DNAT su GW consente a Ext di contattare i due server
6. [VLAN] C'è comunicazione tra elementi di sottoreti diverse (Srv2 con H1, Srv1 con H2)
7. [VLAN] II dominio di collisione è separato

## Schema di rete

### H1

- **Interfaccia**: eth0
    - **IP**: 192.168.1.2
    - **Netmask**: 255.255.255.0

### H2

- **Interfaccia**: eth0
    - **IP**: 192.168.2.2
    - **Netmask**: 255.255.255.0

### Srv1

- **Interfaccia**: eth0
    - **IP**: 192.168.1.1
    - **Netmask**: 255.255.255.0

### Srv2

- **Interfaccia**: eth0
    - **IP**: 192.168.2.1
    - **Netmask**: 255.255.255.0

### GW

- **Interfaccia**: eth0
    - **IP**: 1.1.1.1
    - **Netmask**: 255.255.255.255
- **Interfaccia**: eth1
    - **IP**: 192.168.2.254
    - **Netmask**: 255.255.255.0
- **Interfaccia**: eth2
    - **IP**: 192.168.1.254
    - **Netmask**: 255.255.255.0

### EXT

- **Interfaccia**: eth0
    - **IP**: 2.2.2.2
    - **Netmask**: 255.255.255.255