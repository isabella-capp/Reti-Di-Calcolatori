# Laboratorio
Si chiede di realizzare una rete come quella in figura, in cui GW fornisce connettività alle seguenti sottoreti:

- LAN1
    - **Net id**: 192.168.1.0/29
    - **VLAN id**: 10
    - contiene gli host H1, H2 e GWLAN. GWLAN ha indirizzo IP statico che è il più alto disponibile all'intemo della rete. GWLAN esegue un server DHCP che assegna dinamicamente indirizzi IP
- **LAN2**
**Net id**: 192.168.1.8/29
**VLAN id**: 20
contiene gli host GWLAN, GWDMZ, GW configurati staticamente. GW deve avere l'indirizzo più alto all'interno della rete. GWLAN e GWDMZ i più bassi.
- **DMZ**
**Netid**: 192.168.1.16/30
**VLAN id**: 30
contiene il server Sre (indirizzo IP statico. il minore della rete) e GWDMZ (indirizzo IP statico, il più alto della rete) Con riferimento alla figura, i collegamenti tratteggiati sono link trunk, quelli continui sono access link.

GW ha due interfacce di rete:
- eth0, connessa a sw2 configurato staticamente.
- eth1, connessa a sw3. con indirizzo IP 2.3.4.5/32

La simulazione di rete comprende anche un host esterno (Ext) con indirizzo IP 3.4.5.6/32, connesso a sw3.

GWLAN deve:
1. essere default gateway per la rete LAN1
2. eseguire il server DHCP per la configurazione degli host Hl e H2.

GWDMZ deve:
1. essere default gateway per la rete DMZ

GW deve:
1. Effettuare il NAT (quando necessario) per consentire connettività tra tutti gli host della rete
2. Implementare le opportune regole di NAT e filtro di pacchetto in modo che:
    - tutto il traffico non esplicitamente autorizzato sia bloccato
    - H1, H2 possano contattare un server Web server in esecuzione su Ext
    - Ext possa contattare un server Web in esecuzione su Srv

GW, GWLAN, GWDMZ devono effettuare il routing in modo che:
1. traffico da LAN1 a DMZ e viceversa non transiti per GW
2. la connettività fra tutti gli host della rete sia garantita

```scss
@h1: vim /etc/network/interfaces
auto eth0
iface eth0 inet dhcp
	hostname H1
```

```scss
@h2: vim /etc/network/interfaces
auto eth0
iface eth0 inet dhcp
	hostname H2
```

```scss
@GWLAN: vim /etc/network/interfaces
auto eth0.10
iface eth0.10 inet static
	address 192.168.1.6
	netmask 255.255.255.248 
	
auto eth0.20
iface eth0.20 inet static
	address 192.168.1.9
	netmask 255.255.255.248 
	gateway 192.168.1.14

post-up ip route add 192.168.1.16/30 via 192.168.1.10 dev eth0.20

@GWLAN: vim /etc/sysctl.conf
#uncomment line
net.ipv4.ip_forward=1

@GWLAN: sysctl -p /etc/sysctl.conf

@GWLAN: vim /etc/dnsmasq.conf
no-resolv
expand-hosts
domain=local

interface=eth0.10
dhcp-option=3,192.168.1.6  #server DHCP - IP della sua VLAN
dhcp-option=6,192.168.1.6  #server DNS 
dhcp-option=15,local
dhcp-range=192.168.1.1,192.168.1.5,255.255.255.248,12h

@GWLAN: systemctl enable dnsmasq 
@GWLAN: systemctl restart dnsmasq                  
 
```

```scss
@GWDMZ: vim /etc/network/interfaces
auto eth0.30
iface eth0.30 inet static
	address 192.168.1.18
	netmask 255.255.255.252
	
auto eth0.20
iface eth0.20 inet static
	address 192.168.1.10
	netmask 255.255.255.248
	gateway 192.168.1.14
	
post-up ip route add 192.168.1.0/29 via 192.168.1.9 dev eth0.20

@GWDMZ: vim /etc/sysctl.conf
#uncomment line
net.ipv4.ip_forward=1

@GWDMZ: sysctl -p /etc/sysctl.conf
```

```scss
@Srv: vim /etc/network/interfaces
auto eth0
iface eth0 inet static
	address 192.168.1.17
	netmask 255.255.255.252
	gateway 192.168.1.18
```

```scss
@GW: vim /etc/network/interfaces
auto eth0
iface eth0 inet static
	address 192.168.1.14
	netmask 255.255.255.248

auto eth1
iface eth1 inet static
	address 2.3.4.5/32
	
post-up ip route add 3.4.5.6 dev eth1
post-up ip route add 192.168.1.0/29 via 192.168.1.9
post-up ip route add 192.168.1.16/30 via 192.168.1.10

@GW: vim /etc/sysctl.conf
#uncomment line
net.ipv4.ip_forward=1

@GW: sysctl -p /etc/sysctl.conf
```

```scss
@Ext: vim /etc/network/interfaces
auto eth0
iface eth0 inet static
	address 3.4.5.6
	netmask 255.255.255.255
	gateway 2.3.4.5
```

**SW1**

```coffeescript
vlan/create 10
vlan/create 30

port/setvlan 1 10
port/setvlan 2 10
port/setvlan 3 30

vlan/addport 10 4
vlan/addport 30 4
```

**SW2**

```coffeescript
vlan/create 10
vlan/create 20
vlan/create 30

port/setvlan 4 20 

vlan/addport 10 1
vlan/addport 20 1

vlan/addport 30 2
vlan/addport 20 2

vlan/addport 10 3
vlan/addport 20 3
vlan/addport 30 3
```

```bash
#!/bin/bash

# Pulizia regole esistenti
iptables -F
iptables -t nat -F
iptables -X

# Policy di default (blocco totale)
iptables -t filter -P INPUT DROP
iptables -t filter -P OUTPUT DROP
iptables -t filter -P FORWARD DROP

# 1) H1,H2→ Ext: HTTP (porta 80)
iptables -A FORWARD -i eth0 -o eth1 -p tcp -s 192.168.1.0/29 -d 3.4.5.6 --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -p tcp -s 3.4.5.6 -d 192.168.1.0/29 --sport 80 -m state --state ESTABLISHED -j ACCEPT

# NAT: Masquerading per traffico in uscita
iptables -t nat -A POSTROUTING -o eth1 -s 192.168.1.0/29 -j MASQUERADE

# d) Ext → DMZ (Web su Srv)
iptables -t nat -A PREROUTING -p tcp --dport 80 -i eth1 -s 3.4.5.6 -d 2.3.4.5 -j DNAT --to-destination 192.168.1.17
iptables -A FORWARD -i eth1 -o eth0 -p tcp -s 3.4.5.6 -d 192.168.1.17 --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth0 -o eth1 -p tcp -s 192.168.1.17 -d 3.4.5.6 --sport 80 -m state --state ESTABLISHED -j ACCEPT

#ICMP
iptables -t filter -A INPUT -p icmp -j ACCEPT
iptables -t filter -A FORWARD -p icmp -j ACCEPT
iptables -t filter -A OUTPUT -p icmp -j ACCEPT

```