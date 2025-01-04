import numpy as np
from numpy import ndarray
from ai import AI
from chess_piece import *

def to_string(chess_piece):
    s = 'b'
    if chess_piece.is_white:
        s = 'w'

    if type(chess_piece) is King:
        s += 'k'
    elif type(chess_piece) is Queen:
        s += 'q'
    elif type(chess_piece) is Bishop:
        s += 'b'
    elif type(chess_piece) is Knight:
        s += 'n'
    elif type(chess_piece) is Rook:
        s += 'r'
    elif type(chess_piece) is Pawn:
        s += 'p'

    return s + str(chess_piece.pos[0] + 1) + str(chess_piece.pos[1] + 1)

class Player:
    def __init__(self, client_address, is_white, username='Guess') -> None:
        self.client_address = client_address
        self.is_white = is_white
        self.username = username

        self.curr = ()

class Game:
    def __init__(self, players: Player, time=600, play_com=False) -> None:
        self.game_init()
        
        self.all_move_info = []
        self.players = players 
        self.time = time
        self.play_com = play_com
        self.break_check = []
        
        self.white_turn = True
        self.is_white_checked = None

    def game_init(self):
        self.chess_pieces = [
            King((4, 0), True),
            Queen((3, 0), True),
            Bishop((2, 0), True),
            Bishop((5, 0), True),
            Knight((1, 0), True),
            Knight((6, 0), True),
            Rook((0, 0), True),
            Rook((7, 0), True),
            Pawn((0, 1), True),
            Pawn((1, 1), True),
            Pawn((2, 1), True),
            Pawn((3, 1), True),
            Pawn((4, 1), True),
            Pawn((5, 1), True),
            Pawn((6, 1), True),
            Pawn((7, 1), True),
            
            King((4, 7), False),
            Queen((3, 7), False),
            Bishop((2, 7), False),
            Bishop((5, 7), False),
            Knight((1, 7), False),
            Knight((6, 7), False),
            Rook((0, 7), False),
            Rook((7, 7), False),
            Pawn((0, 6), False),
            Pawn((1, 6), False),
            Pawn((2, 6), False),
            Pawn((3, 6), False),
            Pawn((4, 6), False),
            Pawn((5, 6), False),
            Pawn((6, 6), False),
            Pawn((7, 6), False),
        ]
        
        self.matrix = np.zeros((8, 8), dtype=np.int8)
        for chess_piece in self.chess_pieces:
            self.matrix[chess_piece.pos] = number_from_chess(chess_piece)

    def get_chess_piece_from_pos(self, pos):
        for chess_piece in self.chess_pieces:
            if chess_piece.pos == pos:
                return chess_piece
        
        return None
    
    def pre_castling(self, rook_pos, enemies, pre_moves):
        rook = self.get_chess_piece_from_pos(rook_pos)
        
        if rook is not None and type(rook) is Rook and not rook.is_moved:
            if rook_pos == (0, 0):
                poses = [(1, 0), (2, 0), (3, 0)]
                pre = (2, 0)
            elif rook_pos == (7, 0):
                poses = [(5, 0), (6, 0)]
                pre = (6, 0)
            elif rook_pos == (0, 7):
                poses = [(1, 7), (2, 7), (3, 7)]
                pre = (2, 7)
            elif rook_pos == (7, 7):
                poses = [(5, 7), (6, 7)]
                pre = (6, 7)

            can_castle = True
            for pos in poses:
                if self.get_chess_piece_from_pos(pos) is None:
                    for enemy in enemies:
                        if get_chess_from_number(abs(self.matrix[enemy])).is_attack_at(enemy, pos, self.matrix):
                            can_castle = False
                            break
                else:
                    can_castle = False
                    break
            
            if can_castle:
                pre_moves.append(pre)

    def get_player(self, client_address):
        for p in self.players:
            if p.client_address == client_address:
                player = p

        return player   
    
    def is_check(self, player):
        self.break_check = []
        for chess in self.chess_pieces:
            if chess.is_white == player.is_white:
                _, pos_can_take = chess.possible_moves(self.matrix)
                for pos in pos_can_take:
                    if type(self.get_chess_piece_from_pos(pos)) is King:
                        self.break_check.extend(chess.way_to_opp_king(pos))
        
        return len(self.break_check) != 0

    def out(self, client_address):
        self.get_player(client_address).curr = None
    
    def pos_can_move(self, pos, client_address):
        chess_piece = self.get_chess_piece_from_pos(pos)
        pos_can_moves, pos_can_takes = chess_piece.possible_moves(self.matrix)
        player = self.get_player(client_address)
        player.curr = pos
        
        # hiện không có chiếu
        if self.is_white_checked is None:
            if type(chess_piece) is King and not chess_piece.is_moved:
                enemies = get_opp_chesses(player.is_white, self.matrix)
                if player.is_white:
                    self.pre_castling((0, 0), enemies, pos_can_moves)
                    self.pre_castling((7, 0), enemies, pos_can_moves)
                
                else:
                    self.pre_castling((0, 7), enemies, pos_can_moves)
                    self.pre_castling((7, 7), enemies, pos_can_moves)

            return [pos_can_moves, pos_can_takes]
        
        else:
            if self.is_white_checked == player.is_white:
                return [pos_can_moves, pos_can_takes]
            
            can_move = []
            can_take = []
            
            if type(chess_piece) is not King:
                for pos in pos_can_moves:
                    if pos in self.break_check and self.matrix[pos] == 0:
                        can_move.append(pos)

                for pos in pos_can_takes:
                    if pos in self.break_check:
                        can_take.append(pos)

            else:
                enemies = get_opp_chesses(player.is_white, self.matrix)
                for pos in pos_can_moves:
                    can = True
                    for enemy in enemies:
                        if get_chess_from_number(abs(self.matrix[enemy])).is_attack_at(enemy, pos, self.matrix):
                            can = False
                    if can:
                        can_move.append(pos)
                
                for pos in pos_can_takes:
                    can = True
                    for enemy in enemies:
                        if get_chess_from_number(abs(self.matrix[enemy])).is_attack_at(enemy, pos, self.matrix):
                            can = False
                            break
                    if can:
                        can_take.append(pos)

            return [can_move, can_take]
            
    def move(self, goal, client_address):
        player = self.get_player(client_address)
        chess_piece = self.get_chess_piece_from_pos(player.curr)

        if self.white_turn == player.is_white:
            self.all_move_info.append(str(chess_piece) + pos_to_index(goal))
            self.move_chess(player.curr, goal)

            if self.is_check(player):
                self.is_white_checked = self.white_turn
                if self.is_checkmate(player):
                    self.all_move_info[-1] += '#'
                else:
                    self.all_move_info[-1] += '+'
            else:
                self.is_white_checked = None
        
            player.curr = None
            self.white_turn = not self.white_turn
            return self.all_move_info[-1]

    def move_chess(self, start, goal):
        chess_piece = self.get_chess_piece_from_pos(start)

        if type(chess_piece) is King and not chess_piece.is_moved and abs(start[0] - goal[0]) == 2:
            self.all_move_info = self.all_move_info[:-1]
            if goal == (2, 0):
                self.move_chess((0, 0), (3, 0))
                self.all_move_info.append('wO-O-O')
            elif goal == (6, 0):
                self.move_chess((7, 0), (5, 0))
                self.all_move_info.append('wO-O')
            elif goal == (2, 7):
                self.move_chess((0, 7), (3, 7))
                self.all_move_info.append('bO-O-O')
            elif goal == (6, 7):
                self.move_chess((7, 7), (5, 7))
                self.all_move_info.append('bO-O')
                
        self.matrix[start], self.matrix[goal] = self.matrix[goal], self.matrix[start]
        chess_piece.pos = goal

        if type(chess_piece) in [King, Pawn, Rook]:
            chess_piece.is_moved = True
            if type(chess_piece) is Pawn and (chess_piece.pos[1] == 7 or chess_piece.pos[1] == 0):
                self.promote(chess_piece)

    def promote(self, pawn_piece):
        self.chess_pieces.remove(pawn_piece)
        self.chess_pieces.append(Queen(pawn_piece.pos, pawn_piece.is_white))
        self.matrix[pawn_piece.pos] = 2 * (self.matrix[pawn_piece.pos] / abs(self.matrix[pawn_piece.pos]))

    def get_is_moved(self):
        is_moved = [
            [False, False],
            [False, False]
        ]

        for piece in self.chess_pieces:
            if type(piece) is Rook:
                if piece.is_moved:
                    if piece.pos == (0, 0):
                        is_moved[0][0] = True
                    elif piece.pos == (7, 0):
                        is_moved[0][1] = True
                    if piece.pos == (0, 7):
                        is_moved[1][0] = True
                    elif piece.pos == (7, 7):
                        is_moved[1][1] = True
        
        if False not in is_moved[0]:
            is_moved[0] = None
        if False not in is_moved[1]:
            is_moved[1] = None
        
        for piece in self.chess_pieces:
            if type(piece) is King:
                if piece.is_moved:
                    if piece.is_white:
                        is_moved[0] = None
                    else:
                        is_moved[1] = None

        return is_moved

    def ai_move(self):
        is_moved = self.get_is_moved()
        try:
            start, goal = AI.move(self.matrix, self.break_check, is_moved)
        except:
            print(AI.move(self.matrix, self.break_check, is_moved))
            print(self.matrix, self.break_check, is_moved)
            
        chess_piece = self.get_chess_piece_from_pos(start)
        if self.get_chess_piece_from_pos(goal) is not None:
            self.all_move_info.append(str(chess_piece) + 'x' + pos_to_index(goal))
            self.chess_pieces.remove(self.get_chess_piece_from_pos(goal))
            self.matrix[goal] = 0
        else:
            self.all_move_info.append(str(chess_piece) + pos_to_index(goal))

        self.move_chess(start, goal)
        if self.is_check(self.players[1]):
            self.is_white_checked = self.white_turn
            if self.is_checkmate(self.players[1]):
                self.all_move_info[-1] += '#'
            else:
                self.all_move_info[-1] += '+'
        else:
            self.is_white_checked = None
    
        self.white_turn = not self.white_turn
        return self.all_move_info[-1]

    def take(self, goal, client_address):
        player = self.get_player(client_address)
        chess_piece = self.get_chess_piece_from_pos(player.curr)

        if self.white_turn == player.is_white:
            self.all_move_info.append(str(chess_piece) + 'x' + pos_to_index(goal))

            self.chess_pieces.remove(self.get_chess_piece_from_pos(goal))
            self.matrix[goal] = 0
            self.move_chess(player.curr, goal)

            if self.is_check(player):
                self.is_white_checked = self.white_turn
                if self.is_checkmate(player):
                    self.all_move_info[-1] += '#'
                else:
                    self.all_move_info[-1] += '+'
            else:
                self.is_white_checked = None
        
            player.curr = None
            self.white_turn = not self.white_turn
            return self.all_move_info[-1]

    def is_checkmate(self, player):
        opp = self.players[1 - self.players.index(player)]
        for chess_piece in self.chess_pieces:
            if chess_piece.is_white == opp.is_white:
                can_move = self.pos_can_move(chess_piece.pos, opp.client_address)
                if len(can_move[0]) != 0 or len(can_move[1]) != 0:
                    return False
                
        return True