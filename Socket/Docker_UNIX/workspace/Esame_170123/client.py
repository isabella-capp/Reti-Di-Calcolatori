#!/usr/bin/env python3
import socket
import os
import sys
import time

PORT = 5000       # Port to connect to

def client():
    if len(sys.argv) != 3:
        print("Errore devi fornire esattamente un parametro")
        return
    
    HOST = sys.argv[1]
    TOKEN = sys.argv[2]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Avvia una connessione TCP
        s.connect((HOST, PORT))

        s.sendall(f"Token from client: {TOKEN}".encode('utf-8'))
        data = s.recv(1024)
        s.close()

    print("Received Data: " + data.decode('utf-8'))


if __name__=='__main__':
    client()