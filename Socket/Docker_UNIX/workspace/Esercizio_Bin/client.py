#!/usr/bin/env python3
import socket
import struct
import sys

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

if len(sys.argv) != 3:
    print("Usage: ./client.py <IPv4> <PORT>")
    sys.exit(1)

ip_str = sys.argv[1]
port_int = int(sys.argv[2])

# Conversione IP e PORTA
ip_uint32 = ip2int(ip_str)
port_uint16 = port_int

# Packing in formato network byte order (big endian)
ip_bytes = struct.pack('!I', ip_uint32)
port_bytes = struct.pack('!H', port_uint16)

# Costruzione messaggio: IP + \0 + PORT + \0
message = ip_bytes + b'\x00' + port_bytes + b'\x00'

# Connessione TCP verso 127.0.0.1:1025
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 1025))
    s.sendall(message)

# Output richiesto
print(f"IP is {ip_str}; uint32 is {ip_uint32}")
print(f"Port is {port_int}; uint16 is {port_uint16}")
