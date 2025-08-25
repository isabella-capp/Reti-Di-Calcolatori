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

## Configurazione VLAN

```bash
vlan/create 10
vlan/create 20

port/setvlan 1 20
port/setvlan 2 20
port/setvlan 3 10

vlan/addport 10 4
vlan/addport 20 4

```

## Configurazione Rete

### H1

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet dhcp
        hostname H1
"

echo "$interfaces" >> /etc/network/interfaces
echo "H1 network configuration added."
```

### H2

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet dhcp
         hostname H2
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
        address 192.168.10.1
        netmask 255.255.255.0
        gateway 192.168.10.254
"

echo "$interfaces" >> /etc/network/interfaces
echo "H3 network configuration added."
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

auto eth1
iface eth1 inet static
        address 3.3.3.3
        netmask 255.255.255.255

post-up ip route add 5.5.5.5 via 3.3.3.3 dev eth1
"

echo "$interfaces" >> /etc/network/interfaces
echo "GW network configuration added."

dnsmasq="
no-resolv
expand-hosts
domain=local

interface=eth0.20
dhcp-option=3,192.168.20.254  #server DHCP - IP della sua VLAN
dhcp-option=6,192.168.20.254  #server DNS
dhcp-option=15,local

#Trovo il min/max con ipcalc
dhcp-range=192.168.20.1,192.168.20.253,255.255.255.0,12h
"

echo "$dnsmasq" >> /etc/dnsmasq.conf
echo "dnsmasq configuration added."

echo "Eseguo comandi di configurazione"
systemctl enable dnsmasq
if [ $? -eq 0 ]; then
    systemctl restart dnsmasq
    if [ $? -eq 0 ]; then
        echo "dnsmasq restarted successfully."
    else
        echo "Failed to restart dnsmasq."
        echo "Check the dnsmasq logs for more information."
        echo "Exec -> dnsmasq --test or journalctl -xe"
        exit 1
    fi
    echo "Verifica la configurazione di dnsmasq:"
    dnsmasq --test
    if [ $? -eq 0 ]; then
        echo "dnsmasq configuration is valid."
    else
        echo "dnsmasq configuration is invalid."
        exit 1
    fi
else
    echo "Failed to enable dnsmasq."
    exit 1
fi

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
        address 5.5.5.5
        netmask 255.255.255.255
        gateway 3.3.3.3
"

echo "$interfaces" >> /etc/network/interfaces
echo "EXT network configuration added."
```

## Configurazione Firewall

```bash
#!/bin/bash

# Interfacce
LAN_IF="eth0.10"     # verso H1, H2 (LAN)
EXT_IF="eth1"        # verso Ext / Internet

# Pulizia regole esistenti
iptables -F
iptables -t nat -F
iptables -X

#-------------------------------------------------------
# SNAT: Masquerading per traffico in uscita
#-------------------------------------------------------
iptables -t nat -A POSTROUTING -o $EXT_IF -j MASQUERADE

#-------------------------------------------------------
# DNAT: Port Forwarding
#-------------------------------------------------------
iptables -t nat -A PREROUTING -p tcp --dport 80 -i $EXT_IF -j DNAT --to-destination 192.168.10.1:80

iptables -A FORWARD -i $EXT_IF -o $LAN_IF -d 192.168.10.1 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $LAN_IF -o $EXT_IF -s 192.168.10.1 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT

```