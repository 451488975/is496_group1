# IS496: Computer Networks (Spring 2022)
# Programming Assignment 1
# Name and NetId of each member:
# Member 1: River Liu, ll24
# Member 2: Yuxuan Jiang, yj26
# Member 3: Zhizhou Xu, zhizhou6

# Import any necessary libraries below
import socket
import sys
from pg1lib import *

# Beginning of Part 1
# Define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


def init_sock(host, port):
    sin = (host, port)

    # Create a datagram socket
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

    return sock


def part1():
    print("********** PART 1 **********")
    # Fill in the IP address of the host and the port number
    host = '192.17.61.22'
    port = 41022
    sock = init_sock(host, port)

    print("Waiting ...")

    # Receive message from the client and record the address of the client socket
    while True:
        data = sock.recvfrom(BUFFER)
        message = data[0]
        address = data[1]

    # Convert the message from byte to string and print it to the screen
        str_message = message.decode('utf-8')
        print('Client Message: ' + str_message)

    # 1. Convert the acknowledgement (e.g., integer of 1) from host-byte order to network-byte order
    # 2. Send the converted acknowledgement to the client
        acknowledgement = socket.htons(1)
        sock.sendto(acknowledgement.to_bytes(2, 'big'), address)

    # Close the socket
        break
    sock.close()
# End of Part 1


# Beginning of Part 2
def part2(argv):
    print("********** PART 2 **********")
    # Fill in the IP address of the host and the port number
    host = '192.17.61.22'
    port = int(argv[1])
    sock = init_sock(host, port)

    pubkey_server = get_pub_key()

    # Receive message from the client and record the address of the client socket
    while True:
        print("Waiting ...")
        try:
            data = sock.recvfrom(BUFFER)
            pubkey_client = data[0]
            address = data[1]

            # Encrypt public key of Server
            pubkey_server_e = encrypt(pubkey_server, pubkey_client)
            sock.sendto(pubkey_server_e, address)

            # Receive messages and checksum from Client
            message_e = sock.recvfrom(BUFFER)
            r_checksum = sock.recvfrom(BUFFER)

            message = decrypt(message_e[0])
            cal_checksum = checksum(message)

            # Convert the message from byte to string and print it to the screen
            str_message = message.decode('utf-8')
            r_checksum_int = int(r_checksum[0].decode('utf-8'))
            print("********** NEW MESSAGE **********")
            print('Received Message: ' + str_message)
            print('Received Client Checksum:', r_checksum_int)
            print('Calculated Checksum:', cal_checksum)

            # 1. convert the acknowledgement (e.g., integer of 1) from host-byte order to network-byte order
            # 2. send the converted acknowledgement to the client
            if cal_checksum == r_checksum_int:
                acknowledgement = socket.htons(1)
                sock.sendto(acknowledgement.to_bytes(2, 'big'), address)
            else:
                acknowledgement = socket.htons(0)
                sock.sendto(acknowledgement.to_bytes(2, 'big'), address)
        except KeyboardInterrupt:
            print("Server Shutdown.")
            sock.close()
            break
# End of Part 2


if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input.
    # Otherwise, it will go with function part2() to handle the command line input
    # as specified in the assignment instruction.
    if len(sys.argv) == 1:
        part1()
    else:
        part2(sys.argv)
