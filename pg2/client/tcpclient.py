# IS496: Computer Networks (Spring 2022)
# Programming Assignment 2 - Starter Code
# Name and NetId of each member:
# Member 1: River Liu, ll24
# Member 2: Yuxuan Jiang, yj26
# Member 3: Zhizhou Xu, zhizhou6

# Import any necessary libraries below
import sys
import socket
sys.path.append('../')
from utilities import *

# Beginning of Part 1
# define a buffer size for the message to be read from the TCP socket
BUFFER = 4096


# Initiate socket
# Params: hostname (string), port number (int)
def init_sock(host, port):
    sin = (host, port)

    # create a datagram socket for TCP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # connect to the server
    try:
        sock.connect(sin)
    except socket.error:
        print('Failed to connect.')
        sys.exit()

    return sock


def part1():
    # fill in the hostname and port number
    hostname = 'student00.ischool.illinois.edu'
    port = 41022

    # A dummy message (in bytes) to test the code
    message = b'Hello World'

    # convert the host name to the corresponding IP address
    host = socket.gethostbyname(hostname)
    sock = init_sock(host, port)

    # send the message to the server
    sock.send(message)

    # receive the acknowledgement from the server
    acknowledgement = struct.unpack('i', sock.recv(BUFFER))[0]

    # print the acknowledgement to the screen
    print(f'Acknowledgement: {acknowledgement}')

    # close the socket
    sock.close()


# End of Part 1


# Beginning of Part 2
# List all the files and directories in current server working directory
# Params: socket
def ls(sock):
    print(recv_msg(sock))


# Download file from server
# Params: socket, file name (string)
def dn(sock, filename):
    # check if the file already exists
    result = subprocess.run(['ls', '-l', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # file exists
    if result.stdout:
        # ask user if to overwrite the file
        confirm = input('File already exists. Do you want to overwrite the original file? ')
        confirm = confirm.lower()

        if confirm == 'no':
            # send a negative confirmation to server
            sock.send(struct.pack('i', -1))
            print('Download abandoned by user!')
            return
        elif confirm != 'yes':
            # send a negative confirmation to server
            sock.send(struct.pack('i', -1))
            print('Failed to resolve command.')
            return

    # file does not exist
    # send a positive confirmation to server
    sock.send(struct.pack('i', 1))

    # send file name to server
    send_msg(sock, filename.encode('utf-8'))

    # get file size from server and file name from command
    file_size = struct.unpack('i', sock.recv(4))[0]

    # file exists on server side
    if file_size != -1:
        # get md5 checksum from server
        md5_value = recv_msg(sock)

        speed, recv_size, t = send_file(sock, filename, file_size)

        # print throughput
        print('{} bytes have been transferred in {:.6f} seconds: {:.6f} Megabytes/sec'.format(recv_size, t, speed))

        # compare md5 hash
        file_md5 = subprocess.run(['md5sum', filename], stdout=subprocess.PIPE)
        if file_md5.stdout.decode('utf-8') == md5_value:
            print(f'File downloaded successfully! MD5: {md5_value.split()[0]}')
        else:
            print('File corrupted! Please try download the file again!')

    # file does not exist on server side
    else:
        print('File does not exist!')


# Upload file to server
# Params: socket, file name (string)
def up(sock, filename):
    # send file name to server
    send_msg(sock, filename.encode('utf-8'))

    # receive acknowledgement from server
    acknowledgement = struct.unpack('i', sock.recv(4))[0]

    # file exists on server side
    if acknowledgement == 1:
        # ask user if to overwrite the file
        confirm = input('File already exists. Do you want to overwrite the original file? ')
        confirm = confirm.lower()

        if confirm == 'no':
            # send a negative confirmation to server
            sock.send(struct.pack('i', -1))
            print('Upload abandoned by user!')
            return
        elif confirm != 'yes':
            # send a negative confirmation to server
            sock.send(struct.pack('i', -1))
            print('Failed to resolve command.')
            return

    # check if the file exists and send acknowledgement to client
    result = subprocess.run(['ls', '-l', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # file exists
    if result.stdout:
        # send a confirmation to server
        sock.send(struct.pack('i', 1))

        # file does not exist on server side
        # get the size of this file
        file_size = int(result.stdout.decode('utf-8').split(' ')[4])

        # send file size to server
        sock.send(struct.pack('i', file_size))

        # get md5 checksum
        file_md5 = subprocess.run(['md5sum', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # send file
        with open(filename, 'rb') as f:
            for line in f:
                sock.send(line)

        # print throughput
        throughput = recv_msg(sock)
        print(throughput)

        # compare md5 hash
        md5_value = recv_msg(sock)
        if md5_value == file_md5.stdout.decode('utf-8'):
            print(f'File uploaded successfully! MD5: {md5_value.split()[0]}')
        else:
            print('File corrupted! Please try upload the file again!')
    else:
        # send a negative confirmation to server
        sock.send(struct.pack('i', -1))
        print('File does not exist!')


# Remove file from server
# Params: socket, file name (string)
def rm(sock, filename):
    # send file name to server
    send_msg(sock, filename.encode('utf-8'))

    # check if the file exists
    acknowledgement = struct.unpack('i', sock.recv(4))[0]

    # file exists
    if acknowledgement == 1:
        # ask user delete the file or not
        confirm = input('Are you sure? ')
        confirm = confirm.lower()

        if confirm == 'yes':
            # send confirmation to server
            sock.send(struct.pack('i', 1))

            # acknowledgement from server
            delete = struct.unpack('i', sock.recv(4))[0]

            # delete successfully
            if delete == 1:
                print('File deleted.')

            # delete unsuccessfully
            else:
                print('Unable to delete the file!')
        else:
            sock.send(struct.pack('i', -1))
            print('Delete abandoned by the user!')

    # file does not exist
    else:
        print('File does not exist!')


# Make directory on server
# Params: socket, directory name (string)
def mkdir(sock, dirname):
    # send directory name to server
    send_msg(sock, dirname.encode('utf-8'))

    acknowledgement = struct.unpack('i', sock.recv(4))[0]
    if acknowledgement == 1:
        print("The directory was successfully made")
    elif acknowledgement == -2:
        print("The directory already exists on server")
    else:
        print("Failed to make directory")


# Remove directory from server
# Params: socket, directory name (string)
def rmdir(sock, dirname):
    # send directory name to server
    send_msg(sock, dirname.encode('utf-8'))

    acknowledgement = struct.unpack('i', sock.recv(4))[0]
    if acknowledgement == 1:
        # ask user delete the directory or not
        confirm = input('Are you sure? ')
        confirm = confirm.lower()

        if confirm == 'yes':
            # send confirmation to server
            sock.send(struct.pack('i', 1))

            # acknowledgement from server
            delete = struct.unpack('i', sock.recv(4))[0]

            # delete successfully
            if delete == 1:
                print('Directory deleted.')
            # delete unsuccessfully
            else:
                print('Failed to delete directory.')
        else:
            sock.send(struct.pack('i', -1))
            print('Delete abandoned by the user!')
    elif acknowledgement == -2:
        print("The directory is not empty")
    else:
        print("The directory does not exist on server")


# Change current working directory
# Params: socket, directory name (string)
def cd(sock, dirname):
    # send directory name to server
    send_msg(sock, dirname.encode('utf-8'))

    acknowledgement = struct.unpack('i', sock.recv(4))[0]
    if acknowledgement == 1:
        print("Changed current directory")
    elif acknowledgement == -2:
        print("The directory does not exist on server")
    else:
        print("Failed to change directory!")


# Main function for Part 2
def part2():
    print("********** PART 2 **********")

    # fill in the hostname and port number
    hostname = sys.argv[1]
    port = int(sys.argv[2])

    # convert the host name to the corresponding IP address
    try:
        host = socket.gethostbyname(hostname)
    except socket.error:
        print('Failed to resolve hostname.')
        sys.exit()

    # Initiate the socket and connect to the server
    sock = init_sock(host, port)
    print('Connection established')

    while True:
        # Waiting for user to prompt command
        user_input = input('> ').split(' ')
        command = user_input[0]
        name = ''
        if len(user_input) > 1:
            name = user_input[1]
        command_byte = command.encode('utf-8')

        # Send the command to the server in byte
        sock.send(command_byte)

        # According to the command, print different results.
        if command == 'LS':
            ls(sock)
        elif command == 'QUIT':
            sock.close()
            break
        elif command == 'DN':
            dn(sock, name)
        elif command == 'UP':
            up(sock, name)
        elif command == "RMDIR":
            rmdir(sock, name)
        elif command == 'RM':
            rm(sock, name)
        elif command == 'MKDIR':
            mkdir(sock, name)
        elif command == "CD":
            cd(sock, name)
        else:
            print('Failed to resolve command.')


# End of Part 2


if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input. 
    # Otherwise, it will go with function part2() to handle the command line input 
    # as specified in the assignment instruction. 
    if len(sys.argv) == 1:
        part1()
    else:
        part2()
