#!/usr/bin/env python3 
import socket
import os
import sys
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 5000         # Port to listen on (non-privileged ports are > 1023)

def rot13(x: str):
    x = x.lower()
    alpha = "abcdefghijklmnopqrstuvwxyz"
    return "".join([alpha[(alpha.find(c)+13)%26] for c in x])

def rot11(x: str):
    x = x.lower()
    alpha = "abcdefghijlmnopqrstuvz"
    return "".join([alpha[(alpha.find(c)+11)%22] for c in x])

def server():
    # main
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            print('DEBUG - Connected by', addr)

            child_pid = os.fork()
            if child_pid == 0:
                data = conn.recv(1024)
                data = data.decode('utf-8')
                token = data.split(": ")[1]

                res = rot11(token)
                
                conn.sendall(f"token from server: {res}".encode('utf-8'))
                
                conn.close()
                os._exit(0)
            else:
                conn.close()

if __name__=='__main__':
    server()