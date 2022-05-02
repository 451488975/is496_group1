"""
IS496: Computer Networks (Spring 2022)
Mini Project - Online Pong Game
Member 1: River Liu, ll24
Member 2: Yuxuan Jiang, yj26
Member 3: Zhizhou Xu, zhizhou6 11
"""

# Import Libraries
import socket
import sys

BUFFER = 1024
HOST = '192.17.61.22'
PORT = int(sys.argv[1])
WAITING_USER = []


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

    while True:
        print('Waiting...')
