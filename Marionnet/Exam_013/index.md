# Laboratorio

Si chiede di realizzare una rete come quella in figura, in cui GW fornisce connettività a tutti gli host all'interno
di un'unica rete `192.168.1.0/25`.

**La rete LAN contiene:**
- H1 (indirizzo IP dinamico fornito dal server DHCP)
- H2 (indirizzo IP dinamico fornito dal server DHCP)
- SRV (indirizzo IP statico fornito dal server DHCP, corrispondente al primo indirizzo valido della sottorete)
- GW (indirizzo IP statico corrispondente al più alto indirizzo valido della sottorete)

**GW ha due interfacce di rete:**
- eth0, connessa a sw1.
- eth1, connessa a sw2, con indirizzo IP `9.8.7.6/32`

La rete comprende anche un esterno (EXT) con indirizzo IP `2.1.3.4/32`, connesso a sw2.

GW deve:
- eseguire il server DHCP e DNS per la configurazione degli host all'interno della sottorete.
- essere default gateway per la rete LAN
- effettuare il routing in modo che la connettività fra tutti gli host della rete sia garantita
- implementare le opportune regole di NAT e filtro di pacchetto necessarie per il corretto funzionamento.

![image.png](/Marionnet/img/image_13.png)

Politiche di filtraggio sul firewall:
- Utilizzare una policy di negazione implicita per tutti i pacchetti in transito, ingresso e uscita da GW
- Consentire flussi di comunicazione UDP per il corretto funzionamento del protocollo DHCP
- Consentire flussi di comunicazione UDP per il corretto funzionamento del protocollo DNS
- Consentire connessioni SSH generate dalla macchina H1 (usare l'ip ottenuto dal DHCP) verso GW
- Consentire alle macchine della rete LAN di contattare un server Web in esecuzione su EXT
- Consentire a EXT di contattare un server Web in esecuzione su SRV utilizzando l'ip pubblico associato all'interfaccia eth1 di GW
- Consentire a EXT di contattare un server SSH in esecuzione su H1 (usare l'ip ottenuto dal DHCP) utilizzando l'indirizzo IP pubblico associato all'interfaccia eth1 di GW
- Testare l'invio di file da EXT a SRV con nc

**Elementi di valutazione:**
1. I nodi della rete sono configurati correttamente
2. Le regole di routing sono corrette
3. GW blocca tutto il traffico non espressamente consentito
4. I protocolli DHCP e DNS sono correttamente configurati e forniscono i parametri adeguati
5. H1 riesce a contattare il server SSH in esecuzione su GW
6. I nodi comunichino correttamente con un server Web sul nodo EXT (verificare con nc)
7. EXT può accedere al servizio Web erogato da SRV (verificare con nc)
8. EXT riesce a raggiungere il server SSH su H1 contattando GW (ssh root@9.8.7.6)


 ## Schema di rete

### H1

   - **NetID**: 192.168.1.0
   - **Interfaccia**: eth0
        - **Indirizzo IP**: ---
        - **Netmask**: 255.255.255.128

### H2

   - **NetID**: 192.168.1.0
   - **Interfaccia**: eth0
        - **Indirizzo IP**: ---
        - **Netmask**: 255.255.255.128

### Srv

   - **NetID**: 192.168.1.0
   - **Interfaccia**: eth0
        - **Indirizzo IP**: 192.168.1.1
        - **Netmask**: 255.255.255.128

### GW
- **Interfaccia**: eth0
   - **Indirizzo IP**: 192.168.1.126
   - **Netmask**: 255.255.255.128
- **Interfaccia**: eth1
   - **Indirizzo IP**: 9.8.7.6
   - **Netmask**: 255.255.255.255

### EXT
- **Interfaccia**: eth0
   - **Indirizzo IP**: 2.1.3.4
   - **Netmask**: 255.255.255.255


## Configurazione IP

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

### Srv

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet dhcp
      hostname Srv
"

echo "$interfaces" >> /etc/network/interfaces
echo "Srv network configuration added."
```

### GW

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 192.168.1.126
        netmask 255.255.255.128

auto eth1
iface eth1 inet static
        address 9.8.7.6
        netmask 255.255.255.255

post-up ip route add 2.1.3.4 dev eth1
"

echo "$interfaces" >> /etc/network/interfaces
echo "GW network configuration added."

dnsmasq="
no-resolv
expand-hosts
domain=local

interface=eth0
dhcp-option=3,192.168.1.126  #server DHCP - IP della sua VLAN
dhcp-option=6,192.168.1.126  #server DNS
dhcp-option=15,local

#devo assegnare a Srv sempre lo stesso indirizzo 
dhcp-host=02:04:06:8b:b0:6c,Srv,192.168.1.1

#Trovo il min/max con ipcalc
dhcp-range=192.168.1.2,192.168.1.125,255.255.255.128,12h

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
         address 2.1.3.4
         netmask 255.255.255.255
         gateway 9.8.7.6
"

echo "$interfaces" >> /etc/network/interfaces
echo "EXT network configuration added."
```

## Configurazione firewall
```bash
LAN_IF="eth0"
EXT_IF="eth1"
NET_ID_LAN="192.168.1.0/25"
LAN_HOST=
IP_EXT="2.1.3.4"
IP_SRV="192.168.1.1"

# Policy di default (blocco totale)
iptables -t filter -P INPUT DROP
iptables -t filter -P OUTPUT DROP
iptables -t filter -P FORWARD DROP

#--------------------------------------------------
# DHCP
#--------------------------------------------------
iptables -A INPUT -i $LAN_IF -p udp --sport 68 --dport 67 -j ACCEPT
iptables -A OUTPUT -o $LAN_IF -p udp --sport 67 --dport 68 -j ACCEPT

#--------------------------------------------------
# DNS
#--------------------------------------------------
iptables -A INPUT -i $LAN_IF -p udp -s $NET_ID_LAN --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o $LAN_IF -p udp -d $NET_ID_LAN --sport 53 -m state --state ESTABLISHED -j ACCEPT

#--------------------------------------------------
# SSH
#--------------------------------------------------
iptables -A INPUT -i $LAN_IF -p tcp -s $LAN_HOST --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o $LAN_IF -p tcp -d $LAN_HOST --sport 22 -m state --state ESTABLISHED -j ACCEPT

#--------------------------------------------------
# LAN -> EXT
#--------------------------------------------------
iptables -A FORWARD -i $LAN_IF -o $EXT_IF -p tcp -s $NET_ID_LAN -d $IP_EXT --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT

iptables -A FORWARD -i $EXT_IF -o $LAN_IF -p tcp -s $IP_EXT -d $NET_ID_LAN --sport 80 -m state --state ESTABLISHED -j ACCEPT

#--------------------------------------------------
# EXT -> SRV
#--------------------------------------------------
iptables -t nat -A PREROUTING -p tcp --dport 80 -i $EXT_IF -j DNAT --to-destination $IP_SRV:80

iptables -A FORWARD -p tcp --dport 80 -i $EXT_IF -o $LAN_IF -d $IP_SRV -m state --state NEW,ESTABLISHED -j ACCEPT

iptables -A FORWARD -p tcp --sport 80 -i $DMZ_IF -o $LAN_IF -s $IP_SRV -m state --state ESTABLISHED -j ACCEPT

#----------------------------------------------------
# EXT -> H1 (SSH)
#----------------------------------------------------
iptables -t nat -A PREROUTING -p tcp --dport 22 -i $EXT_IF -j DNAT --to-destination $LAN_HOST:22

iptables -A INPUT -i $EXT_IF -p tcp -s $IP_EXT --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o $LAN_IF -p tcp -d $IP_EXT --sport 22 -m state --state ESTABLISHED -j ACCEPT

```