import curses
import random

ROWS = 6
COLS = 7

EMPTY = 0
P1 = 1
P2 = 2

def create_board():
    """Make a 6x7 board filled with zeros (empty)."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def drop_piece(board, col, player):
    """Put a piece in the lowest empty row of the chosen column."""
    for row in range(ROWS-1, -1, -1):  # start from bottom
        if board[row][col] == EMPTY:
            board[row][col] = player
            return True
    return False  # column full

def check_win(board, player):
    """Check if player has 4 in a row."""
    directions = [(0,1), (1,0), (1,1), (-1,1)]  # right, down, down-right, up-right
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != player:
                continue
            for dr, dc in directions:
                count = 0
                rr, cc = r, c
                while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == player:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False

def board_full(board):
    """Check if the board is completely full (for a draw)."""
    return all(board[0][c] != EMPTY for c in range(COLS))

def menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to LOW QUALITY Connect 4! PLEASE PLAY OUR GAME!🤩🤩")
    stdscr.addstr(2, 0, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()

    stdscr.clear()
    stdscr.addstr(0, 0, "Choose your mode:")
    stdscr.addstr(1, 0, "1. Player vs Player ✨")
    stdscr.addstr(2, 0, "2. Player vs Bot 😱")
    stdscr.addstr(4, 0, "Press 1 or 2 to start. 😁")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('1'):
            return "pvp"
        elif key == ord('2'):
            return "pvb"

def bot_move(board):
    """Bot picks a random valid column."""
    valid_cols = [c for c in range(COLS) if board[0][c] == EMPTY]
    return random.choice(valid_cols) if valid_cols else None

def draw_board(stdscr, board, current_col, player, mode, moves_count):
    stdscr.clear()
    stdscr.addstr(0, 0, "Connect 4 (press q to quit)")
    if mode == "pvb" and player == P2:
        stdscr.addstr(1, 0, "Bot's turn...")
    else:
        stdscr.addstr(1, 0, f"Player {player}'s turn. Use 'a'/'d' to move, Enter to drop.")

    stdscr.addstr(2, 0, f"Moves - P1 (X): {moves_count[P1]} | P2 (O): {moves_count[P2]}")

    # draw selector arrow
    for c in range(COLS):
        stdscr.addstr(3, c*2, "v" if c == current_col else " ")

    # draw grid
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            if board[r][c] == EMPTY:
                row_str += "_ "
            elif board[r][c] == P1:
                row_str += "X "
            else:
                row_str += "O "
        stdscr.addstr(r+4, 0, row_str)

    stdscr.refresh()

def show_message(stdscr, text):
    """Helper to safely show a message at the bottom of the screen."""
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height-2, 0, text[:width-1])  # truncate if too long
    stdscr.refresh()
    stdscr.getch()

def game(stdscr, mode):
    curses.curs_set(0)
    stdscr.keypad(True)

    board = create_board()
    current_col = 0
    player = P1
    moves_count = {P1: 0, P2: 0}

    while True:
        draw_board(stdscr, board, current_col, player, mode, moves_count)

        if mode == "pvb" and player == P2:
            curses.napms(500)
            col = bot_move(board)
            if col is None:
                show_message(stdscr, "It's a draw! BORING! Press any key.")
                break
            drop_piece(board, col, player)
            moves_count[player] += 1
            if check_win(board, player):
                draw_board(stdscr, board, col, player, mode, moves_count)
                show_message(stdscr, "Bot wins! SKILL ISSUE! Press any key.")
                break
            if board_full(board):
                show_message(stdscr, "It's a draw! DANG YALL SUCK! Press any key.")
                break
            player = P1
            continue

        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            break
        elif key in (ord('a'), ord('A')):
            current_col = max(0, current_col - 1)
        elif key in (ord('d'), ord('D')):
            current_col = min(COLS-1, current_col + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            if drop_piece(board, current_col, player):
                moves_count[player] += 1
                if check_win(board, player):
                    draw_board(stdscr, board, current_col, player, mode, moves_count)
                    show_message(stdscr, f"Player {player} wins! +AURA! Press any key.")
                    break
                if board_full(board):
                    show_message(stdscr, "It's a draw! BORING! Press any key.")
                    break
                player = P2 if player == P1 else P1

def main(stdscr):
    while True:
        mode = menu(stdscr)   # ask player which mode
        game(stdscr, mode)    # start game with that mode

        # After game ends, ask if player wants to play again
        height, width = stdscr.getmaxyx()
        stdscr.addstr(height-3, 0, "Play again? Press 'y' for yes or 'n' for no.")
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key in (ord('y'), ord('Y')):
                break  # restart loop → new game
            elif key in (ord('n'), ord('N')):
                stdscr.addstr(height-2, 0, "Thanks for playing! Press any key to quit.")
                stdscr.refresh()
                stdscr.getch()
                return  # exit program
            else:
                stdscr.addstr(height-2, 0, "Please press 'y' or 'n'.")
                stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)