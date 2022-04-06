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
BUFFER = 




"""
The thread target fuction to handle the requests by a user after a socket connection is established.
Args:
    args:  any arguments to be passed to the thread
Returns:
    None
"""
def chatroom (args):
    # Task1: login/register the user
   

    # Task2: use a loop to handle the operations (i.e., BM, PM, EX)
    





if __name__ == '__main__':
    # TODO: Validate input arguments
   

    # TODO: create a socket in UDP or TCP
    try:

    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()
    
    # TODO: Bind the socket to address
    try:
        serversock.bind(('', PORT))
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()


    while True:
        print(f"Waiting for connections on port {PORT}")

        # TODO: handle any incoming connection with UDP or TCP


        # TODO: initiate a thread for the connected user
        
       





