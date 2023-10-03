# Faster module based on NumPy arrays.
# To speed up Evo operations
from collections import defaultdict
from dataclasses import dataclass

# Map all boards to a natural number (N)
# Map all moves to a natural number (M)
# A Strategy is an (N by M) matrix
def empty_board():
    return 0

__apply_move_memo = {}


def board_to_string(board):
    pretty_board = ''
    for row in board:
        pretty_board += ' | '.join(row) + '\n'
    return pretty_board


__is_winning_state_memo = {}


def is_winning_state(board):
    """
    Is the board is a winning state? Produces False if not.
    Otherwise, produces the winning player, X_MARK or O_MARK or DRAW.
    Invariant: board is not in a state where two players are simultaneously winning
    Results are cached for performance.
    """
    if board in __is_winning_state_memo:
        return __is_winning_state_memo[board]
    else:
        res = __rows(board) or __cols(board) or __diagonals(board) or __draw(board)
        __is_winning_state_memo[board] = res
        return res


def __rows(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != FREE:
            return row[0]
    return False


def __cols(board):
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != FREE:
            return board[0][col]
    return False


def __diagonals(board):
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != FREE:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != FREE:
        return board[0][2]
    return False

def __draw(board):
    # Any empty spots?
    for row in board:
        if any([mark == FREE for mark in row]):
            return False
    return DRAW

# Internal variables, populated by __init_all_possible_boards_and_moves_from
__all_boards = set()
__valid_moves_for_board = defaultdict(set)
__winning_boards = set()

def __init_board_search(board, player):
    """ From an initial state, what possible boards are there? """

    if board in __all_boards or is_winning_state(board):
        __winning_boards.add(board)
        __all_boards.add(board)
        return

    __all_boards.add(board)

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == FREE:
                move = create_move(player, row, col)
                __valid_moves_for_board[board].add(move)
                __init_board_search(
                    __unsafe_board_move(board, move),
                    next_player(player)
                )
    return


__init_board_search(empty_board(), X_MARK)

def all_board_states():
    return __all_boards

def valid_moves(board):
    return list(__valid_moves_for_board[board])

def board_move(board, move):
    if move not in valid_moves(board):
        raise Exception(f"Illegal move: {move}")
    return __unsafe_board_move(board, move)