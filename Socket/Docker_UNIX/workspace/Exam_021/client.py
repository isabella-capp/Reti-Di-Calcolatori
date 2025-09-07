import socket
import sys
import json
import collections

def client():
    if len(sys.argv) != 2:
        print("ERROR: You should provide a single parameter!")
        print("Usage: python3 client.py <string>")
        sys.exit(1)

    HOST = '127.0.0.1'
    PORT = 3000

    string_to_parse = sys.argv[1]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            s.sendall(string_to_parse.encode())

            data = s.recv(1024).decode()

            if not data:
                print("ERROR: No data received from server")
                sys.exit(1)
            
            response_json = json.loads(data)

            print("Response from server: ", response_json)  

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()