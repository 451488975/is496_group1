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
import time
import curses
import random
import threading

BUFFER = 1024
HOST = '192.17.61.22'
PORT = int(sys.argv[1])
PLAYERS = []

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
    while len(PLAYERS) < 2:
        player = sock.recvfrom(BUFFER)
        player_addr = player[1]
        PLAYERS.append(player_addr)
        print(f'Player {len(PLAYERS)} has connected!')
    
    for addr in PLAYERS:
        if addr == PLAYERS[0]:
            acknowledgement = socket.htons(0)
            sock.sendto(acknowledgement.to_bytes(2, 'big'), addr)
        else:
            acknowledgement = socket.htons(1)
            sock.sendto(acknowledgement.to_bytes(2, 'big'), addr)
    while True:
        data = sock.recvfrom(BUFFER)
        operation = data[0]
        addr = data[1]
        if addr == PLAYERS[0]:
            sock.sendto(operation, PLAYERS[1])
        else:
            sock.sendto(operation, PLAYERS[0])
