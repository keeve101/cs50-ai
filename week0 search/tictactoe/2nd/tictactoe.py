"""
Tic Tac Toe Player
"""
class Node():
    def __init__(self, state, parent= None):
        self.state = state
        self.parent = parent
   



import math
import copy
X = "X"
O = "O"
EMPTY = None



def row_check(row):
    return row[0] == row[1] == row[2] != None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY,EMPTY,EMPTY] for i in range (3)]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for value in row:
            if value != EMPTY:
                count+=1

    return X if count %2 == 0 else O


def actions(board):
    actions = []
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column:
                continue
            else:
                actions.append((i, j))
    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise ValueError
    board = copy.deepcopy(board)
    
    board[action[0]][action[1]] = player(board)

    return board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    columns = list(map(list, zip(*board)))

    for row in board:
        if row_check(row):
            return row[0]

    for column in columns:
        if row_check(column):
            return column[0]

    return board[1][1] if board[0][0] == board[1][1] == board[2][2] != None or board[0][2] == board[1][1] == board[2][0] != None else None



def terminal(board):
    return 1 if winner(board) or not actions(board) else 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    check = winner(board)
    if check:
        return 1 if check == X else -1 
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    states = []
    moves = actions(board)
    scores = [0 for action in moves]

    for move1 in moves:
        new_board = result(board, move1)
        if terminal(new_board):
            print(utility(new_board))
            return move1
        else:
            states.append(Node(new_board, move1))
        
    while states:

        node = states[-1]
        states = states[:-1]
        poss_moves = actions(node.state)
        if not terminal(node.state):

            for move in poss_moves:
                new_board = result(node.state, move)
                states.append(Node(new_board, node.parent))
                
        else:
            for index, move in enumerate(moves):
                if move == node.parent:
                    
                    scores[index] += utility(node.state)

    
    if player(board) == X:
        index_min = max(range(len(scores)), key=scores.__getitem__)
        print(scores)
        print(moves)
        return moves[index_min]

    else:
        index_max = min(range(len(scores)), key=scores.__getitem__)
        print(scores)
        print(moves)
        return moves[index_max]







    





