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
HOSTNAME = sys.argv[1]
PORT = int(sys.argv[2])


if __name__ == '__main__':
    # Get host IP using hostname
    try:
        host = socket.gethostbyname(HOSTNAME)
    except socket.error:
        print('Failed to resolve hostname.')
        sys.exit()

    sin = (host, PORT)

    # Create a socket in UDP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()
