#!/usr/bin/env python3 
import socket
import os
import sys
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080         # Port to listen on (non-privileged ports are > 1023)


# main
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    # non-parallel version:
    # conn, addr = s.accept()
    # print('DEBUG - Connected by', addr)
    # ...
    # conn.close()

    # single-request version:
    # while True:
    #     conn, addr = s.accept()
    #     print('DEBUG - Connected by', addr)
    #     ...
    #     conn.close()

    # fork version:
    while True:
        conn, addr = s.accept()
        print('DEBUG - Connected by', addr)
        child_pid = os.fork()
        if child_pid == 0:
            

            #...
            
            conn.close()
            exit()
        else:
            conn.close()