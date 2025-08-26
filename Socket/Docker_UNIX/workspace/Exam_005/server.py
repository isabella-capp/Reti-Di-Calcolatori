import socket
import signal
import sys
import os
from itertools import groupby

def validator(input: str):
    seed, n_iteration = input.split(",")

    i = n_iteration.find("\\")
    n_iteration = n_iteration[:i]

    if not seed.isdigit() and not len(str(seed)) == 1:
        print("-ERR")
        return 1
    
    if not n_iteration.isdigit():
        print("-ERR")
        return 1
    
    print(f"+OK {n_iteration} iterations on seed {seed}")
    return 0, seed, n_iteration


def look_and_say(iterations, sequence="1"):
    arr = [sequence]

    def get_sequence(arr, iterations, sequence):
        if iterations == 0:
            return arr
        else:
            current = "".join(
                str(len(list(group))) + key for key, group in groupby(sequence)
            )
            arr.append(current)
            get_sequence(arr, iterations - 1, current)
        return arr

    final_sequence = get_sequence(arr, iterations, sequence)
    for f in final_sequence[1:]:
        print(f)


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

                pid = os.fork()

                if pid == 0:  # Processo figlio
                    try:
                        with conn:
                            input = conn.recv(1024).decode()

                            check, seed, niterations = validator(input)
                            
                            if check:
                                raise

                            print(f"DEBUG: Connected by {addr}")
                            look_and_say(int(niterations), sequence=seed)

                        os._exit(0)  # Terminare il processo figlio
                    except Exception as e:
                        print(f"ERROR (child): {e}")
                else:
                    conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()