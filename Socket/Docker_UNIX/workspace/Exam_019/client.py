import socket
import sys
import json

def client():
    if len(sys.argv) != 3:
        print("ERROR: You should provide two parameters!")
        print("Usage: python3 client.py <key> <value>")
        sys.exit(1)

    HOST = '127.0.0.1'
    PORT = 3000

    key = sys.argv[1]
    value = sys.argv[2]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            json_request = json.dumps(
                {
                    "action": "get", 
                    "key": key, 
                    "value": value
                }
            )

            s.sendall(json_request.encode())

            data = s.recv(1024).decode()

            if not data:
                print("ERROR: No data received from server")
                sys.exit(1)
            
            json_response = json.loads(data)

            if json_response["status"] == 'ok':
                print("Result from server:", json_response["status"])
            else:
                print("ERROR: ", json_response["message"] )


    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()