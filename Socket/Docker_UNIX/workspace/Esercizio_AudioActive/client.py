#!/usr/bin/env python3
import socket
import os
import sys
import time

HOST = "127.0.0.1"
PORT = 8080       # Port to connect to

#il client ha due parametri:
# 1. Indirizzo Server
# 2. Indirizzo IP

def client():
    if len(sys.argv) != 2:
        print("Errore devi fornire esattamente due parametri")
        return
    
    input = sys.argv[1]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Avvia una connessione TCP
        s.connect((HOST, PORT))
        
        # Invia una stringa contenente l'indirizzo IP fornito da linea di comando
        # Invia una stringa contenente SEED e NUM_ITER separati da uno spazio
        s.sendall(input.encode('utf-8'))


if __name__=='__main__':
    client()