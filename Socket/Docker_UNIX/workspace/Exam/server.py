import socket
import signal
import sys


def server():
    HOST = ''       # Ascolta su tutte le interfacce
    PORT = 4321        

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
                    request = conn.recv(1024).decode().rstrip('\x00')
                    print(f"DEBUG - Received: {request}")

                    cc, value = request.split(",")
                    print(f"Received values: {cc} - {value}")
                    response = None

                    
                    with open("euro_coins.csv", "r") as f:
                        lines = f.readlines()

                    for line in lines:
                        country_code, coin_value, item_represented = line.split(",")
                        if cc == country_code and value == coin_value:  
                            print("founded")
                            response = item_represented 
                            break
                    
                    
                    if response is None:
                        response = "not found\n"

                    response = response.rstrip('\n') + '\x00'
                    print(f"DEBUG - Sending: {response}")
                    #----------------------------------------------
                    # INVIO DEI DATI AL CLIENT
                    #----------------------------------------------
                    conn.sendall(response.encode())
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()