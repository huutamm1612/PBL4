import numpy as np
from numpy import ndarray
from ai import *
from chess_piece import *

class Chess:
    def __init__(self):
        self.broad = np.array([
            [ 5,  6,  0,  0,  0,  0, -6, -5],
            [ 4,  6,  0,  0,  0,  0, -6, -4],
            [ 3,  6,  0,  0,  0,  0, -6, -3],
            [ 2,  6,  0,  0,  0,  0, -6, -2],
            [ 1,  6,  0,  0,  0,  0, -6, -1],
            [ 3,  6,  0,  0,  0,  0, -6, -3],
            [ 4,  6,  0,  0,  0,  0, -6, -4],
            [ 5,  6,  0,  0,  0,  0, -6, -5], 
        ])
        self.break_check = []
        self.is_white_checked = None
        
    def get_all_possible_moves(self, is_white: bool):
        all_move = []

        if is_white:
            indices = np.array(np.where(self.broad > 0), dtype=np.int16).T
            values = self.broad[self.broad > 0]
        else:
            indices = np.array(np.where(self.broad < 0), dtype=np.int16).T
            values = self.broad[self.broad < 0]

        if self.is_white_checked is None:
            for index, value in zip(indices, values):
                possible_moves = PIECE[abs(value)].get_possible_move(tuple(index), self.broad)

                for move in [move for moves in possible_moves for move in moves]:
                    all_move.append([tuple(index), move])
            
        