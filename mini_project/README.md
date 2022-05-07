# IS496 Group1 Mini Project


## Group Members
|     Name     |  NetID   |
|:------------:|:--------:|
|  River Liu   |   ll24   |
| Yuxuan Jiang |   yj26   |
|  Zhizhou Xu  | zhizhou6 |


## Introduction
This project is an Online Pong Game that allows two different machines play the same game instance through the server

Before running the scripts, please put `pongserver.py` in Student Machine `student00`.


## Project File Structure
    mini_project
        - pongclent.py
        - pongserver.py


## Example Command
To run the game, after entering the directory with all the scripts, run following command

**Server (`student00`)**

`[netid@is-student00 ~] $ python3 pongserver.py [port]`

**Client (`student01/02/03`)**

`[netid@is-student01 ~] $ python3 pongclient.py student00.ischool.illinois.edu [port]`

Use `UP` key to move the pad up, and use `DOWN` key to move the pad down. Use `Ctrl + C` on clients to exit the
application.

Use `Ctrl + C` on server to stop the server.
