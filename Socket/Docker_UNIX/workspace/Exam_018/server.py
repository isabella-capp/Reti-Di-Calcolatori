import socket
import struct
import sys
import signal

OUTPUT_FILE = "received_file.bin"

def server():
    HOST = ""
    PORT = 3000

    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on port {PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")

                with open(OUTPUT_FILE, "wb") as f:
                    while True:
                        header = conn.recv(2)
                        if not header:
                            break
                        length = struct.unpack("!H", header)[0]

                        # riceve esattamente length byte
                        chunk = b""
                        while len(chunk) < length:
                            data = conn.recv(length - len(chunk))
                            if not data:
                                break
                            chunk += data

                        flag = conn.recv(1)
                        if not flag:
                            break
                        flag = struct.unpack("!B", flag)[0]

                        f.write(chunk)

                        if flag == 1:
                            print("File received completely.")
                            break
