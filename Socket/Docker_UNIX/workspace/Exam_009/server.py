import socket
import signal
import sys
import os
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

                pid = os.fork()

                if pid == 0:  # Processo figlio
                    try:
                        with conn:
                            print(f"DEBUG: Connected by {addr}")
                            message = conn.recv(1024)
                            print(f"Received message: {message}")

                            check_num = message[:1]
                            num_bin = message[1:]

                            if check_num == b'\x01':
                                print(len(num_bin))
                                print("DEBUG - Numero a 32 bit {num_bin}")
                                num_int = struct.unpack("f", num_bin)[0]
                                print("DEBUG - Numero intero da processare:", num_int)
                                num_int *=2
                                num_pack = struct.pack("f", num_int)
                                response = b'\x01' + num_pack
                            else:
                                print("DEBUG - Numero a 64 bit")
                                num_int = struct.unpack("d", num_bin)[0]
                                print("DEBUG - Numero intero da processare:", num_int)
                                num_int *=2
                                num_pack = struct.pack("d", num_int)
                                response = b'\x02' + num_pack
                            
                            
                            conn.sendall(response)
                            print(f"Serving client request: {message} {response}")

                        os._exit(0)  # Terminare il processo figlio
                    except Exception as e:
                        print(f"ERROR (child): {e}")
                else:
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()