import socket
import sys
import json
import collections

def client():
    if len(sys.argv) != 2:
        print("ERROR: You should provide a single parameter!")
        print("Usage: python3 client.py <filename>")
        sys.exit(1)

    HOST = '127.0.0.1'
    PORT = 3000

    filename = sys.argv[1]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Avvia una connessione TCP
            s.connect((HOST, PORT))

            s.sendall(filename.encode())

            data = s.recv(1024).decode()

            if not data:
                print("ERROR: No data received from server")
                sys.exit(1)
            
            json_response = json.loads(data)
            print(json_response)

            if "error" in dict(json_response).keys():
                print("ERROR: ", json_response["error"])
            elif "wordcount" in dict(json_response).keys():
                wordcount = dict(json_response["wordcount"])
                # Ordina direttamente gli item del dizionario:
                #  1. per frequenza decrescente (-count)
                #  2. per parola alfabetica (word)
                sorted_items = sorted(
                    wordcount.items(),
                    key=lambda item: (-item[1], item[0])
                )

                print("Le 5 parole più frequenti:")
                for word, count in sorted_items[:5]:
                    print(f"{word} → {count}")
                


    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__=='__main__':
    client()