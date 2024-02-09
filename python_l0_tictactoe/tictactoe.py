import copy
"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
"""return [[EMPTY, X, O],
            [O, X, EMPTY],
            [X, EMPTY, O]]
            """
board = initial_state()

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    numX = 0
    numO = 0
    # read nbr. of player moves
    for i in range(len(board)):
        for j in range(len(board[i])):
                if board[i][j] == "X":
                    numX += 1
                if board[i][j] == "O":
                    numO += 1
    if numX > numO:
        return O
    else:
        return X

def actions(board):
    possible_action_list = set()
    #possible_action_list = []
    # read empty fields and return a list
    for i in range(len(board)):
        for j in range(len(board[i])):
                if board[i][j] == EMPTY:
                    possible_action_list.add((i , j))
    return possible_action_list

def result(board, action):
    # If choosen field is empty set player X or O sign
    if action not in actions(board):
        raise Exception("Move not possible.")
    result_board = copy.deepcopy(board)
    result_board[action[0]][action[1]] = player(board)
    return result_board
    
def winner(board):
    # Set winning positions
    winner_positions = [
                         [[0,0],[0,1],[0,2]],
                         [[1,0],[1,1],[1,2]],
                         [[2,0],[2,1],[2,2]],
                         [[0,0],[1,0],[2,0]],
                         [[0,1],[1,1],[2,1]],
                         [[0,2],[1,2],[2,2]],
                         [[0,0],[1,1],[2,2]],
                         [[2,0],[1,1],[0,2]]
                         ]
    # check winner positions
    for list in winner_positions:
        nbrX = 0
        nbrO = 0
        # check if player X,O has a winning position
        for pos in list:
            if board[pos[0]][pos[1]] == "X":
                nbrX += 1
            if nbrX == 3:
                return X
            if board[pos[0]][pos[1]] == "O":
                nbrO += 1
            if nbrO == 3:
                return O
    else:
        return None

def terminal(board):
    # Check if Game is over
    if not actions(board) or winner(board) is not None:
        return True
    else:
        return False

def utility(board):
    # Return utility of terminal state
    if terminal(board) is True:
        if winner(board) is X:
            return 1
        elif winner(board) is O:
            return -1
        else:
            return 0  

def MaxValue(board):
    # Return Maximum Value/utility between actual value u and result_board utility
    u = -2
    if terminal(board):
        return utility(board)
    for action in actions(board):
        u = max(u, MinValue(result(board, action)))
    return u

def MinValue(board):
    # Return Minimum Value/utility between actual value u and result_board utility
    if terminal(board):
        return utility(board)
    u = 1
    for action in actions(board):
        u = min(u, MaxValue(result(board, action)))
    return u

def minimax(board):    
    # If Game is over ruturn None
    if terminal(board):
        return None
    # If Players turn return optimal move
    elif player(board) == O:            
        u_min = 1
        opt_move = []
        # iterate over possible moves, get max utility value depending on opponent moves and return opt move
        for move in actions(board):
            result_board = result(board, move)
            min_value = MaxValue(result_board)
            if min_value < u_min:
                u_min = min_value
                opt_move = move
        return opt_move
    # Same for the other player
    elif player(board) == X:      
        u_max = -1
        opt_move = []
        for move in actions(board):
            max_value = MinValue(result(board, move))
            if max_value > u_max:
                u_max = max_value
                opt_move = move
        return opt_move