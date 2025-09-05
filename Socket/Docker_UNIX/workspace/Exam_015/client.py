import socket
import sys
import struct

def client():
    if len(sys.argv) != 2:
        print("ERROR: You should provide a single parameter!")
        print("Usage: python3 client.py <num_int>")
        sys.exit(1)

    HOST = '127.0.0.1'
    PORT = 3000

    string = sys.argv[1]
    length = len(string)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            length = struct.pack(">H", length)
    
            message = length + string.encode("UTF-8")

            s.sendall(message)
            response = s.recv(1024)
            if not response:
                print("No response received")
                return

            resp_len = struct.unpack(">H", response[:2])[0]
            resp_str = response[2:].decode("utf-8")

            print(f"Response from server: length={resp_len}, string='{resp_str}'")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()