# IS496: Computer Networks (Spring 2022)
# Programming Assignment 2 - Starter Code
# Name and NetId of each member:
# Member 1: River Liu, ll24
# Member 2: Yuxuan Jiang, yj26
# Member 3: Zhizhou Xu, zhizhou6

# Note: 
# This starter code is optional. Feel free to develop your own solution to Part 1. 
# The finished code for Part 1 can also be used for Part 2 of this assignment. 


# Import any necessary libraries below
import sys
import os
import socket
sys.path.append('../')
from utilities import *

# Beginning of Part 1
# Define a buffer size for the message to be read from the TCP socket
BUFFER = 4096


# Initiate socket
# Params: hostname (string), port number (int)
def init_sock(host, port):
    sin = (host, port)

    # Create a datagram socket for TCP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # Bind the socket to address
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(sin)
    except socket.error:
        print('Failed to bind socket.')
        sys.exit()

    # Start listening
    try:
        sock.listen()
    except socket.error:
        print('Failed to listen.')
        sys.exit()

    # Accept the connection and record the address of the client socket
    try:
        conn, addr = sock.accept()
    except socket.error:
        print('Failed to accept.')
        sys.exit()

    return sock, conn, addr


def part1():
    print("********** PART 1 **********")
    # Fill in the IP address of the host and the port number
    host = '192.17.61.22'
    port = 41022
    sock, conn, addr = init_sock(host, port)

    # Receive message from the client
    data = conn.recv(BUFFER)

    # Print the message to the screen
    print('Client Message: ' + data.decode('utf-8'))

    # Send an acknowledgement (e.g., integer of 1) to the client
    conn.send(struct.pack('i', 1))

    # Close the socket
    sock.close()
# End of Part 1


# Beginning of Part 2
# List all the files and directories in current server working directory and send to client
# Params: socket
def ls(conn):
    # Use the shell command 'ls -l' to list the directory at the server, and record the result
    result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)

    # Send the result back to the client
    send_msg(conn, result.stdout)


# Download a file to client
# Params: socket
def dn(conn):
    # receive confirmation from client
    acknowledgement = struct.unpack('i', conn.recv(4))[0]

    if acknowledgement == 1:
        # get file name
        filename = recv_msg(conn)

        # check if file exists
        result = subprocess.run(['ls', '-l', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # file exists
        if result.stdout:
            # get file size and send it to client
            file_size = int(result.stdout.decode('utf-8').split(' ')[4])
            conn.send(struct.pack('i', file_size))

            # get md5 checksum and send to client
            file_md5 = subprocess.run(['md5sum', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # conn.send(file_md5.stdout)
            send_msg(conn, file_md5.stdout)

            # send file
            with open(filename, 'rb') as f:
                for line in f:
                    conn.send(line)

        # file does not exist
        else:
            conn.send(struct.pack('i', -1))


# Upload a file from client
# Params: socket
def up(conn):
    # get file name from client
    filename = recv_msg(conn)

    # check if the file already exists
    check_if_exists(conn, filename)

    # acknowledgement from client
    acknowledgement = struct.unpack('i', conn.recv(4))[0]

    # file exists on client side
    if acknowledgement == 1:
        # receive file size from client
        file_size = struct.unpack('i', conn.recv(4))[0]

        if file_size != -1:
            # send the file
            speed, recv_size, t = send_file(conn, filename, file_size)

            # compute the throughput and send it to client
            tp = '{} bytes have been transferred in {:.6f} seconds: {:.6f} Megabytes/sec'.format(recv_size, t, speed)
            send_msg(conn, tp.encode('utf-8'))

            # send md5 hash to client
            file_md5 = subprocess.run(['md5sum', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            send_msg(conn, file_md5.stdout)


# Remove a file from server
# Params: socket
def rm(conn):
    # get filename
    filename = recv_msg(conn)

    # check if the file exists and send acknowledgement to client
    result = subprocess.run(['ls', '-l', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # file exists
    if result.stdout:
        conn.send(struct.pack('i', 1))

        # get the confirmation from client
        confirm = struct.unpack('i', conn.recv(4))[0]
        if confirm == 1:
            delete = subprocess.run(['rm', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # delete unsuccessfully
            if delete.stderr:
                conn.send(struct.pack('i', -1))
            # delete successfully
            else:
                conn.send(struct.pack('i', 1))
    else:
        conn.send(struct.pack('i', -1))


# Make a directory
# Params: socket
def mkdir(conn):
    # receive directory name from client
    dirname = recv_msg(conn)

    # check if the directory exists and send acknowledgement to client
    result = subprocess.run(['ls', '-l', dirname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # directory exists
    if result.stdout:
        conn.send(struct.pack('i', -2))
    else:
        # mkdir directory
        subprocess.run(['mkdir', dirname])
        check_if_exists(conn, dirname)


# Remove a directory
# Params: socket
def rmdir(conn):
    # receive directory name from client
    dirname = recv_msg(conn)

    # check if the directory exists and send acknowledgement to client
    result = subprocess.run(['ls', '-l', dirname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # directory exists
    if result.stdout:
        # check if there is file in
        dir_file = subprocess.run(['ls', dirname+'/'], stdout=subprocess.PIPE)
        if dir_file.stdout.decode('utf-8') == "":
            # no file in
            conn.send(struct.pack('i', 1))
            confirm = struct.unpack('i', conn.recv(4))[0]
            if confirm == 1:
                delete = subprocess.run(['rmdir', dirname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # delete unsuccessfully
                if delete.stderr:
                    conn.send(struct.pack('i', -1))
                # delete successfully
                else:
                    conn.send(struct.pack('i', 1))
        else:
            # has files in
            conn.send(struct.pack('i', -2))
    else:
        conn.send(struct.pack('i', -1))


# Change the current working directory
# Params: socket
def cd(conn):
    try:
        # receive directory name from client
        dirname = recv_msg(conn)

        # check if the directory exists and send acknowledgement to client
        result = subprocess.run(['ls', '-l', dirname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.stderr:
            # directory does not exist
            conn.send(struct.pack('i', -2))
        else:
            # change directory
            wd = os.getcwd()
            os.chdir(f'{wd}/{dirname}/')
            conn.send(struct.pack('i', 1))
    except OSError:
        conn.send(struct.pack('i', -1))


# Main function for Part 2
def part2():
    print("********** PART 2 **********")
    # Fill in the IP address of the host and the port number
    host = '192.17.61.22'
    port = int(sys.argv[1])

    while True:
        print(f'Waiting for connections on port {port}')
        try:
            # Establish the connection with the client
            sock, conn, addr = init_sock(host, port)
            print('Connection established.')

            while True:
                # Receive the command from client
                data = conn.recv(BUFFER)
                command = data.decode('utf-8')

                # According to the command, execute certain function
                if command == 'LS':
                    ls(conn)
                elif command == 'QUIT':
                    sock.close()
                    break
                elif command == 'DN':
                    dn(conn)
                elif command == 'UP':
                    up(conn)
                elif command == "RMDIR":
                    rmdir(conn)
                elif command == 'RM':
                    rm(conn)
                elif command == 'MKDIR':
                    mkdir(conn)
                elif command == "CD":
                    cd(conn)

        # Use Ctrl+C to shut down the server
        except KeyboardInterrupt:
            print('Server Shutdown.')
            break
# End of Part 2


if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input. 
    # Otherwise, it will go with function part2() to handle the command line input 
    # as specified in the assignment instruction. 
    if len(sys.argv) == 1:
        part1()
    else:
        part2()
