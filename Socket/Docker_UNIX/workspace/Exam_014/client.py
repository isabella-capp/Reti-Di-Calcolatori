import socket
import sys
import struct

def client():
    if len(sys.argv) != 2:
        print("ERROR: You should provide a single parameter!")
        print("Usage: python3 client.py <num_int>")
        sys.exit(1)

    HOST = '127.0.0.1'
    PORT = 2525

    num_int = int(sys.argv[1])

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

             # Conversione in binario a 16 bit (signed int16)
            bin_repr = format(num_int & 0xFFFF, "016b")
            print(f"Client: valore={num_int}, binario={bin_repr}")
           
            request = struct.pack(">h", num_int)

            print("Request from Client: ", request)
            
            s.sendall(request)
            response = s.recv(1024)
            response = struct.unpack(">h", response)[0]

            print("Response from Server: ", response)

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()