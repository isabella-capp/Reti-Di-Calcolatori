import socket
import sys
import struct

def client():
    if len(sys.argv) != 3:
        print("ERROR: You should provide two parameters!")
        print("Usage: python3 client.py <ip> <port>")
        sys.exit(1)

    HOST = '127.0.1.1'
    PORT = 1025

    IP_RCV = sys.argv[1]
    PORT_RCV = int(sys.argv[2])

    print(IP_RCV)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            # Conversione numero di porta in unsigned short int a 16 bit (big endian)
            port_uint=struct.pack("!H", PORT_RCV)
            # Conversione indirizzo IP in unsigned int a 32 bit rappresentato in network format (big endian)
            ip_uint=socket.inet_aton(IP_RCV)

            # Invio IP + '\0' + porta + '\0'
            message = ip_uint + b'\0' + port_uint + b'\0'
            s.sendall(message)

            print(f"IP is {IP_RCV}; uint32 is {struct.unpack("!I", ip_uint)[0]}")
            print(f"Port is {PORT_RCV}; uint16 is {struct.unpack("!H", port_uint)[0]}")


    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()