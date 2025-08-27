import socket
import sys

def client():
    if len(sys.argv) != 3:
        print("ERROR: You should provide two parameters!")
        print("Usage: python3 client.py <server_name> <IPv4_address>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = 1025
    address = sys.argv[2]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            s.sendall(address.encode())

            response = s.recv(1024).decode()
            if response:
                print("Received:", response)
            else:
                print("ERROR")

            s.close()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()