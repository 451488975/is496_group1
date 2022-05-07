"""
IS496: Computer Networks (Spring 2022)
Mini Project - Online Pong Game
Member 1: River Liu, ll24
Member 2: Yuxuan Jiang, yj26
Member 3: Zhizhou Xu, zhizhou6
"""

# Import Libraries
import socket
import sys

BUFFER = 1024
HOST = '192.17.61.22'
PORT = int(sys.argv[1])
PLAYERS = []


def pong_game(difficulty: float):
    global PLAYERS
    for addr in PLAYERS:
        if addr == PLAYERS[-1]:
            sock.sendto(str(-difficulty).encode('utf-8'), addr)
        elif addr == PLAYERS[-2]:
            sock.sendto(str(difficulty).encode('utf-8'), addr)
    refresh = 0
    while True:
        data = sock.recvfrom(BUFFER)
        operation = data[0]
        addr = data[1]
        if operation.decode('utf-8').lower() in ['easy', 'medium', 'hard']:
            PLAYERS.append(addr)
            if len(PLAYERS) % 2 == 1:
                print('Player 1 has connected!')
                if operation.decode('utf-8').lower() == "easy":
                    refresh = 0.08
                elif operation.decode('utf-8').lower() == "medium":
                    refresh = 0.04
                elif operation.decode('utf-8').lower() == "hard":
                    refresh = 0.02
            else:
                print('Player 2 has connected!')
                if operation.decode('utf-8').lower() == "easy":
                    refresh = (refresh + 0.08) / 2
                elif operation.decode('utf-8').lower() == "medium":
                    refresh = (refresh + 0.04) / 2
                elif operation.decode('utf-8').lower() == "hard":
                    refresh = (refresh + 0.02) / 2
                print('Game started!')
                pong_game(refresh)
        elif (PLAYERS.index(addr) + 1) % 2 == 0:
            sock.sendto(operation, PLAYERS[PLAYERS.index(addr) - 1])
        else:
            sock.sendto(operation, PLAYERS[PLAYERS.index(addr) + 1])


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
    refresh = 0
    while len(PLAYERS) < 2:
        player = sock.recvfrom(BUFFER)
        message = player[0]
        player_addr = player[1]
        PLAYERS.append(player_addr)
        if len(PLAYERS) == 1:
            if message.decode('utf-8').lower() == "easy":
                refresh = 0.08
            elif message.decode('utf-8').lower() == "medium":
                refresh = 0.04
            elif message.decode('utf-8').lower() == "hard":
                refresh = 0.02
        else:
            if message.decode('utf-8').lower() == "easy":
                refresh = (refresh + 0.08) / 2
            elif message.decode('utf-8').lower() == "medium":
                refresh = (refresh + 0.04) / 2
            elif message.decode('utf-8').lower() == "hard":
                refresh = (refresh + 0.02) / 2
        print(f'Player {len(PLAYERS)} has connected!')
    print('Game started!')
    try:
        pong_game(refresh)
    except KeyboardInterrupt:
        print('Server Shutdown.')

    sock.close()
