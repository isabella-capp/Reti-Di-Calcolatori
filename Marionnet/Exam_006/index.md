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
         hwaddress 02:04:06:11:22:33
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

#devo assegnare a H3 sempre lo stesso indirizzo
dhcp-host=02:04:06:11:22:33,H3,192.168.10.30

#Trovo il min/max con ipcalc
dhcp-range=192.168.10.10,192.168.10.20,255.255.255.0,12h
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

#-------------------------------------------------------
# DNAT: Port Forwarding
#-------------------------------------------------------
iptables -t nat -A PREROUTING -p tcp --dport 80 -i $EXT_IF -s 2.2.2.2 -d 1.1.1.1 -j DNAT --to-destination 192.168.10.30:80

iptables -A FORWARD -i $EXT_IF -o $LAN_IF -d 192.168.10.30 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $LAN_IF -o $EXT_IF -s 192.168.10.30 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT

```
