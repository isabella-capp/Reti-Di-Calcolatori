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
                    temperature = message[1:]
                    print("Number received: ", temperature)
                    temperature = struct.unpack("f", temperature)[0]

                    if lenght == b'\x01':
                        fahrenheit = ( temperature * 9 / 5 ) + 32
                        res = struct.pack("f", fahrenheit)
                        res = b'\x02' + res
            
                    if lenght == b'\x02':
                        celsius =  ( temperature - 32 ) *  5 / 9 
                        res = struct.pack("f", celsius)
                        res = b'\x01' + res
                    
                    conn.sendall(res) 
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()