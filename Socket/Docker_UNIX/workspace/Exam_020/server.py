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

                    filename = conn.recv(1024).decode()
                    print(f"DEBUG: Received data: {filename}")\
                    
                    #-------------------------------------------
                    # OPENING FILE
                    #-------------------------------------------
                    try:
                        with open(filename, "r") as f:
                            print("DEBUG: reading file: ", filename)
                            content = f.read()
                            print("DEBUG: content: ", content)
                    except FileNotFoundError:
                        print("ERROR: file not found")
                        json_response = json.dumps(
                            {"error": "file not found"}
                        )
                        conn.sendall(json_response.encode())
                        continue
                    
                    # Soluzione alternativa se vogliamo dividere solo parole e numeri "ciao" e "ciao," vengono considerati come una unica parola "ciao"
                    # words = re.findall(r"\w+", content.lower())  # prende solo lettere/numeri

                    dictionary = collections.Counter(content.split())

                    json_response = json.dumps({
                        "wordcount": dict(dictionary)
                    })

                    print(json_response)
                    conn.sendall(json_response.encode())              
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()