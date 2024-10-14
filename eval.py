import chess, pygame, random, requests, json
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

def minmax(BOARD: chess.Board, depth: int, is_maximizing: bool):
    if depth == 0 or BOARD.is_game_over():
        return eval_board(BOARD)

    moves = list(BOARD.legal_moves)
    best_move = None
    
    if is_maximizing:
        max_eval = -float('inf')
        for move in moves:
            temp = deepcopy(BOARD)
            temp.push(move)
            eval = minmax(temp, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        if depth == 3:
            return best_move
        return max_eval
    
    else:  # BLACK's turn (minimizing)
        min_eval = float('inf')
        for move in moves:
            temp = deepcopy(BOARD)
            temp.push(move)
            eval = minmax(temp, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        if depth == 3:  # Return move at top level
            return best_move
        return min_eval
