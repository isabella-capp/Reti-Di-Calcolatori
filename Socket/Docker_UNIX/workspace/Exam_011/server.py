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
                    lenght = message[:2]
                    unpacked_lenght = struct.unpack(">H", lenght)[0]
                    print("lenght", unpacked_lenght)
                    request = message[2:].decode("utf-8")
                    print("request message: ", request)

                    response = str.upper(request)
                    print("Upper: ", response)

                    response = lenght + response.encode()
                    
                    print ("Before sending", response)
                    conn.sendall(response) 
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()