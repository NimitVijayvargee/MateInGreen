import chess, pygame
from copy import deepcopy

scoring = {
    "p": -1,
    "n": -3,
    "b": -3,
    "r": -5,
    "q": -9,
    "k": 0,
    "P": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 0,
}


def eval_board(BOARD: chess.Board):
    score = 0
    pieces = BOARD.piece_map()
    for key in pieces:
        score += scoring[str(pieces[key])]

    return score


def best_move(BOARD):
    moves = list(BOARD.legal_moves)
    scores = []

    for move in moves:
        temp = deepcopy(BOARD)
        temp.push(move)
        temp_best_move = most_value_agent(temp)
        try:
            temp.push(temp_best_move)
            scores.append(eval_board(temp))
        except AttributeError:
            pass
        

    if BOARD.turn == True:

        best_move = moves[scores.index(max(scores))]

    else:
        best_move = moves[scores.index(min(scores))]

    return best_move


def most_value_agent(BOARD):

    moves = list(BOARD.legal_moves)
    scores = []
    for move in moves:
        # creates a copy of BOARD so we dont
        # change the original class
        temp = deepcopy(BOARD)
        temp.push(move)

        scores.append(eval_board(temp))
    if moves.__len__() == 0:
        print(f"Checkmate! {chess.COLOR_NAMES[BOARD.turn]} king")
        pygame.quit()
        return None

    if BOARD.turn == True:

        best_move = moves[scores.index(max(scores))]

    else:
        best_move = moves[scores.index(min(scores))]

    return best_move
