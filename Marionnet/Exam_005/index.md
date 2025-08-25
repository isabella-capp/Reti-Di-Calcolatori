# Laboratorio

Si chiede di realizzare una rete come quella in figura, con due sottoreti ciascuna dotata di gateway che
effettua NAT. Tutto deve essere realizzato usando un unico switch configurando opportunamente le VLAN

**GWC deve fornire:**
- SNAT per i nodi appartenenti alla rete `192.168.100.0/24`
- Servizio DHCP per il nodo client

**GWS deve fornire:**
- DNAT per il protocollo HTTP sul nodo WebSrv
- DNAT per il protocollo SMTP sul nodo MailSrv
Si chiede inoltre di configurare le opportune regole di firewalling in modo che i server accettino
esclusivamente:
    - Traffico necessario al servizio rilevante per ciascun server (HTTP per WebSrv e SMTP per
    MailSrv)
    - Traffico ICMP

![image.png](/Marionnet/img/image_5.png)

**Elementi di valutazione:**
1. Il client può raggiungere GWC (verificare con ping)
2. Il client può raggiungere GWS (verificare con ping)
3. Il client può raggiungere il server sulla porte del servizio HTTP (verificare con nc)
4. Il client riceve il suo indirizzo mediante DHCP (se il server DHCP parte automaticamente è meglio)
5. Le VLAN separano le reti (verificare con arping)
6. Le politiche di firewalling sono correttamente implementate (verificare con nc e nc -u su porta
HTTP/SMTP e altra porta da tutti i nodi della rete, incluso l'altro server)

## Schema di rete

### Client

- interfaccia: eth0.30
- indirizzo IP: 192.168.100.X -> DHCP
- netmask: 255.255.255.0

### GWC

- interfaccia: eth0.30
    - indirizzo IP: 192.168.100.254
    - netmask: 255.255.255.0
- interfaccia: eth0.20
    - indirizzo IP: 2.2.2.2
    - netmask: 255.255.255.255

### WebSrv

- interfaccia: eth0.10
    - indirizzo IP: 192.168.200.1
    - netmask: 255.255.255.0

### MailSrv

- interfaccia: eth0.10
    - indirizzo IP: 192.168.200.2
    - netmask: 255.255.255.0

### GWS

- interfaccia: eth0.10
    - indirizzo IP: 192.168.200.254
    - netmask: 255.255.255.0
- interfaccia: eth0.20
    - indirizzo IP: 1.1.1.1
    - netmask: 255.255.255.255

## Configurazione VLAN

```bash
vlan/create 10
vlan/create 20
vlan/create 30

port/setvlan 1 30  # porta 1 → VLAN 30 → Client
port/setvlan 3 10  # porta 3 → VLAN 10 → WebSrv
port/setvlan 4 10  # porta 4 → VLAN 10 → MailSrv

vlan/addport 10 5
vlan/addport 20 5
vlan/addport 30 2
vlan/addport 20 2

### client

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet dhcp
        hostname client
"

echo "$interfaces" >> /etc/network/interfaces
echo "client network configuration added."
```

### GWC

```bash
#!/bin/bash

interfaces="
auto eth0.20
iface eth0.20 inet static
        address 2.2.2.2
        netmask 255.255.255.255

auto eth0.30
iface eth0.30 inet static
        address 192.168.100.254
        netmask 255.255.255.0

post-up ip route add 1.1.1.1 dev eth0.20
post-up ip route add 192.168.200.0/24 via 1.1.1.1
"

echo "$interfaces" >> /etc/network/interfaces
echo "GW network configuration added."

dnsmasq="
no-resolv
expand-hosts
domain=local

interface=eth0.30
dhcp-option=3,192.168.100.254  #server DHCP - IP della sua VLAN
dhcp-option=6,192.168.100.254  #server DNS
dhcp-option=15,local

#Trovo il min/max con ipcalc
dhcp-range=192.168.100.1,192.168.100.253,255.255.255.0,12h
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

### WebSrv

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 192.168.200.1
        netmask 255.255.255.0
        gateway 192.168.200.254
        
"

echo "$interfaces" >> /etc/network/interfaces
echo "WebSrv network configuration added."
```

### MailSrv

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 192.168.200.2
        netmask 255.255.255.0
        gateway 192.168.200.254
"

echo "$interfaces" >> /etc/network/interfaces
echo "MailSrv network configuration added."
```
>⚠️ **Attenzione**: Anche se MailSrv e WebSrv sono nella VLAN `eth0.10` è sbagliato configurarli con `auto eth0.10` perchè i link della VLAN sono di tipo access, per cui non riuscirebbero ad interpretare correttamente il TAG VLAN.

### GWS

```bash
#!/bin/bash

interfaces="
auto eth0.10
iface eth0.10 inet static
        address 192.168.200.254
        netmask 255.255.255.0

auto eth0.20
iface eth0.20 inet static
        address 1.1.1.1
        netmask 255.255.255.255

post-up ip route add 2.2.2.2 dev eth0.20
post-up ip route add 192.168.100.0/24 via 2.2.2.2
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