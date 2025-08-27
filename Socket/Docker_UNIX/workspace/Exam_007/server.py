import socket
import signal
import sys

def rot13(x):
    x = x.lower()
    alpha = "abcdefghijklmnopqrstuvwxyz"
    return "".join([alpha[(alpha.find(c)+13)%26] for c in x])

def rot11(x):
    x = x.lower()
    alpha = "abcdefghijlmnopqrstuvz"
    return "".join([alpha[(alpha.find(c)+11)%22] for c in x])

def server():
    HOST = ''       # Ascolta su tutte le interfacce
    PORT = 5000        

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

                    message = conn.recv(1024).decode('utf-8')
                    index = message.find(":")
                    token = message[index+1:].strip()
                    print(f"Received token: {token}")
                    token_rot = rot11(token)
                    print(f"Token Server:", token_rot)
                    response = f"token from server: {token_rot}"
                    conn.sendall(response.encode())
                    
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()