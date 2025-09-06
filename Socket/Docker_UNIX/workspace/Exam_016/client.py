import socket
import sys
import struct

def client():
    if len(sys.argv) != 2:
        print("ERROR: You should provide a single parameter!")
        print("Usage: python3 client.py <payload>")
        sys.exit(1)

    HOST = '127.0.0.1'
    PORT = 3000

    payload = sys.argv[1].encode('utf-8')
    length = len(payload)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            checksum = 0
            for i in range(length):
                checksum += payload[i]
            
            checksum %= 65536 

            print(f"Request message: length= '{length}', payload= '{payload}', checksum= '{checksum}'")

            length = struct.pack("!H", length)
            checksum = struct.pack("!H", checksum)

            message = length + payload + checksum

            s.sendall(message)
            response = s.recv(1024)
            if not response:
                print("No response received")
                return

            resp_str = response.decode("utf-8")

            print(f"Response from server: '{resp_str}'")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()