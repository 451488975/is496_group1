# IS496: Computer Networks (Spring 2022)
# Programming Assignment 3 - Starter Code
# Name and NetId of each member:
# Member 1: River Liu, ll24
# Member 2: Yuxuan Jiang, yj26
# Member 3: Zhizhou Xu, zhizhou6

# Import any necessary libraries below
import socket
import threading
import sys
import struct

# Any global variables
BUFFER = 1024
HOST = '192.17.61.22'
PORT = int(sys.argv[1])
CLIENTS = []
USERNAME = []


def chatroom(conn):
    """
    The thread target function to handle the requests by a user after a socket connection is established.
    Args:
        conn: specific connection with the client
    Returns:
        None
    """
    # Login/register the user
    username = conn.recv(BUFFER).decode('utf-8')
    user_confirm = 0
    USERNAME.append(username)
    with open('users.txt', 'r') as f:
        for line in f:
            user = line.split(' ')

            # User existed, check password
            if user[0] == username:
                conn.send(struct.pack('i', 1))  # send user_existed
                user_confirm = 1
                password = conn.recv(BUFFER).decode('utf-8')
                while password != user[1].replace("\n", ""):
                    conn.send(struct.pack('i', 0))  # send pwd_correct
                    password = conn.recv(BUFFER).decode('utf-8')
                conn.send(struct.pack('i', 1))  # send pwd_correct
                break

    # User not existed, create new user
    if user_confirm == 0:
        conn.send(struct.pack('i', 0))  # send user_existed
        password = conn.recv(BUFFER).decode('utf-8')
        with open('users.txt', 'a') as f:
            f.write(f'\n{username} {password}')
        conn.send(struct.pack('i', 1))  # send pwd_correct

    # Use a loop to handle the operations (i.e., BM, PM, EX)
    while True:
        # Receive command from client
        command = conn.recv(BUFFER).decode('utf-8')

        # According to the command, execute different function
        if command == 'EX':
            index = CLIENTS.index(conn)
            CLIENTS.remove(conn)
            USERNAME.remove(USERNAME[index])
            conn.close()
            break
        elif command == 'BM':
            message = conn.recv(BUFFER)
            broadcast(message, conn)
        elif command == 'PM':
            users = ''
            for user in USERNAME:
                if user != username:
                    users += user + '\n'
            conn.send(users.encode('utf-8'))
            user_len = struct.unpack('i', conn.recv(4))[0]
            user = conn.recv(user_len).decode('utf-8')
            while user not in USERNAME:
                conn.send(struct.pack('i', 0))  # send user_online
                user_len = struct.unpack('i', conn.recv(4))[0]
                user = conn.recv(user_len).decode('utf-8')
            conn.send(struct.pack('i', 1))  # send user_online
            message = conn.recv(BUFFER)
            private_message(message, user)


def broadcast(message, conn):
    for client in CLIENTS:
        if client != conn:
            client.send('\n**** Incoming public message ****:  '.encode('utf-8') + message)


def private_message(message, user):
    index = USERNAME.index(user)
    CLIENTS[index].send('\n**** Incoming private message ****:  '.encode('utf-8') + message)


if __name__ == '__main__':
    # Validate input arguments
    sin = (HOST, PORT)

    # Create a socket in TCP
    try:
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()
    
    # Bind the socket to address
    try:
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind(sin)
    except socket.error:
        print('Failed to bind socket.')
        sys.exit()

    # Start listening
    try:
        serversock.listen()
    except socket.error:
        print('Failed to listen.')
        sys.exit()

    while True:
        print(f"Waiting for connections on port {PORT}")

        try:
            # Handle any incoming connection with TCP
            try:
                c, addr = serversock.accept()
                print('Connection established.')
                CLIENTS.append(c)
            except socket.error:
                print('Failed to accept.')
                sys.exit()

            # Initiate a thread for the connected user
            t1 = threading.Thread(target=chatroom, args=(c,))
            t1.start()

        # User Ctrl+C to shut down the server
        except KeyboardInterrupt:
            print('Server shutdown.')
            break

    # Close server socket
    serversock.close()
