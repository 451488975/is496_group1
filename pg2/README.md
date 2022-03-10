# IS496 Group 1 PG2


## Group Members
|     Name     |  NetID   |
|:------------:|:--------:|
|  River Liu   |   ll24   |
| Yuxuan Jiang |   yj26   |
|  Zhizhou Xu  | zhizhou6 |


## Introduction
This is a simple FTP application using TCP connection. In part 1, the application will test the ability to connect 
the server and the client using TCP. In part 2, The application will establish a TCP connection between server and 
client, then allow client to do the following operations:
* Download a file from server
* Upload a file to server
* Remove a file from server
* List all the files and directories on server
* Make directory on server
* Remove a directory from server
* Change the current working directory on server
* Close the connection to server

Before running the scripts, please set up the server in Student Machine 'student00'.


## List of files
    /server
        - tcpserver.py
        - TestFile.txt
    /client
        - tcpclient.py
        - upload.txt
    - utilities.py


## Part 1
To run part 1, after entering the server/client subdirectory, run following command lines to establish the TCP
connection

**Server (`student00`)**

`[netid@is-student00 ~/server] $ python3 tcpserver.py`

**Client (`student01/02/03`)**

`[netid@is-student01 ~/client] $ python3 tcpclient.py`

The server will shut down itself after it received the message from the client for part 1.


## Part 2
To run part 2, after entering the server/client subdirectory, run following command lines to establish the TCP
connection

**Server (`student00`)**

`[netid@is-student00 ~/server] $ python3 tcpserver.py [port]`

You should see prompts below on server side if the server is set up successfully:

    ********** PART 2 **********
    Waiting for connections on port [port]

**Client (`student01/02/03`)**

`[netid@is-student01 ~/client] $ python3 tcpclient.py student00.ischool.illinois.edu [port]`

You should see prompts below on client side if the client is connected to the server:

    ********** PART 2 **********
    Connection established
    > 

The prompts on server side should be updated to:

    ********** PART 2 **********
    Waiting for connections on port [port]
    Connection established.

Then, users from client can do operations below to use the FTP:

### 1. Download a file from server
Users can download a file with name as `[filename]`from server using command

    DN [filename]

Example:

    DN TestFile.txt

If the current working directory on client side has a file with the same name, the app will ask if user wants to 
overwrite the existing file. Type `Yes` to overwrite, or `No` to abandon the process.

After the downloading is complete, the app will print the file size and the downloading speed of the current process.
Also, the app will compare the MD5 hash with the server to make sure the data integrity of the downloaded file. If the
MD5 hash is matched, the app will print the confirmation message with the MD5 hash. Otherwise, the app will print
the message to ask the user to download the file again.

### 2. Upload a file to server
Users can upload a file with name as `[filename]` to server using command

    UP [filename]

Example:

    UP upload.txt

If the current working directory on server side has a file with the same name, the app will ask if user wants to 
overwrite the existing file. Type `Yes` to overwrite, or `No` to abandon the process.

After the uploading is complete, the app will print the file size and the uploading speed of the current process.
Also, the app will compare the MD5 hash with the server to make sure the data integrity of the uploaded file. If the
MD5 hash is matched, the app will print the confirmation message with the MD5 hash. Otherwise, the app will print
the message to ask the user to upload the file again.

### 3. Remove a file on server
Users can remove a file with name as `[filename]` from server using command

    RM [filename]

Example:

    RM TestFile.txt

The app will prompt user a message to make sure if user wants to remove the file or not. Type `Yes` to remove the file 
, or type `No` to abandon the process.

### 4. List all the files and directories on server
Users can list all the files and directories in current working directory on server using command

    LS

### 5. Make a directory on server
User can make a new directory with name as `[dirname]` on server using command

    MKDIR [dirname]

Example:

    MKDIR testdir

After the app tried to make the directory, it will give a confirmation message to the user with result of succeeded, 
existed directory name, or failed

### 6. Remove a directory on server
Users can remove a directory with name as `[dirname]` on server using command

    RMDIR [dirname]

If the directory is not empty or does not exist on server, the app will inform users with error prompts. If the 
directory is eligible for deletion, the app will prompt user a message to make sure if user wants to remove the 
directory or not. Type `Yes` to remove the directory, or type `No` to abandon the process.

### 7. Change the current working directory on server
Users can change the current working directory to path as `[path]` on server using command

    CD [path]

After the app tried to change the directory, it will give a confirmation message to the user with result of succeeded, 
non-existed path, or failed

### 8. Close the connection to server
Users can close the connection to server using command

    QUIT


## Extra

The app integrated the function to check MD5 hash, and compare between server and client with original file and 
transferred file. It should also have the ability to transfer large files using `DN` and `UP` command. 