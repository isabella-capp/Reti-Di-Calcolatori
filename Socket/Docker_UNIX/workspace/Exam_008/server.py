import socket
import signal
import sys
import struct

def server():
    HOST = ''       # Ascolta su tutte le interfacce
    PORT = 1025        

    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()

            print(f"DEBUG: Server listening on port {PORT}")

            while True:
                conn, addr = s.accept()

                with conn:
                    print(f"DEBUG: Connected by {addr}")
                    message = conn.recv(1024)
                    ip_uint32 = struct.unpack("!I", message[:4])[0]
                    port_uint16 = struct.unpack("!H", message[5:7])[0]

                    ip_bin = struct.pack("!I", ip_uint32)
                    ip = socket.inet_ntoa(ip_bin)
                    
                    print(f"uint32 is {ip_uint32}; IP is {ip}")
                    print(f"uint16 is {port_uint16}; port is {int(port_uint16)}")
                    
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()