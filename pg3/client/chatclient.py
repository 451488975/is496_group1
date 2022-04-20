# IS496: Computer Networks (Spring 2022)
# Programming Assignment 3 - Starter Code
# Name and NetId of each member:
# Member 1: River Liu, ll24
# Member 2: Yuxuan Jiang, yj26
# Member 3: Zhizhou Xu, zhizhou6

# Note: 
# This starter code is optional. Feel free to develop your own solution. 


# Import any necessary libraries below
from email import message
import socket
import threading
import sys, os, struct

# Any global variables
BUFFER = 1024
HOSTNAME = sys.argv[1]
PORT = int(sys.argv[2])
USERNAME = sys.argv[3]
FLAG = 0


"""
The thread target function to handle any incoming message from the server.
Args:
    None
Returns:
    None
Hint: you can use the first character of the message to distinguish different types of message
"""
def accept_messages(sock):
    while True:
        try:
            message = sock.recv(BUFFER).decode('utf-8')
            if FLAG == 0:
                print(message + '\n')
                print('>Please enter a command (BM: Broadcast Messaging, PM: Private Messaging, EX: Exit')
            elif FLAG == 1:
                print(message + '\n')
                print('>Enter the public message: ')
            elif FLAG == 2:
                print(message + '\n')
                print('>Enter the private message: ')
        except:
            sock.close()
            break
    


if __name__ == '__main__':
    # Validate input arguments
    try:
        host = socket.gethostbyname(HOSTNAME)
    except socket.error:
        print('Failed to resolve hostname.')
        sys.exit()

    sin = (host, PORT)

    # Create a socket with UDP or TCP, and connect to the server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print(f'Failed to create socket. Error Code : {str(msg[0])}\n Message: {msg[1]}')
        sys.exit()

    try:
        sock.connect(sin)
    except socket.error:
        print('Failed to connect.')
        sys.exit()

    # Send username to the server and login/register the user
    sock.send(USERNAME.encode('utf-8'))

    user_existed = struct.unpack('i', sock.recv(4))[0]
    if user_existed == 1:
        print('Existing user')
    else:
        print('Creating new user')

    password = input('Enter password: ')
    sock.send(password.encode('utf-8'))
    pwd_correct = struct.unpack('i', sock.recv(4))[0]
    while pwd_correct == 0:
        password = input('Incorrect password. Please enter again: ')
        sock.send(password.encode('utf-8'))
        pwd_correct = struct.unpack('i', sock.recv(4))[0]

    # TODO: initiate a thread for receiving message
    t1 = threading.Thread(target=accept_messages, args=(sock,)) 
    t1.start()

    while True:
        # Wait for user to input command
        print('>Please enter a command (BM: Broadcast Messaging, PM: Private Messaging, EX: Exit')
        command = input()
        data = 'C:' + command # Add 'C' to indicate this command message

        # Send command to server
        sock.send(data.encode('utf-8'))

        # According to the command, execute different function
        if command == 'EX':
            print('Bye!')
            sock.close()
            break
        elif command == 'BM':
            FLAG = 1
            message = input('>Enter the public message: \n')
            sock.send(message.encode('utf-8'))
            FLAG = 0
        elif command == 'PM':
            print('Online users currently:')
            users = sock.recv(BUFFER).decode('utf-8')
            print(users)
            user = input('>Please select a user to contact: ')
            user_len = len(user.encode('utf-8'))
            sock.send(struct.pack('i', user_len))
            sock.send(user.encode('utf-8'))
            user_online = struct.unpack('i', sock.recv(4))[0]
            while user_online == 0:
                user = input('>' + user + 'is not online, please select an online user: ')
                user_len = len(user.encode('utf-8'))
                sock.send(struct.pack('i', user_len))
                sock.send(user.encode('utf-8'))
            FLAG = 2
            message = input('>Enter the private message: \n')
            sock.send(message.encode('utf-8'))
            FLAG = 0