import socket
import signal
import sys
import json
import os

def server():
    HOST = ''       # Ascolta su tutte le interfacce
    PORT = 8080        

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
                    print(f"DEBUG: Connection from {addr}")

                    #-----------------------------------------------
                    # Ricevi la richiesta JSON
                    #-----------------------------------------------
                    request = conn.recv(1024).decode()
                    print(f"DEBUG: Received data: {request}")

                    data = request.split("\n")
                    json_info = data[0]
                    content = data[1]
                
                    data = json.loads(json_info)
                    filename = data["filename"]
                    print(filename)

                    #-----------------------------------------------
                    # Leggi il contenuto del file
                    #-----------------------------------------------
                    try:
                        directory = "uploads/" + filename

                        with open(directory, "w") as f:
                            f.write(content)


                        json_response = json.dumps(
                            {
                                "statuscode": 200
                            }
                        )
                    except Exception as e:
                        print("ERROR:", e)

                        json_response = json.dumps(
                            {
                                "statuscode": 500
                            }
                        )

                    conn.sendall(json_response.encode())                 
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()