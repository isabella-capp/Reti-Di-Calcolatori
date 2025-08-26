#!/usr/bin/env python3 
import socket
import os
import sys
import struct

HOST = '127.0.0.1'
PORT = 1025

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] In ascolto su {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            print('[SERVER] Connessione da', addr)

            pid = os.fork()
            if pid == 0:
                # Processo figlio
                with conn:
                    
                        data = conn.recv(1024)

                        ip_uint32 = struct.unpack("!I", data[0:4])[0]
                        port_uint16 = struct.unpack("!H", data[5:7])[0]
                        
                        ip_str = socket.inet_ntoa(struct.pack("!I", ip_uint32))

                        print(f"uint32 is {ip_uint32}; IP is {ip_str}")
                        print(f"uint16 is {port_uint16}; Port is {port_uint16}")
                        
            else:
                # Processo padre
                conn.close()  # Chiude connessione nel padre

if __name__ == '__main__':
    server()
