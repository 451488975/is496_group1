# IS496: Computer Networks (Spring 2022)
# Programming Assignment 3 - Starter Code
# Name and NetId of each member:
# Member 1: River Liu, ll24
# Member 2: Yuxuan Jiang, yj26
# Member 3: Zhizhou Xu, zhizhou6

# Note: 
# This starter code is optional. Feel free to develop your own solution. 


# Import any necessary libraries below
import socket
import threading
import sys, os, struct

# Any global variables
BUFFER = 1024
HOST = '192.17.61.22'
PORT = int(sys.argv[1])


"""
The thread target function to handle the requests by a user after a socket connection is established.
Args:
    args: any arguments to be passed to the thread
Returns:
    None
"""
def chatroom (conn):
    # Login/register the user
    username = conn.recv(BUFFER).decode('utf-8')
    user_confirm = 0
    with open('users.txt', 'r') as f:
        for line in f:
            user = line.split(' ')

            # User existed, check password
            if user[0] == username:
                conn.send(struct.pack('i', 1)) # send user_existed
                user_confirm = 1
                password = conn.recv(BUFFER).decode('utf-8')
                while password != user[1]:
                    conn.send(struct.pack('i', 0)) # send pwd_correct
                    password = conn.recv(BUFFER).decode('utf-8')
                conn.send(struct.pack('i', 1)) # send pwd_correct
                break

    # User not existed, create new user
    if user_confirm == 0:
        conn.send(struct.pack('i', 0)) # send user_existed
        password = conn.recv(BUFFER).decode('utf-8')
        with open('users.txt', 'a') as f:
            f.write(f'\n{username} {password}')
        conn.send(struct.pack('i', 1))  # send pwd_correct

    # TODO: Use a loop to handle the operations (i.e., BM, PM, EX)
    while True:
        # Receive command from client
        data = conn.recv(BUFFER).decode('utf-8').split(':')
        command = data[1]

        # According to the command, execute different function
        if command == 'EX':
            conn.close()
            break


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
            except socket.error:
                print('Failed to accept.')
                sys.exit()

            # TODO: initiate a thread for the connected user
            t1 = threading.Thread(target=chatroom, args=(c,))
            t1.start()

        # User Ctrl+C to shut down the server
        except KeyboardInterrupt:
            print('Server shutdown.')
            break

    # Close server socket
    serversock.close()