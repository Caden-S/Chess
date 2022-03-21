def board_print(board):
    player = board[-1]
    if player == 'b':
        board = flip_board(board)
    board_list = board.split("/")
    board_list[-1] = board_list[-1][:-2]

    spacer = "   ------------------------------- "
    print(spacer)
    row_counter = 1
    for item in board_list:
        if player == 'w':
            row = "{} | ".format(row_counter)
        else:
            row = "{} | ".format(9 - row_counter)
        if len(item) > 1:
            for char in item:
                if char == '0':
                    row += ("  | ".format(char))
                else:
                    row += ("{} | ".format(char))
        print(row)
        print(spacer)
        row_counter += 1
    if player == 'w':
        print("    a   b   c   d   e   f   g   h")
    else:
        print("    h   g   f   e   d   c   b   a ")

def flip_board(board):
    player = board[-2:]
    board = board[:-2]
    board = board[::-1]
    return board + player

def in_board(move):
    return (move < 8 and move >= 0)

def make_list(board):
    return board.split("/")

def location_empty(board, row, col):
    b = board.split("/")
    return  b[row][col:col+1] == "0"
