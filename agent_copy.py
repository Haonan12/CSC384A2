"""
An AI player for Othello. 
"""

import random
import sys
import time

cache_minimax = {}
cache_alphabeta = {}
f = 0
g = 0
# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    return get_score(board)[color-1] - get_score(board)[2 - color]

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    add_scores = 0

    # Additional score for corner, punish for occupy by opponents
    if board[0][0] != 0:
        add_scores += 4 * len(board) * (abs(int(board[0][0]) - color) + 0.5)
    if board[0][len(board)-1] != 0:
        add_scores += 4 * len(board) * (abs(int(board[0][len(board)-1]) - color) + 0.5)
    if board[len(board)-1][0] != 0:
        add_scores += 4 * len(board) * (abs(int(board[len(board)-1][0]) - color) + 0.5)
    if board[len(board)-1][len(board)-1] != 0:
        add_scores += 4 * len(board) * (abs(int(board[len(board)-1][len(board)-1]) - color) + 0.5)

    # Punish for near corner if the player not occupy the corner
    if board[1][0] == color:
        add_scores -= len(board) * (abs(int(board[0][0]) - color) + 0.5)
    if board[0][1] == color:
        add_scores -= len(board) * (abs(int(board[0][0]) - color) + 0.5)
    if board[1][1] == color:
        add_scores -= 2 * len(board) * (abs(int(board[0][0]) - color) + 0.5)

    if board[1][len(board)-1] == color:
        add_scores -= len(board) * (abs(int(board[0][len(board)-1]) - color) + 0.5)
    if board[0][len(board)-2] == color:
        add_scores -= len(board) * (abs(int(board[0][len(board)-1]) - color) + 0.5)
    if board[1][len(board)-2] == color:
        add_scores -= 2 * len(board) * (abs(int(board[0][len(board)-1]) - color) + 0.5)

    if board[len(board)-2][len(board)-1] == color:
        add_scores -= len(board) * (abs(int(board[len(board)-1][len(board)-1]) - color) + 0.5)
    if board[len(board)-1][len(board)-2] == color:
        add_scores -= len(board) * (abs(int(board[len(board)-1][len(board)-1]) - color) + 0.5)
    if board[len(board)-2][len(board)-2] == color:
        add_scores -= 2 * len(board) * (abs(int(board[len(board)-1][len(board)-1]) - color) + 0.5)

    if board[len(board)-2][0] == color:
        add_scores -= len(board) * (abs(int(board[len(board)-1][0]) - color) + 0.5)
    if board[len(board)-1][1] == color:
        add_scores -= len(board) * (abs(int(board[len(board)-1][0]) - color) + 0.5)
    if board[len(board)-2][1] == color:
        add_scores -= 2 * len(board) * (abs(int(board[len(board)-1][0]) - color) + 0.5)

    return add_scores + compute_utility(board, color) #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #IMPLEMENT (and replace the line below)
    if caching and (board, 3 - color) in cache_minimax.keys():
        return cache_minimax[(board,3 - color)]
    min_move = None
    moves = get_possible_moves(board, 3-color)
    if not moves:
        if caching:
            cache_minimax[(board, 3 - color)] = min_move, compute_utility(board, color)
            return cache_minimax[(board, 3 - color)]
        return min_move, compute_utility(board, color)

    min_value = float("inf")
    for move in moves:
        new_board = play_move(board, 3-color, move[0], move[1])
        if limit > 1:
            (next_move, new_value) = minimax_max_node(new_board, color, limit - 1, caching)
        else:
            new_value = compute_utility(new_board, color)
        if min_value > new_value:
            min_value, min_move = new_value, move

    if caching:
        cache_minimax[(board, 3 - color)] = min_move, min_value
        return cache_minimax[(board, 3 - color)]

    return min_move, min_value

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT (and replace the line below)

    if caching and (board,color) in cache_minimax.keys():
        return cache_minimax[(board,color)]
    max_move = None
    moves = get_possible_moves(board, color)
    if not moves:
        if caching:
            cache_minimax[(board, 3 - color)] = max_move, compute_utility(board, color)
            return cache_minimax[(board, 3 - color)]
        return max_move, compute_utility(board, color)

    max_value = float("-inf")
    for move in moves:
        new_board = play_move(board, color, move[0], move[1])
        if limit > 1:
            (next_move, new_value) = minimax_min_node(new_board, color, limit - 1, caching)
        else:
            new_value = compute_utility(new_board, color)
        if max_value < new_value:
            max_value, max_move = new_value, move

    if caching:
        cache_minimax[(board, color)] = max_move, max_value
        return cache_minimax[(board, color)]
    return max_move, max_value

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    (next_move, new_value) = minimax_max_node(board, color, limit, caching)
    return next_move

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT (and replace the line below)
    # print(len(cache_alphabeta))
    if caching and (board, 3 - color) in cache_alphabeta.keys():
        return cache_alphabeta[(board,3 - color)]
    min_move = None
    # if ordering:
    #     moves = node_ordering_sort(board, 3-color)
    moves = get_possible_moves(board, 3 - color)
    if not moves:
        value = compute_heuristic(board, color)
        if caching:
            cache_alphabeta[(board, 3 - color)] = min_move, value
        return min_move, value

    min_value = float("inf")
    value_list = []
    if ordering:
        moves = sorted(moves, key = lambda move: compute_heuristic(play_move(board, 3 - color, move[0], move[1]), 3 - color), reverse = True)
    else:
        nmoves = sorted(moves,
                       key=lambda move: compute_heuristic(play_move(board, 3 - color, move[0], move[1]), 3 - color),
                       reverse=True)
    # print("min")
    # print(len(moves))
    for move in moves:

        # print(compute_utility(play_move(board, 3-color, move[0], move[1]), 3-color))
        # print(compute_utility(play_move(board, 3 - color, x[0], x[1]), color))
        new_board = play_move(board, 3-color, move[0], move[1])
        if limit > 1:
            (next_move, new_value) = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        else:
            new_value = compute_heuristic(new_board, color)
        if min_value > new_value:
            min_value, min_move = new_value, move

        if min_value <= alpha:
            if caching:
                cache_alphabeta[(board, 3 - color)] = min_move, min_value
            return min_move, min_value
        beta = min(beta, min_value)

    if caching:
        cache_alphabeta[(board, 3 - color)] = min_move, min_value
    return min_move, min_value

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):

    #IMPLEMENT (and replace the line below)
    # print(len(cache_alphabeta))
    if caching and (board,color) in cache_alphabeta.keys():
        return cache_alphabeta[(board, color)]
    max_move = None

    moves = get_possible_moves(board, color)
    if not moves:
        value = compute_heuristic(board, color)
        if caching:
            cache_alphabeta[(board, color)] = max_move, value
            return cache_alphabeta[(board, color)]
        return max_move, value

    max_value = float("-inf")
    if ordering:

        moves = sorted(moves, key = lambda move: compute_heuristic(play_move(board, color, move[0], move[1]), color), reverse = True)
    else:
        nmoves = sorted(moves, key=lambda move: compute_heuristic(play_move(board, color, move[0], move[1]), color),
                       reverse=True)

    # print("max")
    # print(len(moves))
    for move in moves:
        new_board = play_move(board, color, move[0], move[1])
        if limit > 1:
            (next_move, new_value) = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        else:
            new_value = compute_heuristic(new_board, color)
        if max_value < new_value:
            max_value, max_move = new_value, move

        if max_value >= beta:
            if caching:
                cache_alphabeta[(board, color)] = max_move, max_value
            return max_move, max_value
        alpha = max(alpha, max_value)

    if caching:
        cache_alphabeta[(board, color)] = max_move, max_value
    return max_move, max_value

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    (next_move, new_value) = alphabeta_max_node(board, color, float("-inf"), float("inf"), limit, caching, ordering)
    return next_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            board = tuple(tuple(row) for row in board)
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
