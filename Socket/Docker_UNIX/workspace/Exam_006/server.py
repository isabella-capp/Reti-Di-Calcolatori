import socket
import signal
import sys

def check_address(address: str):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False

def calculate_address(address: str):
    byte = address.split(".")

    if int(byte[0]) >= 0 and int(byte[0]) <= 127:
        class_address = "A"
        netID = f"{byte[0]}.0.0.0"
        broadcast = f"{byte[0]}.255.255.255"
    
    if int(byte[0]) >= 128 and int(byte[0]) <= 191:
        class_address = "B"
        netID = f"{byte[0]}.{byte[1]}.0.0"
        broadcast = f"{byte[0]}.{byte[1]}.255.255"

    if int(byte[0]) >= 192 and int(byte[0]) <= 223:
        class_address = "C"
        netID = f"{byte[0]}.{byte[1]}.{byte[2]}.0"
        broadcast = f"{byte[0]}.{byte[1]}.{byte[2]}.255"
    
    if int(byte[0]) >= 224 and int(byte[0]) <= 239:
        class_address = "D"
    
    if int(byte[0]) >= 240 and int(byte[0]) <= 255:
        class_address = "E"

    return class_address, netID, broadcast
    
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
                    request = conn.recv(1024).decode()

                    check_address(request)

                    class_address, net_id, broadcast = calculate_address(request)
                    
                    if class_address in ["A", "B", "C"]:
                        message = f"{class_address} {net_id} {broadcast}"
                        print(message)
                    else:
                        message = f"{class_address}"
                        print(message)

                    conn.sendall(message.encode())
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()