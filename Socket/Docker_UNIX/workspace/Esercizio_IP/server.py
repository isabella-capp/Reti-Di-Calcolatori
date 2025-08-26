#!/usr/bin/env python3 
import socket
import os
import sys

HOST = '127.0.0.1'
PORT = 1025

def determina_classe_ip(ip_address):
    try:
        splitted = ip_address.split(".")
        ottetti = [int(x) for x in splitted]

        primo_ottetto = ottetti[0]

        if 1 <= primo_ottetto <= 127:
            return "A"
        if 128 <= primo_ottetto <= 191:
            return "B"
        if 192 <= primo_ottetto <= 223:
            return "C"
        if 224 <= primo_ottetto <= 239:
            return "D"
        if 240 <= primo_ottetto <= 255:
            return "E"
        else:
            raise ValueError("Invalid IP class")
    except:
        raise

def find_info(classe: str, ip_address):
    splitted = ip_address.split(".")
    ottetti = [int(x) for x in splitted]

    if classe == "A":
        net_id = f"{ottetti[0]}.0.0.0"
        broadcast = f"{ottetti[0]}.255.255.255"
    elif classe == "B":
        net_id = f"{ottetti[0]}.{ottetti[1]}.0.0"
        broadcast = f"{ottetti[0]}.{ottetti[1]}.255.255"
    elif classe == "C":
        net_id = f"{ottetti[0]}.{ottetti[1]}.{ottetti[2]}.0"
        broadcast = f"{ottetti[0]}.{ottetti[1]}.{ottetti[2]}.255"
    else:
        return None, None

    return net_id, broadcast

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
                    try:
                        data = conn.recv(1024)
                        ip = data.decode('utf-8')
                        print(f"[CHILD] IP ricevuto: {ip}")
                        classe = determina_classe_ip(ip)
                        print(f"[CHILD] Classe: {classe}")

                        if classe in ['A', 'B', 'C']:
                            net_id, broadcast = find_info(classe, ip)
                            msg = f"Classe {classe}, NetID: {net_id}, Broadcast: {broadcast}"
                        else:
                            msg = f"Classe {classe} (nessuna info NetID/Broadcast)"

                        conn.sendall(msg.encode('utf-8'))
                    except Exception as e:
                        print(f"[CHILD] Errore: {e}")
                        conn.sendall(b"ERROR")
                    finally:
                        conn.close()
                        os._exit(0)  # Importante: termina figlio
            else:
                # Processo padre
                conn.close()  # Chiude connessione nel padre

if __name__ == '__main__':
    server()
