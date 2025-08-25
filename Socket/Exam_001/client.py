#!/usr/bin/env python3
import socket
import os
import sys
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 2525       # Port to connect to


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    hostname = socket.gethostname()
    print('DEBUG - Connected to server:', hostname)

    s.send(f'Welcome from {hostname}'.encode('utf-8'))
    response = s.recv(1024).decode('utf-8')
    print('DEBUG - Received from server:', response)

    s.close()