# IS496: Computer Networks (Spring 2022)
# Programming Assignment 1
# Name and NetId of each member:
# Member 1: River Liu, ll24
# Member 2: Yuxuan Jiang, yj26
# Member 3: Zhizhou Xu, zhizhou6


# Import any necessary libraries below
import socket
import sys, time
from pg1lib import *


############## Beginning of Part 1 ##############
# Define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


def part1 ():
    print("********** PART 1 **********")
    # Fill in the hostname and port number
    hostname = 'student00.ischool.illinois.edu'
    port = 41022

    # A dummy message (in bytes) to test the code
    message = b"Hello World"

    # Convert the host name to the corresponding IP address
    host = socket.gethostbyname(hostname)
    sin = (host, port)

    # Create a datagram socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # Convert the message from string to byte and send it to the server
    sock.sendto(message, sin)

    # 1. Receive the acknowledgement from the server
    # 2. Convert it from network-byte order to host-byte order
    data = sock.recvfrom(BUFFER)
    acknowledgement = socket.ntohs(int.from_bytes(data[0], 'big'))

    # Print the acknowledgement to the screen
    print('Acknowledgement: {}'.format(acknowledgement))

    # Close the socket
    sock.close()


############## End of Part 1 ##############




############## Beginning of Part 2 ##############
# Note: any functions/variables for Part 2 will go here


def part2 (argv):
    print("********** PART 2 **********")
    # Fill in the hostname and port number
    hostname = argv[1]
    port = int(argv[2])

    # A message (in bytes) passed from arguments
    message_raw = bytes(argv[3], encoding="utf-8")

    # Convert the host name to the corresponding IP address
    try:
        host = socket.gethostbyname(hostname)
    except socket.error:
        print('Failed to resolve hostname.')
        sys.exit()

    sin = (host, port)

    pubkey = getPubKey()

    # Create a datagram socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # Client send its public key to Server and get public key of Server
    sock.sendto(pubkey, sin)
    pubkey_server_data = sock.recvfrom(BUFFER)
    pubkey_server_e = pubkey_server_data[0]
    pubkey_server = decrypt(pubkey_server_e)

    # Encrypt the message and generate the checksum
    message = encrypt(message_raw, pubkey_server)
    checksum_int = checksum(message_raw)
    checksum_b = bytes(str(checksum_int), encoding='utf8')

    # Convert the message from string to byte and send it to the server
    start = int(time.time() * 1000000)
    sock.sendto(message, sin)
    sock.sendto(checksum_b, sin)
    print('Checksum Sent: ', checksum_int)

    # 1. receive the acknowledgement from the server
    # 2. convert it from network-byte order to host-byte order
    data = sock.recvfrom(BUFFER)
    end = int(time.time() * 1000000)
    acknowledgement = socket.ntohs(int.from_bytes(data[0], 'big'))
    if acknowledgement == 1:
        print('Server has successfully received the message!')
    else:
        print('Server has not successfully received the message!')

    print('RTT: ', end - start, 'us')

    # Close the socket
    sock.close()


############## End of Part 2 ##############


if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input.
    # Otherwise, it will go with function part2() to handle the command line input
    # as specified in the assignment instruction.
    if len(sys.argv) == 1:
        part1()
    else:
        part2(sys.argv)