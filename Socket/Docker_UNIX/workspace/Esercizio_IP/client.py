#!/usr/bin/env python3
import socket
import os
import sys
import time

PORT = 1025       # Port to connect to

#il client ha due parametri:
# 1. Indirizzo Server
# 2. Indirizzo IP

def client():
    if len(sys.argv) != 3:
        print("Errore devi fornire esattamente due parametri")
        return
    
    HOST = sys.argv[1]
    IP = sys.argv[2]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Avvia una connessione TCP
        s.connect((HOST, PORT))

        # Invia una stringa contenente l'indirizzo IP fornito da linea di comando
        s.sendall(bytes(IP, encoding='utf-8'))
        data = s.recv(1024)

        s.close()

    print("Received Data:" + data.decode('utf-8'))


if __name__=='__main__':
    client()