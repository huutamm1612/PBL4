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

def pre_castling(broad: ndarray, enemies, poses):
    for enemy in enemies:
        for pos in poses:
            if PIECE[abs(broad[enemy])].is_attack_at(enemy, pos, broad):
                return False
    return True


def get_all_move(broad, is_white, break_check = [], is_moved=[None, None]):
    all_move = []

    if is_white:
        indices = np.array(np.where(broad > 0), dtype=np.int16).T
        values = broad[broad > 0]
    else:
        indices = np.array(np.where(broad < 0), dtype=np.int16).T
        values = broad[broad < 0]

    if len(break_check) == 0:
        if is_moved[0] is not None and is_white:
            if (broad[(1, 0)] == 0 and broad[(2, 0)] == 0 and broad[(3, 0)] == 0) or (broad[(5, 0)] == 0 and broad[(6, 0)] == 0):
                enemies = get_opp_chesses(is_white, broad)
                if not is_moved[0][0] and (broad[(1, 0)] == 0 and broad[(2, 0)] == 0 and broad[(3, 0)] == 0) and pre_castling(broad, enemies, [(1, 0), (2, 0), (3, 0)]):
                    all_move.append([(4, 0), (2, 0)])
                elif not is_moved[0][1] and (broad[(5, 0)] == 0 and broad[(6, 0)] == 0) and pre_castling(broad, enemies, [(5, 0), (6, 0)]):
                    all_move.append([(4, 0), (6, 0)])
        elif is_moved[1] is not None and not is_moved[1][1] and not is_white:
            if (broad[(1, 7)] == 0 and broad[(2, 7)] == 0 and broad[(3, 7)] == 0) or (broad[(5, 7)] == 0 and broad[(6, 7)] == 0):
                enemies = get_opp_chesses(is_white, broad)
                if not is_moved[1][0] and (broad[(1, 7)] == 0 and broad[(2, 7)] == 0 and broad[(3, 7)] == 0) and pre_castling(broad, enemies, [(1, 7), (2, 7), (3, 7)]):
                    all_move.append([(4, 7), (2, 7)])
                elif not is_moved[1][1] and (broad[(5, 7)] == 0 and broad[(6, 7)] == 0) and pre_castling(broad, enemies, [(5, 7), (6, 7)]):
                    all_move.append([(4, 7), (6, 7)])

        for index, value in zip(indices, values):
            possible_moves = PIECE[abs(value)].get_possible_move(tuple(index), broad)

            for move in [move for moves in possible_moves for move in moves]:
                all_move.append([tuple(index), move])

    else:
        if break_check[0] == 'only King move':
            break_check = []
            for index, value in zip(indices, values):
                if abs(value) == 1:
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
                if len(break_check) != 0:
                    return ['only King move']
                break_check.extend(PIECE[abs(value)].to_opp_king(tuple(index), take))
    
    return break_check
        
def piece_move(broad: ndarray, old_pos, new_pos, is_moved=[None, None]):
    is_white = True
    if broad[old_pos] < 0:
        is_white = False

    if abs(broad[old_pos]) == 1 and abs(new_pos[0] - old_pos[0]) == 2:
        if new_pos == (2, 0):
            broad[(3, 0)] = 5
            broad[(0, 0)] = 0
        elif new_pos == (6, 0):
            broad[(5, 0)] = 5
            broad[(7, 0)] = 0
        elif new_pos == (2, 7):
            broad[(3, 7)] = -5
            broad[(0, 7)] = 0
        elif new_pos == (6, 7):
            broad[(5, 7)] = -5
            broad[(7, 7)] = 0

    broad[new_pos] = broad[old_pos]
    broad[old_pos] = 0

    if abs(broad[new_pos]) == 1:
        if is_white and is_moved[0] is not None:
            is_moved[0] = None
        elif not is_white and is_moved[1] is not None:
            is_moved[1] = None

    if abs(broad[new_pos]) == 5:
        if is_moved[0] is not None and is_white:
            if old_pos == (0, 0):
                is_moved[0][0] = True
            elif old_pos == (7, 0):
                is_moved[0][1] = True
            if False not in is_moved[0]:
                is_moved[0] = None
        elif is_moved[1] is not None and not is_white:
            if old_pos == (0, 7):
                is_moved[1][0] = True
            elif old_pos == (7, 7):
                is_moved[1][1] = True
            if False not in is_moved[1]:
                is_moved[1] = None

    if abs(broad[new_pos]) == 6 and (new_pos[1] == 7 or new_pos[1] == 0):
        broad[new_pos] = 2 * (broad[new_pos] / abs(broad[new_pos]))

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

    KING_EARLY_TABLE = np.array([
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [ 20,  20,  00,  00,  00,  00,  20,  20],
        [ 20,  30,  10,  00,  00,  10,  30,  20]
    ])

    KING_END_TABLE = np.array([
        [-50, -40, -30, -20, -20, -30, -40, -50],
        [-30, -20, -10,  00,  00, -10, -20, -30],
        [-30, -10,  20,  30,  30,  20, -10, -30],
        [-30, -10,  30,  40,  40,  30, -10, -30],
        [-30, -10,  30,  40,  40,  30, -10, -30],
        [-30, -10,  20,  30,  30,  20, -10, -30],
        [-30, -30, -10,  00,  00, -10, -30, -30],
        [-50, -30, -30, -30, -30, -30, -30, -50]
    ])

    @staticmethod
    def evaluate(broad: ndarray):
        broad_score = ScoreSupporter.broad_score(broad)

        queen_score = ScoreSupporter.piece_score(broad, ScoreSupporter.QUEEN_TABLE, Queen)
        bishop_score = ScoreSupporter.piece_score(broad, ScoreSupporter.BISHOP_TABLE, Bishop)
        knight_score = ScoreSupporter.piece_score(broad, ScoreSupporter.KNIGHT_TABLE, Knight)
        rook_score = ScoreSupporter.piece_score(broad, ScoreSupporter.ROOK_TABLE, Rook)
        pawn_score = ScoreSupporter.piece_score(broad, ScoreSupporter.PAWN_TABLE, Pawn)

        if np.count_nonzero(broad > 0) > 12:
            king_score = ScoreSupporter.piece_score(broad, ScoreSupporter.KING_EARLY_TABLE, King)
        else:
            king_score = ScoreSupporter.piece_score(broad, ScoreSupporter.KING_END_TABLE, King)

        return broad_score + queen_score + bishop_score + knight_score + rook_score + pawn_score + king_score

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
    def move(broad: ndarray, break_check: list=[], is_moved = [[False, False], [False, False]], is_white=False):
        curr_pos = 0
        best_move = 0
        best_score = AI.INFINITE
        if is_white:
            best_score = -AI.INFINITE

        all_move = get_all_move(broad, is_white, break_check, is_moved)
        
        for old_pos, new_pos in all_move:
            broad_clone = broad.copy()

            break_check = piece_move(broad_clone, old_pos, new_pos, is_moved)
            score = AI.alpha_beta(2, broad_clone, -AI.INFINITE, AI.INFINITE, True, break_check, is_moved)

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
    def alpha_beta(depth: int, broad: ndarray, alpha, beta, maximizing: bool, break_check=[], is_moved=[None, None]):
        if depth == 0:
            return ScoreSupporter.evaluate(broad)
        if maximizing:
            best_score = -AI.INFINITE

            for old_pos, new_pos in get_all_move(broad, True, break_check, is_moved):
                broad_clone = broad.copy()

                break_check = piece_move(broad_clone, old_pos, new_pos)
                best_score = max(best_score, AI.alpha_beta(depth - 1, broad_clone, alpha, beta, False, break_check, is_moved))

                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            
            return best_score

        else:
            best_score = AI.INFINITE
            for old_pos, new_pos in get_all_move(broad, False, break_check, is_moved):
                broad_clone = broad.copy()

                break_check = piece_move(broad_clone, old_pos, new_pos)
                best_score = min(best_score, AI.alpha_beta(depth - 1, broad_clone, alpha, beta, True, break_check, is_moved))

                beta = min(alpha, best_score)
                if beta <= alpha:
                    break
            
            return best_score

if __name__ == '__main__':
    broad = np.array([
        [ 0,  0,  0, -1,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  5,  0,  5,  0,  0,  0],
        [ 0,  0,  0,  0,  3,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  6,  0,  0,  0],
        [ 1,  0,  6,  0,  0,  0,  0,  0],
        [ 0,  6,  0,  0,  0,  0,  0,  0]
    ])
    start_time = time.time()  # Ghi lại thời gian bắt đầu
    print(AI.move(broad, [], [None, None]))
    end_time = time.time()  # Ghi lại thời gian kết thúc

    print(end_time - start_time)
    
    