"""
IS496: Computer Networks (Spring 2022)
Mini Project - Online Pong Game
Member 1: River Liu, ll24
Member 2: Yuxuan Jiang, yj26
Member 3: Zhizhou Xu, zhizhou6 11
"""

# Import Libraries
from encodings import utf_8
import socket
import sys
import threading

BUFFER = 1024
HOST = '192.17.61.22'
PORT = 41002
CLIENTS = []


if __name__ == '__main__':
    sin = (HOST, PORT)

    # Create a socket in UDP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # Bind the socket to address
    try:
        sock.bind(sin)
    except socket.error:
        print('Failed to bind socket.')
        sys.exit()

    print('Waiting...')
    while len(CLIENTS)<2:
        client = sock.recvfrom(BUFFER)
        cli_addr = client[1]
        CLIENTS.append(cli_addr)
        print(f'Client {len(CLIENTS)} has connected...')

    for user in CLIENTS:
        if user == CLIENTS[0]:
            acknowledge = socket.htons(0)
            sock.sendto(acknowledge.to_bytes(2,'big'),user)
        else:
            acknowledge = socket.htons(1)
            sock.sendto(acknowledge.to_bytes(2,'big'),user)
    while True:
        data = sock.recvfrom(BUFFER)
        operation = data[0]
        user = data[1]
        # If the received operation is from client1
        if user == CLIENTS[0]:
            sock.sendto(operation,CLIENTS[1])   #The server forwards the operation to client2
        # If the received operation is from client2
        else:
            sock.sendto(operation,CLIENTS[0])   #If the received operation is from client2

