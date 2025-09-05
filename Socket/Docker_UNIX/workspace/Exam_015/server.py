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
                    if not message:
                        continue

                    print(f"Received message: {message}")
                    length_packed = message[:2]
                    length = struct.unpack(">H", length_packed)[0]
                    request = message[2:]
                    
                    try:
                        request = request.decode("utf-8")
                    except UnicodeDecodeError:
                        print("ERROR: Invalid UTF-8 sequence")
                        conn.close()
                        continue

                    print(f"Received: length={length}, string='{request}'")

                    response = request.upper()
                    print("Upper: ", response)

                    response = length_packed + response.encode()
                    
                    print ("Before sending", response)
                    conn.sendall(response) 
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()