# LAB

Si chiede di realizzare una rete come quella in figura in due versioni diverse:
- La **prima versione (NOVLAN)** usando solo schede di rete e switch senza supporto di VLAN. 
- La **seconda versione (VLAN)**, si basa su VLAN, usando un solo switch (che unisce SW1 e SW2) e usando un'unica scheda di rete su GW che unisce eth1 e eth2. 

Si chiede inoltre di implementare SNAT per ogni nodo e DNAT per:
- un server che si trova sulla porta 80 di Srv1 che deve apparire sulla porta 80 di GW 
- un server sulla porta 80 di Srv2 che deve apparire sulla porta 8080 di GW.

![image.png](/Marionnet/img/image_4.png)

**Elementi di valutazione**
1. [NOVLAN] C'è comunicazione all'interno di ogni sottorete (Srv2 con H2, Srv1 con H1) 
2. [NOVLAN] C'è comunicazione di ogni nodo con GW (incluso Ext) 
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


### H1

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
    address 192.168.1.2
    netmask 255.255.255.0
    gateway 192.168.1.254

"

echo "$interfaces" >> /etc/network/interfaces
echo "H1 network configuration added."
```

### H2

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
    address 192.168.2.2
    netmask 255.255.255.0
    gateway 192.168.2.254
"

echo "$interfaces" >> /etc/network/interfaces
echo "H2 network configuration added."
```

### Srv1

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 192.168.1.1
        netmask 255.255.255.0
        gateway 192.168.1.254      
"

echo "$interfaces" >> /etc/network/interfaces
echo "Srv1 network configuration added."
```

### Srv2

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 192.168.2.1
        netmask 255.255.255.0
        gateway 192.168.2.254      
"

echo "$interfaces" >> /etc/network/interfaces
echo "Srv2 network configuration added."
```

### GW

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 1.1.1.1
        netmask 255.255.255.255

auto eth1
iface eth1 inet static
        address 192.168.2.254
        netmask 255.255.255.0

auto eth2
iface eth2 inet static
        address 192.168.1.254
        netmask 255.255.255.0

post-up ip route add 2.2.2.2 dev eth0
"

echo "$interfaces" >> /etc/network/interfaces
echo "GW network configuration added."

echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
echo "Ip configurato correttamente."

sysctl -p /etc/sysctl.conf
if [ $? -eq 0 ]; then
    echo "sysctl configuration reloaded successfully."
else
    echo "Failed to reload sysctl configuration."
    exit 1
fi

```

### EXT

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 2.2.2.2
        netmask 255.255.255.255
        gateway 1.1.1.1
"

echo "$interfaces" >> /etc/network/interfaces
echo "EXT network configuration added."
```



```bash
#!/bin/bash

#---------------------------------------------
# SNAT
#---------------------------------------------
NET_ID_LAN_1="192.168.1.0/24"
NET_ID_LAN_2="192.168.2.0/24"
iptables -t nat -A POSTROUTING -o $EXT_IF -s $NET_ID_LAN_1  -j MASQUERADE
iptables -t nat -A POSTROUTING -o $EXT_IF -s $NET_ID_LAN_1  -j MASQUERADE

#---------------------------------------------
# DNAT
#---------------------------------------------
IP_SRV_2= 192.168.2.1
IP_SRV_1= 192.168.1.1

iptables -t nat -A PREROUTING -p tcp --dport 8080 -i $EXT_IF -j DNAT --to-destination $IP_SRV_2:80
iptables -t nat -A PREROUTING -p tcp --dport 80 -i $EXT_IF -j DNAT --to-destination $IP_SRV_1:80
```