import struct
import time
import subprocess


# send length of message followed by the message
# Params: socket, msg (byte)
def send_msg(sock, msg):
    len_msg = len(msg)
    sock.send(struct.pack('i', len_msg))
    sock.send(msg)


# receive length of message followed by the message
# Params: socket
# Return: message (string)
def recv_msg(sock):
    len_msg = struct.unpack('i', sock.recv(4))[0]
    msg = sock.recv(len_msg).decode('utf-8')
    return msg


# send file to the other end
# Params: socket, file name (string), file size (int)
# Return: transfer speed (float), received size (int), transfer time (float)
def send_file(sock, filename, file_size):
    f = open(filename, 'wb')
    recv_size = 0

    # start time
    start = time.time()

    # receiving file
    while recv_size < file_size:
        data = sock.recv(4096)
        f.write(data)
        recv_size += len(data)

    # end time
    end = time.time()
    t = end - start

    # speed
    speed = recv_size / 1000000 / t

    f.close()
    return speed, recv_size, t


# check if file or directory is existed on this side
# Params: socket, name of file or directory (string)
def check_if_exists(conn, name):
    result = subprocess.run(['ls', '-l', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        conn.send(struct.pack('i', 1))
    else:
        conn.send(struct.pack('i', -1))