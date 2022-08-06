"""
Tic Tac Toe Player
"""

import math
import copy
import time


X = "X"
O = "O"
EMPTY = None

class Node():
    def __init__(self, state, score):
        self.state = state
        self.score = score

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

def minimax(board,depth, ls):
    """
    Returns the optimal action for the current player on the board.
    """
    bestval = -100000000
    for move in actions(board):
        value = maximiser(result(board), move, depth, ls)
        bestval = max(value, bestval)
    return bestval


def maximiser(board, depth, ls):
    if terminal(board):
        return utility(board)
    else:
        bestval = -100000000
        value = 0
        
        for move in actions(board):
            value += maximiser(result(board, move), depth, ls)
            bestval = max(bestval, value)
        return bestval 


        


def minimiser(board, depth):
    return None

score = 0
lst1 = []
ts = 0
print(maximiser(initial_state(), 0, lst1))
print(lst1)