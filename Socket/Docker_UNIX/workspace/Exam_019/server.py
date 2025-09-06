import socket
import signal
import sys
import json

def server():
    HOST = ''       # Ascolta su tutte le interfacce
    PORT = 3000        

    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

    database = {
        "nome": "Mario",
        "cognome": "Rossi",
        "età": "25",
        "corso": "Informatica"
    }

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
                    print(f"DEBUG: Received data: {request}")

                    data = json.loads(request)
                    action = data["action"]
                    print(action)

                    if action == "insert":
                        database[data["key"]] = data["value"]
                        response = {"status": "ok", "key": data["key"], "value": data["value"]}
                    elif action == "get":
                        if data["key"] in database:
                            print("Trovato!")
                            response = {"status": "ok", "key": data["key"], "value": database[data["key"]]}
                        else:
                            response = {"status": "error", "message": "key not found"}
                    else:
                        response = {"status": "error", "message": "unknown action"}

                    print(response)
                    json_response = json.dumps(response)
                    conn.sendall(json_response.encode())

                    print("DATABASE: ", database)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()