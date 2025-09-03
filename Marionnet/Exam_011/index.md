# Laboratorio

 Si chiede di realizzare una rete come quella in figura, in cui GW fornisce connettività a due sottoreti:
- 10.0.10.0/24 con Srv1 (MAC address 02:04:06:11:22:33)
- 10.0.20.0/24 con Srv2 (MAC address 02:04:06:11:22:44)

 GW deve fornire connettività a entrambe le reti avendo a disposizione una sola scheda di rete collegato allo switch SW (usare opportunamente le VLAN e le schede di rete virtuali). 

Inoltre GW deve ospitare un server DHCP che deve configurare i parametri di rete di entrambi i server.

 Si chiede inoltre di implementare sul nodo GW:
 - SNAT per ogni nodo delle reti considerate
 - DNAT per un server web sulla porta 80 di Srv1 che deve apparire sulla porta 80 di GW
 - DNAT per un server web sulla porta 80 di Srv2 che deve apparire sulla porta 8080 di GW

![image.png](/Marionnet/img/image_11.png)

  **Elementi di valutazione:**
 1. Il server DHCP è configurato correttamente (bonus se il server parte automaticamente)
 2. C’è comunicazione di ogni nodo con GW (incluso Ext – verificare con ping) ma il dominio di collisione è separato (verificare con arping e tcpdump)
 3. C’è comunicazione tra elementi di sottoreti diverse (Srv2 con Srv –  verificare con ping)
 4. Il SNAT su GW consente a ciascun nodo in una sottorete di contattare Ext  (verificare con ping)
 5. Il DNAT su GW consente a Ext di contattare Srv1 e Srv2 (verificare con nc)

 ## Schema di rete

### Srv1

   - **NetID**: 10.0.10.0
   - **VLANID**: 10
   - **Interfaccia**: eth0
        - **Indirizzo IP**: 10.0.10.1
        - **Netmask**: 255.255.255.0

### Srv2

   - **NetID**: 10.0.20.0
   - **VLANID**: 20
   - **Interfaccia**: eth0
        - **Indirizzo IP**: 10.0.20.1
        - **Netmask**: 255.255.255.0

### GW
- **Interfaccia**: eth0.10
   - **Indirizzo IP**: 10.0.10.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth0.20
   - **Indirizzo IP**: 10.0.20.254
   - **Netmask**: 255.255.255.0
- **Interfaccia**: eth1
   - **Indirizzo IP**: 1.1.1.1
   - **Netmask**: 255.255.255.255

### EXT
- **Interfaccia**: eth0
   - **Indirizzo IP**: 2.2.2.2
   - **Netmask**: 255.255.255.255

## Configurazione VLAN
```bash
vlan/create 10
vlan/create 20

port/setvlan 1 10
port/setvlan 2 20

vlan/addport 10 3
vlan/addport 20 3

```


## Configurazione IP

### Srv1

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet dhcp
      hostname Srv1
      hwaddress 02:04:06:11:22:33
"

echo "$interfaces" >> /etc/network/interfaces
echo "Srv1 network configuration added."
```

### Srv2

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet dhcp
      hostname Srv2
      hwaddress 02:04:06:11:22:44
"

echo "$interfaces" >> /etc/network/interfaces
echo "Srv2 network configuration added."
```

### GW

```bash
#!/bin/bash

interfaces="
auto eth0.10
iface eth0.10 inet static
        address 10.0.10.254
        netmask 255.255.255.0

auto eth0.20
iface eth0.20 inet static
        address 10.0.20.254
        netmask 255.255.255.0

auto eth1
iface eth1 inet static
        address 1.1.1.1
        netmask 255.255.255.255

post-up ip route add 2.2.2.2 dev eth1
"

echo "$interfaces" >> /etc/network/interfaces
echo "GW network configuration added."

dnsmasq="
no-resolv
expand-hosts
domain=local

interface=eth0.10
dhcp-option=3,10.0.10.254  #server DHCP - IP della sua VLAN
dhcp-option=6,10.0.10.254  #server DNS
dhcp-option=15,local

#devo assegnare a Srv1 sempre lo stesso indirizzo 
dhcp-host=02:04:06:11:22:33,Srv1,10.0.10.1

#Trovo il min/max con ipcalc
dhcp-range=10.0.10.2,10.0.10.253,255.255.255.0,12h

interface=eth0.20
dhcp-option=3,10.0.20.254  #server DHCP - IP della sua VLAN
dhcp-option=6,10.0.20.254  #server DNS
dhcp-option=15,local

#devo assegnare a Srv2 sempre lo stesso indirizzo 
dhcp-host=02:04:06:11:22:44,Srv2,10.0.20.1

#Trovo il min/max con ipcalc
dhcp-range=10.0.20.2,10.0.20.253,255.255.255.0,12h

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

#!/bin/bash

EXT_IF="eth1"
NET_ID_LAN_1="10.0.10.0/24"
NET_ID_LAN_2="10.0.20.0/24"
IP_SRV_1=10.0.10.1
IP_SRV_2=10.0.20.1

#-----------------------------------------
# SNAT
#-----------------------------------------
iptables -t nat -A POSTROUTING -o $EXT_IF -s $NET_ID_LAN_1  -j MASQUERADE
iptables -t nat -A POSTROUTING -o $EXT_IF -s $NET_ID_LAN_2  -j MASQUERADE

#-----------------------------------------
# DNAT: server sulla porta 80 di SrvInt che deve apparire sulla porta 8000 di R1
#-----------------------------------------  
iptables -t nat -A PREROUTING -p tcp --dport 80 -i $EXT_IF -j DNAT --to-destination $IP_SRV_1:80

iptables -t nat -A PREROUTING -p tcp --dport 8080 -i $EXT_IF -j DNAT --to-destination $IP_SRV_2:80

```
