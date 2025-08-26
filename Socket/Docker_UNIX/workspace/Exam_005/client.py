import socket
import sys

def client():
    if len(sys.argv) != 2:
        print("ERROR: You should provide a single parameter!")
        print("Usage: python3 client.py '<seed>,<niterations>\r\n' ")
        sys.exit(1)

    HOST = '127.0.1.1'
    PORT = 8080

    input = sys.argv[1]    

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            print(input)

            s.sendall(input.encode())

            s.close()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()