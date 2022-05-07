"""
IS496: Computer Networks (Spring 2022)
Mini Project - Online Pong Game
Member 1: River Liu, ll24
Member 2: Yuxuan Jiang, yj26
Member 3: Zhizhou Xu, zhizhou6
"""

# Import Libraries
import socket
import sys
import curses
import time
import threading

BUFFER = 1024
HOSTNAME = sys.argv[1]
PORT = int(sys.argv[2])


def init_curses():
    global win

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    win = curses.newwin(HEIGHT, WIDTH)
    win.keypad(True)
    win.box(0, 0)
    win.refresh()
    win.nodelay(True)
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)


def reset():
    """
    Return ball and paddles to starting positions
    Horizontal direction of the ball is randomized
    """
    global ball_x, ball_y, pad_left_y, pad_right_y, dx, dy, score_l, score_r, init_dx
    ball_x = int(WIDTH / 2)
    pad_left_y = pad_right_y = ball_y = int(HEIGHT / 2)
    # dx is randomly either -1 or 1
    dx = init_dx
    dy = 0
    # Draw to reset everything visually
    draw(ball_x, ball_y, pad_left_y, pad_right_y, score_l, score_r)


def draw(ball_x, ball_y, pad_left_y, pad_right_y, score_l, score_r):
    """
    Draw the current game state to the screen
    ball_x: X position of the ball
    ball_y: Y position of the ball
    pad_left_y: Y position of the left paddle
    pad_right_y: Y position of the right paddle
    score_l: Score of the left player
    score_r: Score of the right player
    """
    win.clear()
    win.border() 
    # Center line
    for i in range(1, HEIGHT, 2):
        win.addch(i, 21, '|', curses.color_pair(1))  
    # Score
    win.addstr(1, int(WIDTH / 2) - 3, f'{score_l:2d}', curses.color_pair(2))
    win.addstr(1, int(WIDTH / 2) + 1, f'{score_r:2d}', curses.color_pair(2))
    # Ball
    win.addch(ball_y, ball_x, '#', curses.color_pair(2))
    # Paddle
    for i in range(1, HEIGHT-1, 1):
        if i > pad_right_y+2 or i < pad_right_y-2:
            win.addch(i, PAD_RIGHT_X, ' ', curses.color_pair(2))
        else:
            win.addch(i, PAD_RIGHT_X, '#', curses.color_pair(2))
    for i in range(1, HEIGHT-1, 1):
        if i > pad_left_y+2 or i < pad_left_y-2:
            win.addch(i, PAD_LEFT_X, ' ', curses.color_pair(2))
        else:
            win.addch(i, PAD_LEFT_X, '#', curses.color_pair(2))
    # Print the virtual window (win) to the screen
    win.refresh()


def countdown(message):
    """
    Display a message with a 3-second countdown
    This method blocks for the duration of the countdown
    message: The text to display during the countdown
    """
    global lock

    h = 4
    w = len(message) + 4
    popup = curses.newwin(h, w, int((HEIGHT-h) / 2), int((WIDTH-w) / 2))
    popup.box(0, 0)
    popup.addstr(1, 2, message)

    for countdown in range(3, 0, -1):
        popup.addstr(2, int(w/2), f"{countdown}")
        popup.refresh()
        time.sleep(1)
    popup.clear()
    popup.refresh()
    popup.erase()


def listen_input(win):
    """
    Listen to keyboard input
    Updates global pad positions
    """
    global pad_left_y, pad_right_y, ACTIVE, sock, sin
    while ACTIVE:
        key = win.getch()
        curses.flushinp()

        if key == curses.KEY_UP:
            pad_right_y -= 1
            sock.sendto(b'U', sin)
        elif key == curses.KEY_DOWN:
            pad_right_y += 1
            sock.sendto(b'D', sin)

        time.sleep(0.2)


def tock():
    """
    Perform periodic game functions:
    1. Move the ball
    2. Detect collisions
    3. Detect scored points and react accordingly
    4. Draw updated game state to the screen
    """
    global ball_x, ball_y, pad_left_y, pad_right_y, dx, dy, score_l, score_r
    # Move the ball
    ball_x += dx
    ball_y += dy

    # Check for paddle collisions
    # pad_y is y value of the closest paddle to ball
    if ball_x < WIDTH / 2:
        pad_y = pad_left_y
        col_x = PAD_LEFT_X + 1
    else:
        pad_y = pad_right_y
        col_x = PAD_RIGHT_X - 1
    # col_x is x value of ball for a paddle collision
    if ball_x == col_x and abs(ball_y - pad_y) <= 2:
        # Collision detected!
        dx *= -1
        # Determine bounce angle
        if ball_y < pad_y:
            dy = -1
        elif ball_y > pad_y:
            dy = 1
        else:
            dy = 0
    # Check for top/bottom boundary collisions
    if ball_y == 1:
        dy = 1
    elif ball_y == HEIGHT - 2:
        dy = -1

    # Score points
    if ball_x == 0:
        score_r = (score_r + 1) % 100
        reset()
        countdown("SCORE -->")
    elif ball_x == WIDTH - 1:
        score_l = (score_l + 1) % 100
        reset()
        countdown("<-- SCORE")

    # Finally, redraw the current state
    else:
        draw(ball_x, ball_y, pad_left_y, pad_right_y, score_l, score_r)


def recv_operation():
    global pad_left_y, ACTIVE, sock
    while ACTIVE:
        data = sock.recvfrom(BUFFER)
        if data[0] == b'U':
            pad_left_y += 1
        else:
            pad_left_y -= 1


def main(std_scr):
    global win, ACTIVE, refresh

    init_curses()
    reset()
    countdown("Starting Game")

    thread1 = threading.Thread(name='daemon', target=listen_input, args=(win,))
    thread2 = threading.Thread(target=recv_operation)
    thread1.setDaemon(True)
    thread2.setDaemon(True)
    thread1.start()
    thread2.start()

    while True:
        try:
            before = time.time()
            tock()
            after = time.time()
            to_sleep = refresh - (after - before)
            if to_sleep > refresh:
                to_sleep = refresh
            if to_sleep > 0:
                time.sleep(to_sleep)
            else:
                time.sleep(refresh/2)
        except KeyboardInterrupt:
            break

    ACTIVE = False
    curses.nocbreak()
    win.keypad(False)
    curses.echo()
    curses.endwin()


def set_vals(x: int, difficulty: float):
    global HEIGHT, WIDTH, PAD_LEFT_X, PAD_RIGHT_X, ball_x, ball_y, dx, dy, pad_left_y, pad_right_y, score_l, score_r, ACTIVE, refresh
    HEIGHT = 21
    WIDTH = 43
    PAD_LEFT_X = 1
    PAD_RIGHT_X = WIDTH - 2
    # Position of ball
    ball_x = ball_y = 0
    # Movement of ball
    dx = x
    dy = 0
    # Position of paddles
    pad_left_y = pad_right_y = 0
    # Player scores
    score_l = score_r = 0
    # thread status
    ACTIVE = True

    refresh = difficulty


if __name__ == '__main__':
    # Get host IP using hostname
    try:
        host = socket.gethostbyname(HOSTNAME)
    except socket.error:
        print('Failed to resolve hostname.')
        sys.exit()

    sin = (host, PORT)

    # Create a socket in UDP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()
    
    difficulty = input("Please select the difficulty level (easy, medium or hard): ")
    sock.sendto(difficulty.encode('utf-8'), sin)
    ack_data = sock.recvfrom(BUFFER)
    difficulty = float(ack_data[0].decode('utf-8'))
    if difficulty < 0:
        init_dx = -1
        difficulty = -difficulty
    else:
        init_dx = 1

    set_vals(init_dx, difficulty)
    curses.wrapper(main)

    sock.close()
