import socket
import signal
import sys
import struct

def server():
    HOST = ''       # Ascolta su tutte le interfacce
    PORT = 3000        

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
                    print(f"Received message: {message}")
                    lenght = message[:1]
                    print("lenght", lenght)
                    termine_1 = message[1:5]
                    termine_2 = message[5:]
                    print("Number received: ", termine_1, termine_2)
                    termine_1 = struct.unpack("f", termine_1)[0]
                    termine_2= struct.unpack("f", termine_2)[0]

                    if lenght == b'\x01':
                        res = termine_1 + termine_2
            
                    if lenght == b'\x02':
                        res = termine_1 - termine_2

                    if lenght == b'\x03':
                        res = termine_1 * termine_2

                    if lenght == b'\x04':
                        res = termine_1 / termine_2
                    
                    res = lenght + struct.pack("f", res)
                    conn.sendall(res) 
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()