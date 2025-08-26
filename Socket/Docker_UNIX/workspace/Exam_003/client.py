import socket
import sys
import json

def client():
    if len(sys.argv) != 2:
        print("ERROR: You should provide a single parameter!")
        print("Usage: python3 client.py <file_name>")
        sys.exit(1)

    filename = sys.argv[1]

    HOST = '127.0.1.1'
    PORT = 8080

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #-----------------------------------------------
            # Avvia una connessione TCP
            #-----------------------------------------------
            s.connect((HOST, PORT))

            #-----------------------------------------------
            # Invia la richiesta JSON
            #-----------------------------------------------
            json_request = json.dumps(
                {
                    "filename": filename
                }
            )  

            s.sendall(json_request.encode())

            #-----------------------------------------------
            # Ricevi la risposta dal server
            #-----------------------------------------------
            data = s.recv(1024).decode('utf-8')

            if not data:
                print("ERROR: No data received from server")
                sys.exit(1)

            #-----------------------------------------------
            # Estrai il contenuto dal messaggio di risposta
            #-----------------------------------------------
            index = data.find('}')
            content = data[index + 2:]

            #-----------------------------------------------
            # Salva il contenuto su file
            #-----------------------------------------------
            with open(filename, "w") as file:
                file.write(content)

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()