import socket
import signal
import sys
import os

def server():
    HOST = ''       # Ascolta su tutte le interfacce
    PORT = 2525        

    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()

            print(f"DEBUG: Server listening on port {PORT}")

            while True:
                conn, addr = s.accept()

                pid = os.fork()

                if pid == 0:  # Processo figlio
                    try:
                        with conn:
                            print(f"DEBUG: Connected by {addr}")
                            message = conn.recv(1024).decode('utf-8')
                            print(f"Received message: {message}")
                        os._exit(0)  # Terminare il processo figlio
                    except Exception as e:
                        print(f"ERROR (child): {e}")
                else:
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()