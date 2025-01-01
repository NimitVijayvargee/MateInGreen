import chess, pygame, random
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
# Piece Definitions
maps = {
"P" : [
     0,  0,  0,  0,  0,  0,  0,  0,
     5,  5,  5,  5,  5,  5,  5,  5,
     1,  1,  2,  3,  3,  2,  1,  1,
     0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
     0,  0,  0,  2,  2,  0,  0,  0,
     0.5, -0.5, -1,  0,  0, -1, -0.5, 0.5,
     0.5,  1,  1, -2, -2,  1,  1,  0.5,
     0,  0,  0,  0,  0,  0,  0,  0
],
"N" : [
    -5, -4, -3, -3, -3, -3, -4, -5,
    -4, -2,  0,  0,  0,  0, -2, -4,
    -3,  0,  1,  1.5,  1.5,  1,  0, -3,
    -3,  0.5, 1.5,  2,  2,  1.5,  0.5, -3,
    -3,  0,  1.5,  2,  2,  1.5,  0, -3,
    -3,  0.5,  1,  1.5,  1.5,  1,  0.5, -3,
    -4, -2,  0,  0.5,  0.5,  0, -2, -4,
    -5, -4, -3, -3, -3, -3, -4, -5
],
"B" : [
    -2, -1, -1, -1, -1, -1, -1, -2,
    -1,  0,  0,  0,  0,  0,  0, -1,
    -1,  0,  0.5,  1,  1,  0.5,  0, -1,
    -1,  0.5,  0.5,  1,  1,  0.5,  0.5, -1,
    -1,  0,  1,  1,  1,  1,  0, -1,
    -1,  1,  1,  1,  1,  1,  1, -1,
    -1,  0.5,  0,  0,  0,  0,  0.5, -1,
    -2, -1, -1, -1, -1, -1, -1, -2
],
"R": [
     0,  0,  0,  0,  0,  0,  0,  0,
     0.5,  1,  1,  1,  1,  1,  1,  0.5,
    -0.5,  0,  0,  0,  0,  0,  0, -0.5,
    -0.5,  0,  0,  0,  0,  0,  0, -0.5,
    -0.5,  0,  0,  0,  0,  0,  0, -0.5,
    -0.5,  0,  0,  0,  0,  0,  0, -0.5,
    -0.5,  0,  0,  0,  0,  0,  0, -0.5,
     0,  0,  0,  0.5,  0.5,  0,  0,  0
],
"Q" : [
    -2, -1, -1, -0.5, -0.5, -1, -1, -2,
    -1,  0,  0,  0,  0,  0,  0, -1,
    -1,  0,  0.5,  0.5,  0.5,  0.5,  0, -1,
    -0.5,  0,  0.5,  0.5,  0.5,  0.5,  0, -0.5,
     0,  0,  0.5,  0.5,  0.5,  0.5,  0, -0.5,
    -1,  0.5,  0.5,  0.5,  0.5,  0.5,  0, -1,
    -1,  0,  0.5,  0,  0,  0,  0, -1,
    -2, -1, -1, -0.5, -0.5, -1, -1, -2
],
"K" : [
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -2, -3, -3, -4, -4, -3, -3, -2,
    -1, -2, -2, -2, -2, -2, -2, -1,
     2,  2,  0,  0,  0,  0,  2,  2,
     2,  3,  1,  0,  0,  1,  3,  2
]}
maps["p"] = maps["P"][::-1]
maps["k"] = maps["K"][::-1]
maps["b"] = maps["B"][::-1]
maps["r"] = maps["R"][::-1]
maps["q"] = maps["Q"][::-1]
maps["n"] = maps["N"][::-1]

def eval_board(BOARD: chess.Board) -> float:
    
    score = 0
    pieces = BOARD.piece_map()
    
    for key in pieces:
        score += scoring[str(pieces[key])]

    return score

def minmax(BOARD, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
    # Base case: if we've reached a depth limit or the game is over
    if depth == 0 or BOARD.is_game_over():
        return eval_board(BOARD), None  # Evaluate board (you can define this evaluation function)

    if is_maximizing:
        max_eval = (float('-inf'), None)
        for move in BOARD.legal_moves:
            temp_board = deepcopy(BOARD)
            temp_board.push(move)
            evaluation = minmax(temp_board, depth - 1, False, alpha, beta)
            if evaluation[0] > max_eval[0]:
                alpha = max(alpha, evaluation[0])
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = float('inf')
        legal_moves = BOARD.legal_moves
        evaluations = {}
        for move in legal_moves:
            temp_board = deepcopy(BOARD)
            temp_board.push(move)
            evaluation = minmax(temp_board, depth - 1, True, alpha, beta)
            if evaluation < min_eval:
                min_eval = evaluation
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval