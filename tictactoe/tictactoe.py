"""
Tic Tac Toe Player
"""
import math
import copy

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    
    for row in board:
        for element in row:
            if element == 'X':
                x_count += 1
            elif element == 'O':
                o_count += 1

    if x_count == o_count:
        return 'X'
    else:
        return 'O'



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i, row in enumerate(board):
        for j, element in enumerate(row):
            if element is None:
                possible_actions.add((i,j))
                
    return possible_actions
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
            raise Exception("No la aguanta")

    board_copy = copy.deepcopy(board)

    for i, row in enumerate(board):
        for j, element in enumerate(row):

            if (i, j) == action:
                board_copy[i][j] = player(board)
                return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check rows
    for row in board:
        if row == ['X', 'X', 'X']:
            return 'X'
        elif row == ['O', 'O', 'O']:
            return 'O'
        
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    elif len(actions(board)) == 0:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0
    

def minimax(board):
    """
    Retorna la acción óptima para el jugador actual en el tablero.
    """
    if terminal(board):
        return None

    elif player(board) == 'X':
        plays = []
        for action in actions(board):
            plays.append([min_value(result(board, action)), action])
        
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]

    elif player(board) == 'O':
        plays = []
        for action in actions(board):
            plays.append([max_value(result(board, action)), action])
        
        print(sorted(plays, key=lambda x: x[0]))
        return sorted(plays, key=lambda x: x[0])[0][1]
    

def max_value(board):

    value = -math.inf

    if terminal(board):
        return utility(board)

    for action in actions(board):
        value = max(value, min_value(result(board, action))) 
    
    return value


def min_value(board):

    value = math.inf

    if terminal(board):
        return utility(board)

    for action in actions(board):
        value = min(value, max_value(result(board, action))) 
    
    return value