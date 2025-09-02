# Laboratorio

 Si chiede di realizzare una rete come quella in figura, in cui R1 fornisce connettività a tre sottoreti:
 - `192.168.20.0/24` con Cli1 e Cli2 (configurati mediante DHCP)
 - `192.168.30.0/24` con SrvInt
 - `155.185.48.0/24` con SrvExt

 GW deve fornire connettività a tutte le reti avendo a disposizione una sola scheda di rete collegato allo switch SW (usare opportunamente le VLAN e le schede di rete virtuali)
 
 Si chiede inoltre di implementare sul nodo GW:
 - SNAT per ogni rete con indirizzi privati
 - DNAT per un server sulla porta 80 di SrvInt che deve apparire sulla porta 8000 di R1 e deve essere raggiungibile da tutti le reti

![image.png](/Marionnet/img/image_9.png)

**Elementi di valutazione:**
 1. C’è comunicazione La configurazione DHCP di Cli1 e Cli2 funziona
 2. C’è comunicazione di ogni nodo con R1 ma il dominio di collisione è separato (verificare con ping e arping)
 3. Per ogni sottorete, le interfacce di R1 devono avere il più alto hostID disponibile
 4. SrvExt, Cli1, Cli2 possono dialogare con SrvInt usando il DNAT (verificare con nc)
 5. Cli1 e Cli2 possono dialogare con SrvExt (verificare con ping e controllare con tcpdump il funzionamento del SNAT)

  ## Schema di rete

 ### Cli1 e Cli2

   - **NetID**: 192.168.20.0
   - **VLANID**: 20
   - **Interfaccia**: eth0
        - **Indirizzo IP**: DHCP range: 192.168.20.1 - 192.168.20.253
        - **Netmask**: 255.255.255.0

### SrvExt
   - **NetID**: 155.185.48.0
   - **VLANID**: 10
   - **Interfaccia**: eth0
        - **Indirizzo IP**: 155.185.54.1
        - **Netmask**: 255.255.255.0

### SrvInt
   - **NetID**: 192.168.30.0
   - **VLANID**: 30
   - **Interfaccia**: eth0
        - **Indirizzo IP**: 192.168.30.1
        - **Netmask**: 255.255.255.0

### R1
- **Interfaccia**: eth0.10
   - **Indirizzo IP**: 
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth0.20
   - **Indirizzo IP**: 192.168.20.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth0.30
   - **Indirizzo IP**: 
   - **Netmask**: 255.255.255.0


## Configurazione VLAN
```bash
vlan/create 10
vlan/create 20 
vlan/create 30

port/setvlan 1 20
port/setvlan 2 20
port/setvlan 3 30
port/setvlan 5 10

vlan/addport 10 4
vlan/addport 20 4
vlan/addport 30 4
```

## Configurazione IP

### Cli1

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet dhcp
      hostname Cli1
"

echo "$interfaces" >> /etc/network/interfaces
echo "Cli1 network configuration added."

ifup -a
```

### Cli2

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet dhcp
      hostname Cli2
"

echo "$interfaces" >> /etc/network/interfaces
echo "Cli2 network configuration added."

ifup -a
```

### SrvInt

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
      address 192.168.30.1
      netmask 255.255.255.0
      gateway 192.168.30.254
"

echo "$interfaces" >> /etc/network/interfaces
echo "SrvInt network configuration added."

ifup -a
```

### R1

```bash
#!/bin/bash

interfaces="
auto eth0.10
iface eth0.10 inet static
        address 155.185.48.254
        netmask 255.255.255.0

auto eth0.20
iface eth0.20 inet static
        address 192.168.10.254
        netmask 255.255.255.0

auto eth0.30
iface eth0.30 inet static
        address 192.168.30.254
        netmask 255.255.255.0
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

ifup -a

```

### SrvExt

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
      address 155.185.54.1
      netmask 255.255.255.0
      gateway 192.168.10.254
"

echo "$interfaces" >> /etc/network/interfaces
echo "SrvExt network configuration added."

ifup -a
```

## Configurazione firewall

```bash
EXT_IF="eth0.10"
NET_ID_LAN="192.168.20.0/24"
NET_ID_DMZ="192.168.30.0/24"
IP_SRV_INT=192.168.30.1

#-----------------------------------------
# SNAT
#-----------------------------------------
iptables -t nat -A POSTROUTING -o $EXT_IF -s $NET_ID_LAN  -j MASQUERADE
iptables -t nat -A POSTROUTING -o $EXT_IF -s $NET_ID_DMZ  -j MASQUERADE

#-----------------------------------------
# DNAT: server sulla porta 80 di SrvInt che deve apparire sulla porta 8000 di R1
#-----------------------------------------  
iptables -t nat -A PREROUTING -p tcp --dport 8000 -i $EXT_IF -j DNAT --to-destination $IP_SRV_INT:80

```