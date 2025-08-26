#!/usr/bin/env python3
import socket
import os
import re

HOST = '127.0.0.1'
PORT = 8080

def look_and_say(seed, n):
    result = []
    current = seed
    for _ in range(n):
        next_seq = ""
        count = 1
        for i in range(1, len(current)):
            if current[i] == current[i-1]:
                count += 1
            else:
                next_seq += str(count) + current[i-1]
                count = 1
        next_seq += str(count) + current[-1]
        result.append(next_seq)
        current = next_seq
    return result

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
                s.close()  # Chiudi socket di ascolto nel figlio
                with conn:
                    try:
                        data = conn.recv(1024).decode('utf-8').strip()

                        # Validazione con regex
                        if not re.fullmatch(r"[0-9],[0-9]+\r?", data):
                            conn.sendall(b"- ERR\r\n")
                            os._exit(0)

                        seed_str, iterations_str = data.split(',')
                        seed = seed_str
                        iterations = int(iterations_str)

                        response = f"+ OK {iterations} iterations on seed {seed}\r\n"
                        conn.sendall(response.encode())

                        results = look_and_say(seed, iterations)
                        for r in results:
                            conn.sendall((r + "\r\n").encode())

                    except Exception as e:
                        print(f"[CHILD] Errore: {e}")
                        conn.sendall(b"- ERR\r\n")
                    finally:
                        conn.close()
                        os._exit(0)
            else:
                conn.close()  # Chiude connessione nel padre

if __name__ == '__main__':
    server()
