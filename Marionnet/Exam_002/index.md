# Laboratorio

Si chiede di realizzare una rete come quella in figura, in cui GW fornisce connettività a due sottoreti: 
`192.168.10.0/24` con due host (H1, H2) e `192.168.20.0/24` con due host (H3, H4). Si chiede di:
 1. Connettere gli host usando le VLAN come indicato in figura (bisogna garantire la connettività tra le 
sottoreti).
 2. Garantire scambio dati tra le due sottoreti passando per GW

**Elementi di valutazione:**
 1. Connettività tra i nodi della rete `192.168.10.0/24` (verificare con ping e arping)
 2. Connettività tra i nodi della rete `192.168.20.0/24` (verificare con ping e arping)
 3. Isolamento tra sottoreti differenti (verificare con arping)
 4. Corretta configurazione delle VLAN (configurazione su switch)
 5. Comunicazione tra le due sottoreti passando per GW (verificare con ping)

### LAN 10

**NetID** `192.168.10.0/24`
**Netmask** `255.255.255.0`

- **H1** 
    - interfaccia: `eth0`
    - IP: `192.168.10.1/24`
- **H2**
    - interfaccia: `eth0`
    - IP: `192.168.10.2/24`

### LAN 20

**NetID** `192.168.20.0/24`
**Netmask** `255.255.255.0`

- **H3**
    - interfaccia: `eth0`
    - IP: `192.168.20.1/24`
- **H4**
    - interfaccia: `eth0`
    - IP: `192.168.20.2/24`

### GW

    eth0.10 → 192.168.10.254
    eth0.20 → 192.168.20.254

## Configurazione VLAN

Configurazione per lo Switch:

```bash
vlan/create 10
vlan/create 20

port/setvlan 1 10
port/setvlan 2 10
port/setvlan 3 20
port/setvlan 4 20

vlan/addport 10 5
vlan/addport 20 5

```

## Configurazione IP

### H1

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 192.168.10.1
        netmask 255.255.255.0
        gateway 192.168.10.254
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
        address 192.168.10.2
        netmask 255.255.255.0
        gateway 192.168.10.254
"

echo "$interfaces" >> /etc/network/interfaces
echo "H2 network configuration added."
```

### H3

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 192.168.20.1
        netmask 255.255.255.0
        gateway 192.168.20.254
"

echo "$interfaces" >> /etc/network/interfaces
echo "H3 network configuration added."
```

### H4

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 192.168.20.2
        netmask 255.255.255.0
        gateway 192.168.20.254
"

echo "$interfaces" >> /etc/network/interfaces
echo "H4 network configuration added."
```

### GW

```bash
#!/bin/bash

interfaces="
auto eth0.10
iface eth0.10 inet static
        address 192.168.10.254
        netmask 255.255.255.0

auto eth0.20
iface eth0.20 inet static
        address 192.168.20.254
        netmask 255.255.255.0
"

echo "$interfaces" >> /etc/network/interfaces
echo "GW network configuration added."

echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
echo "Ip Forward configurato correttamente."

sysctl -p /etc/sysctl.conf
if [ $? -eq 0 ]; then
    echo "sysctl configuration reloaded successfully."
else
    echo "Failed to reload sysctl configuration."
    exit 1
fi
```