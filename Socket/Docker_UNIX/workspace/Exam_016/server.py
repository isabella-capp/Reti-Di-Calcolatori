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
                    
                    print(message)

                    length = struct.unpack("!H", message[:2])[0]
                    print(length)
                    payload = message[2:length+2]
                    print(payload)
                    checksum = struct.unpack("!H", message[length+2:])[0]

                    print(f"Received message: length= '{length}', payload= '{payload}', checksum= '{checksum}'")
                    
                    checksum_1 = 0
                    for i in range(length):
                        checksum_1 += payload[i]
                    
                    checksum_1 %= 65536

                    if checksum_1 == checksum:
                        response = 'ACK'
                    else:
                        response = 'NACK'
                    
                    print ("Before sending", response.encode('utf-8'))
                    conn.sendall(response.encode('utf-8')) 
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()