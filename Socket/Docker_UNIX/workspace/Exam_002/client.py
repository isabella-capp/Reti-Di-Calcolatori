import socket
import sys

def client():
    if len(sys.argv) != 2:
        print("ERROR: You should provide a single parameter!")
        print("Usage: python3 client.py <server_name>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = 2525

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            hostname = socket.gethostname()
            message = f"Connection from {hostname}"
            s.sendall(message.encode('utf-8'))

            s.close()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()