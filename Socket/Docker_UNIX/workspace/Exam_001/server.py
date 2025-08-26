import socket
import signal
import sys

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

                with conn:
                    print(f"DEBUG: Connected by {addr}")

                    hostname = socket.gethostname()
                    message = f"Welcome from {hostname}"
                    conn.sendall(message.encode('utf-8'))
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()