import socket
import sys

def client():
    if len(sys.argv) != 2:
        print("ERROR: You should provide a single parameter!")
        print("Usage: python3 client.py <token>")
        sys.exit(1)

    HOST = '127.0.1.1'
    PORT = 5000

    token = sys.argv[1]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            message = f"token from client: {token}"
            s.sendall(message.encode('utf-8'))
            print(f"Spedito token: '{token}'")
            response = s.recv(1024).decode()
            index = response.find(":")
            response = response[index+1:].strip()
            print(f"Ricevuto token: '{response}'")


    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()