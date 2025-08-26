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
            content = "Contenuto del file"
            json_request = json.dumps(
                {
                    "filename": filename,
                    "filesize": len(content)
                }
            )  

            request = f"{json_request}\n{content}"

            s.sendall(request.encode())

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
            response = json.loads(data)
            if response["statuscode"] == 200:
                s.close()
                print("Data loaded successfully!")
            else:
                print("ERROR:", response["statuscode"])

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()