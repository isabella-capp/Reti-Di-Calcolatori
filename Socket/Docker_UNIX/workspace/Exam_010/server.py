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
                    num_bin = message[1:]
                    print("Number received: ", num_bin)

                    if lenght == b'\x01':
                        num_int = struct.unpack("!B", num_bin)[0]
                        print("Unpacked number: ", num_int)
                        num_res = num_int * 10
                        response = lenght + struct.pack("!B", num_res)
                        print(f"response: ", response)

                    if lenght == b'\x02':
                        num_int =  struct.unpack("!H", num_bin)[0]
                        print("Unpacked number: ", num_int)
                        num_res = num_int * 10
                        response = lenght + struct.pack("!H", num_res)
                        print(f"response: ", response)

                    if lenght == b'\x04':
                        num_int =  struct.unpack("!I", num_bin)[0]
                        print("Unpacked number: ", num_int)
                        num_res = num_int * 10
                        response = lenght + struct.pack("!I", num_res)
                        print(f"response: ", response)
                    
                    print ("Before sending", response)
                    conn.sendall(response) 
                    print(f"Serving client request: {num_int} {num_res} ")
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()