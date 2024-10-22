import numpy as np
import time
from chess_piece import *

PIECE_NUMBER = {
    King : 1,
    Queen : 2,
    Bishop : 3,
    Knight : 4,
    Rook : 5,
    Pawn : 6
}

PIECE = {
    1 : King,
    2 : Queen,
    3 : Bishop,
    4 : Knight,
    5 : Rook,
    6 : Pawn
}

def get_all_move(broad, is_white, break_check = []):
    all_move = []

    if is_white:
        indices = np.array(np.where(broad > 0), dtype=np.int16).T
        values = broad[broad > 0]
    else:
        indices = np.array(np.where(broad < 0), dtype=np.int16).T
        values = broad[broad < 0]

    if len(break_check) == 0:
        for index, value in zip(indices, values):
            possible_moves = PIECE[abs(value)].get_possible_move(tuple(index), broad)

            for move in [move for moves in possible_moves for move in moves]:
                all_move.append([tuple(index), move])

    else:
        for index, value in zip(indices, values):
            possible_moves = PIECE[abs(value)].get_possible_move(tuple(index), broad)

            for move in [move for moves in possible_moves for move in moves]:
                if move in break_check:
                    all_move.append([tuple(index), move])
                elif abs(value) == 1:
                    all_move.append([tuple(index), move])


    return all_move

def is_check(is_white_move: bool, broad: ndarray):
    if is_white_move:
        indices = np.array(np.where(broad > 0), dtype=np.int16).T
        values = broad[broad > 0]
    else:
        indices = np.array(np.where(broad < 0), dtype=np.int16).T
        values = broad[broad < 0]

    break_check = []

    for index, value in zip(indices, values):
        _, possible_takes = PIECE[abs(value)].get_possible_move(tuple(index), broad)

        for take in possible_takes:
            if PIECE[abs(broad[take])] is King:
                break_check.extend(PIECE[abs(value)].to_opp_king(tuple(index), take))
    
    return break_check
        
def piece_move(broad: ndarray, old_pos, new_pos):
    broad[new_pos] = broad[old_pos]
    broad[old_pos] = 0
    
    is_white = True
    if broad[new_pos] < 0:
        is_white = False

    return is_check(is_white, broad)

class ScoreSupporter:
    SCORE = {
        1 : 20000,  # king score
        2 : 900,    # queen score
        3 : 330,    # bishop score
        4 : 320,    # knight score
        5 : 500,    # rook score
        6 : 100,    # pawn score
    }

    PAWN_TABLE = np.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = np.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = np.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = np.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    QUEEN_TABLE = np.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

    @staticmethod
    def evaluate(broad: ndarray):
        broad_score = ScoreSupporter.broad_score(broad)

        queen_score = ScoreSupporter.piece_score(broad, ScoreSupporter.QUEEN_TABLE, Queen)
        bishop_score = ScoreSupporter.piece_score(broad, ScoreSupporter.BISHOP_TABLE, Bishop)
        knight_score = ScoreSupporter.piece_score(broad, ScoreSupporter.KNIGHT_TABLE, Knight)
        rook_score = ScoreSupporter.piece_score(broad, ScoreSupporter.ROOK_TABLE, Rook)
        pawn_score = ScoreSupporter.piece_score(broad, ScoreSupporter.PAWN_TABLE, Pawn)

        return broad_score + queen_score + bishop_score + knight_score + rook_score + pawn_score

    @staticmethod
    def broad_score(broad: ndarray):
        white = 0
        black = 0

        for value in broad[broad != 0]:
            score = ScoreSupporter.SCORE[abs(value)]
            if value > 0:
                white += score
            else:
                black += score
        
        return white - black
    
    @staticmethod
    def piece_score(broad: ndarray, table: ndarray, piece_type):
        white = 0
        black = 0

        for index in np.argwhere(np.abs(broad) == PIECE_NUMBER[piece_type]):
            if broad[tuple(index)] > 0:
                white += table[index[1], index[0]]
            else:
                black += table[7 - index[1], index[0]]

        return white - black

class AI:
    INFINITE = 10000000

    @staticmethod
    def move(broad: ndarray, break_check: list=[]):
        curr_pos = 0
        best_move = 0
        best_score = AI.INFINITE

        all_move = get_all_move(broad, False, break_check)
        
        for old_pos, new_pos in all_move:
            broad_clone = broad.copy()

            break_check = piece_move(broad_clone, old_pos, new_pos)              
            score = AI.alpha_beta(2, broad_clone, -AI.INFINITE, AI.INFINITE, True, break_check)

            if score < best_score:
                best_score = score
                best_move = new_pos
                curr_pos = old_pos

        if best_move == 0:
            return 0
        
        return curr_pos, best_move

    @staticmethod
    def costMove(broad: ndarray):
        pass

    @staticmethod
    def alpha_beta(depth: int, broad: ndarray, alpha, beta, maximizing: bool, break_check = []):
        if depth == 0:
            return ScoreSupporter.evaluate(broad)
        
        if maximizing:
            best_score = -AI.INFINITE

            for old_pos, new_pos in get_all_move(broad, True, break_check):
                broad_clone = broad.copy()

                break_check = piece_move(broad_clone, old_pos, new_pos)
                best_score = max(best_score, AI.alpha_beta(depth - 1, broad_clone, alpha, beta, False, break_check))

                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            
            return best_score

        else:
            best_score = AI.INFINITE

            for old_pos, new_pos in get_all_move(broad, False, break_check):
                broad_clone = broad.copy()

                break_check = piece_move(broad_clone, old_pos, new_pos)
                best_score = min(best_score, AI.alpha_beta(depth - 1, broad_clone, alpha, beta, True, break_check))

                beta = min(alpha, best_score)
                if beta <= alpha:
                    break
            
            return best_score

if __name__ == '__main__':
    broad = np.array([
        [ 5,  6,  0,  0,  0,  0, -6, -5],
        [ 4,  6,  0,  0,  0,  0, -6,  0],
        [ 3,  6,  0,  0,  0,  3, -6, -3],
        [ 2,  6,  0,  0,  0, -6,  0, -2],
        [ 1,  0,  0,  6, -6,  0,  0, -1],
        [ 0,  6,  4,  0,  0,  0, -6, -3],
        [ 0,  6,  0,  0,  0,  0, -6, -4],
        [ 5,  6,  0,  0,  0,  0, -6, -5], 
    ])
    start_time = time.time()  # Ghi lại thời gian bắt đầu
    print(AI.move(broad, [(2, 5), (3, 6)]))
    end_time = time.time()  # Ghi lại thời gian kết thúc

    print(end_time - start_time)