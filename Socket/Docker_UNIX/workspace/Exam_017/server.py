import socket
import signal
import sys
import struct

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
                
                    message = conn.recv(1024)
                    if not message:
                        continue

                    length = struct.unpack("!B", message[:1])[0]
                    records = message[1:]

                    records_unpacked = []
                    for i in range(0, len(records), 5):
                        records_unpacked.append(struct.unpack("!B", records[i:i+1])[0])
                        records_unpacked.append(struct.unpack("!f", records[i+1:i+5])[0] )
                    
                    print("Inizio raggruppamento: ", records_unpacked, "lengt: ", length)
                    records_list = [[]]
                    for i in range(1, length+1):
                        records_list.append([])
                        print(records_list)
                        print("Raggruppamento numero: ", i)
                        for j in range(0, len(records_unpacked), 2):
                            print("Record type: ", records_unpacked[j])
                            if i == records_unpacked[j]:
                                print("Record to append: ", records_unpacked[j+1])
                                
                                records_list[i].append(records_unpacked[j+1])

                    print(records_list)

                    response = ""
                    for i in range(length):
                        response += f"Tipo {str(i+1)}: {str(sum(records_list[i+1]) / len(records_list[i+1]))}\n" 
                        
                    conn.sendall(response.encode('utf-8'))
                    
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    server()