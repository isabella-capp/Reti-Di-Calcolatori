import socket
import sys
import struct
import os

CHUNK_SIZE = 512

def client():
    if len(sys.argv) != 2:
        print("Usage: python3 client.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"ERROR: File '{filename}' not found")
        sys.exit(1)

    HOST = "127.0.0.1"
    PORT = 3000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server {HOST}:{PORT}")

        with open(filename, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break

                length = len(chunk)
                # flag: 1 se ultimo pacchetto, 0 altrimenti
                flag = 1 if len(chunk) < CHUNK_SIZE else 0

                packet = struct.pack("!H", length) + chunk + struct.pack("!B", flag)
                s.sendall(packet)

                if flag == 1:
                    break

        print("File sent successfully.")

if __name__ == "__main__":
    client()
