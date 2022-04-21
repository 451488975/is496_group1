# IS496 Group 1 PG2


## Group Members
|     Name     |  NetID   |
|:------------:|:--------:|
|  River Liu   |   ll24   |
|  Zhizhou Xu  | zhizhou6 |


## Introduction
This is a simple chatroom application using TCP connection. The application is able to establish multiple TCP
connections between server and clients, then allow clients to do the following operations:
* Broadcast Messaging
* Private Messaging
* Exit

Before running the scripts, please set up the server in Student Machine 'student00'.


## List of files
    /server
        - chatserver.py
        - users.txt
    /client
        - chatclient.py


## Application
To run the application, after entering the server/client subdirectory, run following command lines to establish the TCP
connection

**Server (`student00`)**

`[netid@is-student00 ~/server] $ python3 chatserver.py [port]`

You should see prompts below on server side if the server is set up successfully:

    Waiting for connections on port [port]

**Client (`student01/02/03`)**

`[netid@is-student01 ~/client] $ python3 chatclient.py student00.ischool.illinois.edu [port] [Username]`

The prompts on server side should be updated to:

    Waiting for connections on port [port]
    Connection established.

You should see prompts below on client side if the connection is established and `[Username]` is existed on server:

    Existing user
    Enter password:

Or, if `[Username]` is not existed on server:

    Creating new user
    Enter password:

Then, users from client should enter the password. For new users, server will save the username and password to 
`users.txt`, and for old users, server will check if the password is matching the username.

Afterwards, users can do operations below to use the chatroom:

### 1. Broadcast Messaging
Users can broadcast a message to all the online users by:

    BM

Then, enter the message content user wants

    >Enter the public message: [message]

Example:

    >Enter the public message: Hi everyone!

The `[message]` will send to all clients online except the sender by the server, format like:

    **** Incoming public message ****:  [message]

Sender will receive a confirmation prompt like:

    Public message sent.

### 2. Private Messaging
Users can send private message to specific online user by:

    PM

Server will prompt all users online, and ask the sender whom to receive the message:

    Peers Online:
    [User1]
    [User2]

    >Peer to message: [receiver ([User1] or [User2])]

Sender types the `[receiver]` in to the terminal, and client would ask for the message content:

    >Enter the private message:[message]

The `[message]` will send to the `[receiver]` client by the server, format like:

    **** Incoming private message ****:  [message]

Sender will receive a confirmation prompt like:

    Private message sent.

### 3. Exit
Users can close the connection to server using command

    EX

To shut down the server, please use `Ctrl + C` on keyboard to terminate the server.