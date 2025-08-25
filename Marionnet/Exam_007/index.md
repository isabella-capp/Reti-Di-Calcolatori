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
iface eth0 inet dhcp
         hostname H3
"

echo "$interfaces" >> /etc/network/interfaces
echo "H3 network configuration added."
```

### GW

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 192.168.10.254
        netmask 255.255.255.0

auto eth1
iface eth1 inet static
        address 1.1.1.1
        netmask 255.255.255.255

post-up ip route add 2.2.2.2 via 1.1.1.1 dev eth1
"

echo "$interfaces" >> /etc/network/interfaces
echo "GW network configuration added."

dnsmasq="
no-resolv
expand-hosts
domain=local

interface=eth0
dhcp-option=3,192.168.10.254  #server DHCP - IP della sua VLAN
dhcp-option=6,192.168.10.254  #server DNS
dhcp-option=15,local

#Trovo il min/max con ipcalc
dhcp-range=192.168.10.1,192.168.10.3,255.255.255.0,12h
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
        address 2.2.2.2
        netmask 255.255.255.255
        gateway 1.1.1.1
"

echo "$interfaces" >> /etc/network/interfaces
echo "EXT network configuration added."
```

## Configurazione Firewall

```bash
#!/bin/bash

# Interfacce
LAN_IF="eth0"     # verso H1, H2 (LAN)
EXT_IF="eth1"        # verso Ext / Internet

# Pulizia regole esistenti
iptables -F
iptables -t nat -F
iptables -X

#-------------------------------------------------------
# SNAT: Masquerading per traffico in uscita
#-------------------------------------------------------
iptables -t nat -A POSTROUTING -o $EXT_IF -j MASQUERADE

```
