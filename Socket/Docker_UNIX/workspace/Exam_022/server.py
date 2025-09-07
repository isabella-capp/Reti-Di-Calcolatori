import socket
import signal
import sys
import json
import collections

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

                    string_to_check = conn.recv(1024).decode()
                    print(f"DEBUG: Received data: {string_to_check}")

                    string_to_check = string_to_check.lower().strip()
                    reversed_string_to_check = string_to_check[::-1]

                    if string_to_check == reversed_string_to_check:
                        message = json.dumps(
                            {"palindrome": True}
                        )
                    else:
                        message = json.dumps(
                            {"palindrome": False}
                        )
                     
                    conn.sendall(message.encode())                                    
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()