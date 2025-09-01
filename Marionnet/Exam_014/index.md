## Laboratorio


Si chiede di realizzare e configurare la rete proposta in Figura 1, in cui GW permette la **connettività tra tutti gli host** della rete e agisce anche come **server DHCP**.
In particolare, la rete interna è composta da due VLAN identificate dai **tag 42** e **43** a cui corrispondono rispettivamente le sottoreti **10.42.0.0/25** e **10.42.0.128/25**


![image.png](/Marionnet/img/image_14.png)

All’interno della rete privata i nodi devono essere configurati rispettando le seguenti specifiche:

- **H1** e **H2** (indirizzi IP assegnati mediante DHCP ma fissi corrispondenti ai **primi due indirizzi** disponibili nella sottorete **10.42.0.0/25**)
- **SRV** (indirizzo IP statico corrispondente al **primo indirizzo** disponibile nella sottorete
**10.42.0.128/25**) → 10.42.0.129/25
- **GW** (indirizzo IP statico corrispondente all’ **ultimo indirizzo disponibile** nelle due sottoreti identificati dalle VLAN 42 e 43)
Ha due interfacce di rete:
    - **eth0**, connessa a sw1.
    - **eth1**, connessa a sw2, con **indirizzo IP 2.2.2.42/32**

La simulazione di rete comprende anche un host esterno (EXT) con indirizzo IP **2.20.20.20/32**, connesso sw2

GW deve:

1. Permettere **connettività tra le due sottoreti**
2. Eseguire il **server DHCP e DNS** per la configurazione degli host all’interno della sottorete.
3. Effettuare il routing in modo che la **connettività fra tutti gli host** della rete sia garantita.
    
    **NB:** il routing tra GW e EXT deve essere fatto impostando regole che usino l’IP
    pubblico dell’interfaccia eth1 di GW e l’ip pubblico dell’interfaccia eth0 di EXT
    
4. Implementare le **opportune regole di NAT** e filtro di pacchetto necessarie per il corretto funzionamento


**Regole di NAT** e politiche di filtraggio sul firewall

1. Utilizzare una **policy di negazione implicita** per tutti i pacchetti in transito, ingresso e uscita da GW
2. Consentire flussi di comunicazione UDP per il corretto funzionamento del protocollo DHCP tra gli host della **VLAN 42** e **GW**
3. Consentire a tutte le **macchine della rete interna** di accedere a macchine in **Internet** condividendo l’IP pubblico associato all’interfaccia eth1 di GW
4. Consentire **connessioni HTTP** generate dalla **sottorete 10.42.0.0/25** verso il server web in esecuzione su **SRV** (testare con nc)
5. Consentire **connessioni SSH** generate dalla macchina **H1** verso **GW**
6. Consentire alle macchine della **rete LAN** di contattare un **server Web** in esecuzione su **EXT** (testare con nc)
7. **EXT** possa contattare un **server Web** in esecuzione su **SRV** utilizzando l’IP pubblico associato all’interfaccia eth1 di GW (testare con nc)
8. Consentire il **passaggio di traffico ICMP** tra tutti i nodi.
    
    Si ricorda che per abilitare il traffico ICMP è possibile usare il seguente comando per tutte le
    catene con una policy DROP:
    iptables-t filter-A {CATENA}-p icmp-j ACCEPT


 ### H1 
**DHCP**
   - **Indirizzo IP**: 10.42.0.1
   - **Netmask**: 255.255.255.128

 ### H2
**DHCP**
   - **Indirizzo IP**: 10.42.0.2
   - **Netmask**: 255.255.255.128

### SRV

   - **Indirizzo IP**: 10.42.0.129
   - **Netmask**: 255.255.255.128

### GW
- **Interfaccia**: eth0.42
   - **Indirizzo IP**: 10.42.0.126
   - **Netmask**: 255.255.255.128
- **Interfaccia**: eth0.43
   - **Indirizzo IP**: 10.42.0.254
   - **Netmask**: 255.255.255.128   
- **Interfaccia**: eth1
   - **Indirizzo IP**: 2.2.2.42
   - **Netmask**: 255.255.255.255

### EXT
- **Interfaccia**: eth0
   - **Indirizzo IP**: 2.20.20.20
   - **Netmask**: 255.255.255.255


## Configurazione VLAN
```bash
vlan/create 42
vlan/create 43

port/setvlan 1 42
port/setvlan 2 42
port/setvlan 3 43

vlan/addport 42 4
vlan/addport 43 4
```

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

### SRV

```bash
#!/bin/bash

interfaces="
auto eth0
iface eth0 inet static
        address 10.42.0.129
        netmask 255.255.255.128
        gateway 10.42.0.254
"

echo "$interfaces" >> /etc/network/interfaces
echo "SRV network configuration added."
```

### GW

```bash
#!/bin/bash

interfaces="
auto eth0.42
iface eth0.42 inet static
        address 10.42.0.126
        netmask 255.255.255.128

auto eth0.43
iface eth0.43 inet static
        address 10.42.0.254
        netmask 255.255.255.128

auto eth1
iface eth1 inet static
        address 2.2.2.42
        netmask 255.255.255.255

post-up ip route add 2.20.20.20 dev eth1
"

echo "$interfaces" >> /etc/network/interfaces
echo "GW network configuration added."

dnsmasq="
no-resolv
expand-hosts
domain=local

interface=eth0
dhcp-option=3,10.42.0.126  #server DHCP - IP della sua VLAN
dhcp-option=6,10.42.0.126  #server DNS
dhcp-option=15,local

#devo assegnare a H1 sempre lo stesso indirizzo 
dhcp-host=02:04:06:e0:a0:f7,H1,10.42.0.1
dhcp-host=02:04:06:67:8a:1f,H2,10.42.0.2

#Trovo il min/max con ipcalc
dhcp-range=10.42.0.3,10.42.0.125,255.255.255.128,12h
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
        address 2.20.20.20
        netmask 255.255.255.255
        gateway 2.2.2.42
"

echo "$interfaces" >> /etc/network/interfaces
echo "EXT network configuration added."
```

## Configurazione Firewall

```bash
#!/bin/bash

# Interfacce
LAN_IF="eth0.42"     # verso H1, H2 (LAN)
DMZ_IF="eth0.43"     # verso SRV
EXT_IF="eth1"        # verso Ext / Internet

# Pulizia regole esistenti
iptables -F
iptables -t nat -F
iptables -X

# Policy di default (blocco totale)
iptables -t filter -P INPUT DROP
iptables -t filter -P OUTPUT DROP
iptables -t filter -P FORWARD DROP

#------------------------------------------------
# DHCP LAN 
#------------------------------------------------
iptables -t filter -A INPUT  -i $LAN_IF  -p udp --sport 68 --dport 67 -j ACCEPT
iptables -t filter -A OUTPUT -o $LAN_IF  -p udp --sport 67 --dport 68 -j ACCEPT

#------------------------------------------------
# DNS LAN
#------------------------------------------------
iptables -A INPUT -i $LAN_IF -p udp -s 10.42.0.0/25 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o $LAN_IF -p udp -d 10.42.0.0/25 --sport 53 -m state --state ESTABLISHED -j ACCEPT

#----------------------------------------------------------------------------------------------
# CONSENTIRE ALLE MACCHINE DELLA LAN DI ACCEDERE AD INTERNET CONDIVIDENDO L'IP PUBBLICO DEL GW
#----------------------------------------------------------------------------------------------
iptables -t nat -A POSTROUTING -o $EXT_IF -s 10.42.0.0/25 -j MASQUERADE

#------------------------------------------------
# H1, H2 -> SRV: HTTP -> 80
#------------------------------------------------
iptables -A FORWARD -p tcp --dport 80 -i $LAN_IF -o $DMZ_IF -d 10.42.0.129 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -p tcp --sport 80 -i $DMZ_IF -o $LAN_IF -s 10.42.0.129 -m state --state ESTABLISHED -j ACCEPT

#------------------------------------------------
# H1 -> GW : SSH
#------------------------------------------------
iptables -t filter -A INPUT  -i $LAN_IF -p tcp -s 10.42.0.1 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -t filter -A OUTPUT -o $LAN_IF -p tcp -d 10.42.0.1 --sport 22 -m state --state ESTABLISHED -j ACCEPT

#------------------------------------------------
# H1, H2 -> EXT : HTTP -> 80
#------------------------------------------------
iptables -A FORWARD -p tcp -i $LAN_IF -o $EXT_IF --dport 80 -j ACCEPT
iptables -A FORWARD -p tcp -o $EXT_IF -i $LAN_IF --sport 80 -m state --state ESTABLISHED,RELATED -j ACCEPT

#-------------------------------------------------
# EXT -> SRV: utilizzando ip pubblico di GW
#-------------------------------------------------
iptables -t nat -A PREROUTING -p tcp --dport 80 -i $EXT_IF -j DNAT --to-destination 10.42.0.129:80

iptables -A FORWARD -p tcp --dport 80 -i $EXT_IF -o $DMZ_IF -d 10.42.0.129 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -p tcp --sport 80 -i $DMZ_IF -o $EXT_IF -s 10.42.0.129 -m state --state ESTABLISHED -j ACCEPT


#-------------------------------------------------
# ICMP
#-------------------------------------------------
 iptables -t filter -A INPUT   -p icmp -j ACCEPT
 iptables -t filter -A OUTPUT  -p icmp -j ACCEPT
 iptables -t filter -A FORWARD -p icmp -j ACCEPT

```