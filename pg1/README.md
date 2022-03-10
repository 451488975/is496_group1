# IS496 Group1 PG1


## Group Members
|     Name     |  NetID   |
|:------------:|:--------:|
|  River Liu   |   ll24   |
| Yuxuan Jiang |   yj26   |
|  Zhizhou Xu  | zhizhou6 |


## Introduction
This program is a simple UDP program. In part 1, the program will establish a simple UDP connection between server and
client. In part 2, the program will establish a simple secure UDP connection accepting arguments for hostname, port, and
the message you want to send from client to the server.

Before running the scripts, please put `udpserver.py` in Student Machine `student00`.


## Part 1
To run part 1, after entering the directory with all the scripts, run following command lines to establish the UDP
connection

**Server (`student00`)**

`[netid@is-student00 ~] $ python3 udpserver.py`

**Client (`student01/02/03`)**

`[netid@is-student01 ~] $ python3 udpclient.py`

The server will shut down itself after it received the message from the client for part 1.


## Part 2
To run part 2, after entering the directory with all the scripts, run following command lines to establish the secure 
UDP connection

**Server (`student00`)**

`[netid@is-student00 ~] $ python3 udpserver.py [port]`

**Client (`student01/02/03`)**

`[netid@is-student01 ~] $ python3 udpclient.py [hostname] [port] [test message]`

To shut down the server, please use `Ctrl + C` on keyboard to terminate the server.
