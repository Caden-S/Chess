import os
from Board import *
from math import floor

def start():
    # modified FEN notation because this is easier to deal with
    board = "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR w"
    play(board, 0)

def play(board, err):
    os.system("clear")
    board_print(board)
    if err == 1:
        print("Please enter a valid move.")
    move = input("Please enter your move (d7d6): ")
    if check_input(board, move) == True:
        board = move_piece(board, move)
        play(board, 0)
    else:
        play(board, 1)

def move_piece(board, move):
    cols = ['a','b','c','d','e','f','g','h']
    old_x = cols.index(move[0])
    old_y = int(move[1:2]) - 1
    new_x = cols.index(move[2:3])
    new_y = int(move[3:]) - 1

    b = make_list(board)
    new_string = b[new_y][:new_x] + b[old_y][old_x:old_x+1] + b[new_y][new_x + 1:]
    b[new_y] = new_string
    new_string = b[old_y][:old_x] + '0' + b[old_y][old_x+1:]
    b[old_y] = new_string

    if b[-1][-1:] == 'w':
        b[-1] = b[-1][:-1] + 'b'
    else:
        b[-1] = b[-1][:-1] + 'w'
    new_board = '/'.join(b)
    return new_board

def check_input(board, move):
    letters = ['a','b','c','d','e','f','g','h']
    nums = [1,2,3,4,5,6,7,8]
    try:
        if len(move) == 4 and move[0] in letters and move[2] in letters and int(move[1]) in nums and int(move[3]) in nums:
            if move in available_moves(board, move[:2]):
                return True
            else:
                return False
        else:
            return False
    except IndexError:
        return False

def same_team(board, piece, target):
    return piece.islower() == board[target[0]][target[1]].islower()
    
def available_moves(board, location):
    b = make_list(board)
    cols = ['a','b','c','d','e','f','g','h']
    col = cols.index(location[0])
    row = int(location[1]) - 1
    piece = b[row][col:col+1]
    move_dict = {'p':1, 'P':-1,
                'n':[(-1,-2),(-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2)],
                'k':[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]}
    moves = []
    
    if piece.lower() in  ['r', 'b', 'q']:
        return get_moves(board, location, piece)
    if piece.lower() == 'p':
        # Diagonal captures
        move_list = move_dict[piece] * [(1,1), (1,-1)]
        for loc in move_list:
            if in_board(col + loc[0]) == True and in_board(row + loc[1]) == True:
                if location_empty(board, row + loc[1], col + loc[0]) == False and same_team(b, piece, (loc[0], loc[1])) == False:
                    moves.append(loc_reformat(location, row + loc[1] + 1, col + loc[0] + 1))
                else:
                    continue
        for i in range(1,3):
            if location_empty(board, row + (i * move_dict[piece]), col) == False:
                break
            else:
                moves.append(loc_reformat(location, row + (i * move_dict[piece]) + 1, col + 1))
    else:
        piece = piece.lower()
        for i in range(0, len(move_dict[piece])):
            if in_board(row + move_dict[piece][i][0]) == True and in_board(col + move_dict[piece][i][1]) == True:
                if location_empty(board, row + move_dict[piece][i][0], col + move_dict[piece][i][1]) == False:
                    if same_team(b, piece, (row + move_dict[piece][i][0], col + move_dict[piece][i][1])) == False:
                        moves.append(loc_reformat(location, row + move_dict[piece][i][0] + 1, col + move_dict[piece][i][1] + 1))
                        continue
                    else:
                        continue
                else:
                    moves.append(loc_reformat(location, row + move_dict[piece][i][0] + 1, col + move_dict[piece][i][1] + 1))
    return moves

def loc_reformat(origin, row, col):
    cols = ['a','b','c','d','e','f','g','h']
    return "{}{}{}".format(origin, cols[col-1], row)

def in_check(board, color):
    cols = ['a','b','c','d','e','f','g','h']
    b = make_list(board)
    piece_indexes = [ piece[0] for piece in enumerate(b[:-2]) if piece != "0"]
    piece_locs = [(floor(index/8), index%8) for index in piece_indexes]
    black_king_index, white_king_index = board.find('k'), board.find('K')
    black_king_loc = (cols[floor(black_king_index/8)], black_king_index%8)
    white_king_loc = (cols[floor(white_king_index/8)], white_king_index%8)
    white_danger = []
    black_danger = []
    for piece in piece_locs:
        if b[piece[0]][piece[1]].islower() == True:
            white_danger += available_moves(board, (cols[piece[0]], piece[1]))
        else:
            black_danger += available_moves(board, (cols[piece[0]], piece[1]))
    if color == "black":
        return black_king_loc in black_danger
    else:
        return white_king_loc in white_danger

def get_moves(board, location, piece):
    b = make_list(board)
    l_piece = piece.lower()
    moves = []
    cols = ['a','b','c','d','e','f','g','h']
    col = cols.index(location[0])
    row = int(location[1]) - 1
    left_down = [-1,-2,-3,-4,-5,-6,-7]
    right_up = [1,2,3,4,5,6,7]
    possible_moves = left_down + right_up

    type_dict = {'r':[(1,0),(0,1),(-1,0),(0,-1)],
                 'b':[(1,1),(1,-1),(-1,1),(-1,-1)],
                 'q':[(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)],}
    for key in range(0, len(type_dict[l_piece])):
        for move in possible_moves:
            new_row = row + (move * type_dict[l_piece][key][0])
            new_col = col + (move * type_dict[l_piece][key][1])
            if in_board(new_row) and in_board(new_col):
                if location_empty(board, new_row, new_col) == True:
                    moves.append(loc_reformat(location, new_row + 1, new_col + 1))
                else:
                    if same_team(b, piece, (new_row, new_col)) == False:
                        moves.append(loc_reformat(location, new_row + 1, new_col + 1))
                        break
                    else:
                        break
            else:
                break
    return moves

def checkmate(board, location, color):
    cols = ['a','b','c','d','e','f','g','h']
    split_board = make_list(board)
    b = "".join(split_board)[:-2]
    piece_indexes = [ piece[0] for piece in enumerate(b) if piece != "0"]
    piece_locs = [(floor(index/8), index%8) for index in piece_indexes]
    black_index, white_index = b.find('k'), b.find('K')
    black_king, white_king = (cols[floor(black_index/8)], black_index%8), (cols[floor(white_index/8)], white_index%8)
    if color == 'b' and available_moves(board, black_king) == []:
        return True
    if color == 'w' and available_moves(board, black_king) == []:
        return True
    else:
        return False