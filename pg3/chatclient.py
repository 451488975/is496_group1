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




"""
The thread target fuction to handle any incoming message from the server.
Args:
    None
Returns:
    None
Hint: you can use the first character of the message to distinguish different types of message
"""
def accept_messages():
    





if __name__ == '__main__': 
    # TODO: Validate input arguments
    


    # TODO: create a socket with UDP or TCP, and connect to the server
    try:
        
    except socket.error as msg:
        print(f'Failed to create socket. Error Code : {str(msg[0])}\n Message: {msg[1]}')
        sys.exit()
    

    
    # TODO: Send username to the server and login/register the user
    


    # TODO: initiate a thread for receiving message
    


    # TODO: use a loop to handle the operations (i.e., BM, PM, EX)
    

