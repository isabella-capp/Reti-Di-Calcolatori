import socket
import sys
import struct

def client():
    if len(sys.argv) % 2 != 1:
        print("ERROR: You should provide an odd number of parameters!")
        print("Usage: python3 client.py <type> <value> ...")
        sys.exit(1)

    HOST = '127.0.0.1'
    PORT = 3000

    records = sys.argv[1:]
    length = int(len(records)/2)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            length_packed = struct.pack("!B", length)
            print(length_packed)
            message = length_packed

            for i in range(0, length * 2, 2):
                print(f"iteration {i}: {records[i], records[i+1]}")
                type_sensor = struct.pack("!B", int(records[i])) 
                value = struct.pack("!f", float(records[i+1]))
                message += type_sensor + value
                print(message)
               

            print(message)

            s.sendall(message)

            response = s.recv(1024).decode('utf-8')

            print(f"Response from server: \n{response}")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()