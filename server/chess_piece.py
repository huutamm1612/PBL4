from abc import ABC, abstractmethod
import numpy as np
from numpy import ndarray

def pos_to_index(pos):
    return chr(pos[0] + 97) + str(pos[1] + 1)

def get_chess_from_number(number):
    if abs(number) == 1:
        return King
    elif abs(number) == 2:
        return Queen
    elif abs(number) == 3:
        return Bishop
    elif abs(number) == 4:
        return Knight
    elif abs(number) == 5:
        return Rook
    elif abs(number) == 6:
        return Pawn
    else:
        raise "number error"
    
def number_from_chess(chess_piece):
    n = -1
    if chess_piece.is_white:
        n = 1

    if type(chess_piece) is Queen:
        n *= 2
    elif type(chess_piece) is Bishop:
        n *= 3
    elif type(chess_piece) is Knight:
        n *= 4
    elif type(chess_piece) is Rook:
        n *= 5
    elif type(chess_piece) is Pawn:
        n *= 6

    return n

# hàm trả về vị trí của tất cả quân cờ của đối thủ
def get_opp_chesses(is_white, matrix: ndarray):
    if is_white:
        opp_chesses = np.where(matrix < 0)
        opp_chesses = list(zip(opp_chesses[0], opp_chesses[1]))
    else:
        opp_chesses = np.where(matrix > 0)
        opp_chesses = list(zip(opp_chesses[0], opp_chesses[1]))
    return opp_chesses

# hàm kiểm tra xem quân cờ ở vị trí start có thể di chuyển đến vị trí goal được hay không
# ví dụ như quân cờ đó đang bảo vệ vua khỏi một quân cờ của đối thủ thì không thể di chuyển đễn hướng khác được
def can_move(start, goal, matrix: ndarray):
    # start: vị trí ban đầu của quân cờ
    # goal: đích đến của quân cờ

    if matrix[start] > 0:
        is_white = True
        if matrix[start] == 1:
            king_pos = goal
        else:
            coor = np.where(matrix == 1)
            king_pos = (coor[0][0], coor[1][0])
    else:
        is_white = False
        if matrix[start] == -1:
            king_pos = goal
        else:
            coor = np.where(matrix == -1)
            king_pos = (coor[0][0], coor[1][0])

    opp_chesses = get_opp_chesses(is_white, matrix)
    tmp1 = matrix[goal]
    tmp2 = matrix[start]

    matrix[goal] = tmp2
    matrix[start] = 0
    for opp_chess in opp_chesses:
        if opp_chess != goal and get_chess_from_number(abs(matrix[opp_chess])).is_attack_at(opp_chess, king_pos, matrix):
            matrix[goal] = tmp1
            matrix[start] = tmp2
            return False
        
    matrix[goal] = tmp1
    matrix[start] = tmp2
    return True

class ChessPiece(ABC):
    def __init__(self, pos: tuple, is_white: bool) -> None:
        # vị trí của quân cờ 'self'
        self.pos = pos
        # quân cờ 'self' có phải quân trắng hay không
        self.is_white = is_white

    @staticmethod
    @abstractmethod
    def is_attack_at(pos: tuple, goal: tuple, matrix: ndarray) -> bool:
        # Kiểm tra xem quân cờ ở vị trí 'pos' có đang tấn công tại vị trí 'goal' hay không
        pass

    @staticmethod
    @abstractmethod
    def get_possible_move(pos: tuple, matrix: ndarray):
        pass

    @staticmethod
    @abstractmethod
    def to_opp_king(pos: tuple, opp_king_pos:tuple):
        pass

    @abstractmethod
    def way_to_opp_king(self, opp_king_pos: tuple) -> list:
        # Trả về tọa độ các vị trí từ quân cờ 'self' đến quân vua của đối thủ
        # Đã thỏa mãn rằng quân 'self' đang tấn công vua đối thủ
        # opp_king_pos: vị trí của vua đối thủ
        pass

    @abstractmethod
    def possible_moves(self, matrix: ndarray) -> list:
        # Trả về tất cả các vị trí mà quân cờ 'self' có thể đi đến (kể cả ăn quân đối thủ)
        pass

class King(ChessPiece):
    around = (
        [-1, -1], [-1, 0], [-1, 1],
        [0, -1], [0, 1],
        [1, -1], [1, 0], [1, 1]
    )

    def __init__(self, pos: tuple, is_white: bool) -> None:
        super().__init__(pos, is_white)
        # Kiểm tra xem quân vua đã di chuyển hay chưa, để có thể nhập thành (castle)
        self.is_moved = False

    def __str__(self) -> str:
        if self.is_white:
            return 'wK' + pos_to_index(self.pos)
        return 'bK' + pos_to_index(self.pos)
            
    @staticmethod
    def to_opp_king(pos, opp_king_pos):
        return []

    @staticmethod
    def is_attack_at(pos: tuple, goal: tuple, matrix: ndarray) -> bool:
        for index in King.around:
            if (pos[0] + index[0], pos[1] + index[1]) == goal:
                return True
        
        return False
    
    @staticmethod
    def get_possible_move(pos: tuple, matrix: ndarray):
        pos_can_moves = []
        pos_can_takes = []

        for index in King.around:
            new_pos = (pos[0] + index[0], pos[1] + index[1])
            if new_pos[0] >= 0 and new_pos[0] < 8 and new_pos[1] >= 0 and new_pos[1] < 8:
                if can_move(pos, new_pos, matrix):
                    if matrix[new_pos] == 0:
                        pos_can_moves.append(new_pos)
                    elif matrix[pos] * matrix[new_pos] < 0:
                        pos_can_takes.append(new_pos)
                
        return [pos_can_moves, pos_can_takes]

    def way_to_opp_king(self, opp_king_pos: tuple) -> list:
        return []
    
    def possible_moves(self, matrix: ndarray) -> list:
        return King.get_possible_move(self.pos, matrix)

class Queen(ChessPiece):
    def __init__(self, pos: tuple, is_white: bool) -> None:
        super().__init__(pos, is_white)


    def __str__(self) -> str:
        if self.is_white:
            return 'wQ' + pos_to_index(self.pos)
        return 'bQ' + pos_to_index(self.pos)
    
    @staticmethod
    def to_opp_king(pos, opp_king_pos):
        r = Rook.to_opp_king(pos, opp_king_pos)[1:]
        r.extend(Bishop.to_opp_king(pos, opp_king_pos))
        return r

    @staticmethod
    def is_attack_at(pos: tuple, goal: tuple, matrix: ndarray) -> bool:
        return Bishop.is_attack_at(pos, goal, matrix) or Rook.is_attack_at(pos, goal, matrix)
    
    @staticmethod
    def get_possible_move(pos: tuple, matrix: ndarray):
        possible_move1 = Bishop.get_possible_move(pos, matrix)
        possible_move2 = Rook.get_possible_move(pos, matrix)
        possible_move1[0].extend(possible_move2[0])
        possible_move1[1].extend(possible_move2[1])
        
        return possible_move1

    def way_to_opp_king(self, opp_king_pos: tuple) -> list:
        return Queen.to_opp_king(self.pos, opp_king_pos)
    
    def possible_moves(self, matrix: ndarray) -> list:
        return Queen.get_possible_move(self.pos, matrix)

class Bishop(ChessPiece):
    def __init__(self, pos: tuple, is_white: bool) -> None:
        super().__init__(pos, is_white)

    def __str__(self) -> str:
        if self.is_white:
            return 'wB' + pos_to_index(self.pos)
        return 'bB' + pos_to_index(self.pos)
    
    @staticmethod
    def to_opp_king(pos, opp_king_pos):        
        result = [pos]
        if opp_king_pos[0] > pos[0] and opp_king_pos[1] > pos[1]:
            for i in range(1, 8):
                possition = (pos[0] + i, pos[1] + i)
                if opp_king_pos == possition:
                    return result
                result.append(possition)

        elif opp_king_pos[0] > pos[0] and opp_king_pos[1] < pos[1]:
            for i in range(1, 8):
                possition = (pos[0] + i, pos[1] - i)
                if opp_king_pos == possition:
                    return result
                result.append(possition)

        elif opp_king_pos[0] < pos[0] and opp_king_pos[1] < pos[1]:
            for i in range(1, 8):
                possition = (pos[0] - i, pos[1] - i)
                if opp_king_pos == possition:
                    return result
                result.append(possition)

        elif opp_king_pos[0] < pos[0] and opp_king_pos[1] > pos[1]:
            for i in range(1, 8):
                possition = (pos[0] - i, pos[1] + i)
                if opp_king_pos == possition:
                    return result
                result.append(possition)

        return result
    
    @staticmethod
    def is_attack_at(pos: tuple, goal: tuple, matrix: ndarray) -> bool:
        # Chéo lên bên phải
        for i in range(1, 8):
            new_pos = (pos[0] + i, pos[1] + i)
            if new_pos == goal:
                return True
            if new_pos[0] == 8 or new_pos[1] == 8 or matrix[new_pos] != 0:
                break
        
        # Chéo lên bên trái
        for i in range(1, 8):
            new_pos = (pos[0] + i, pos[1] - i)
            if new_pos == goal:
                return True
            if new_pos[0] == 8 or new_pos[1] == -1 or matrix[new_pos] != 0:
                break
            
        # Chéo xuống bên phải
        for i in range(1, 8):
            new_pos = (pos[0] - i, pos[1] + i)
            if new_pos == goal:
                return True
            if new_pos[0] == -1 or new_pos[1] == 8 or matrix[new_pos] != 0:
                break
            
        # Chéo xuống bên trái
        for i in range(1, 8):
            new_pos = (pos[0] - i, pos[1] - i)
            if new_pos == goal:
                return True
            if new_pos[0] == -1 or new_pos[1] == -1 or matrix[new_pos] != 0:
                break

        return False
    
    @staticmethod
    def get_possible_move(pos: tuple, matrix: ndarray):
        pos_can_moves = []
        pos_can_takes = []

        for i in range(1, 8):
            new_pos = (pos[0] + i, pos[1] + i)
            if new_pos[0] == 8 or new_pos[1] == 8 or matrix[new_pos] * matrix[pos] > 0:
                break
            if can_move(pos, new_pos, matrix):
                if matrix[new_pos] == 0:
                    pos_can_moves.append(new_pos)
                    continue
                elif matrix[new_pos] * matrix[pos] < 0:
                    pos_can_takes.append(new_pos)
                break

        for i in range(1, 8):
            new_pos = (pos[0] + i, pos[1] - i)
            if new_pos[0] == 8 or new_pos[1] == -1 or matrix[new_pos] * matrix[pos] > 0:
                break
            if can_move(pos, new_pos, matrix):
                if matrix[new_pos] == 0:
                    pos_can_moves.append(new_pos)
                    continue
                elif matrix[new_pos] * matrix[pos] < 0:
                    pos_can_takes.append(new_pos)
                break

        for i in range(1, 8):
            new_pos = (pos[0] - i, pos[1] - i)
            if new_pos[0] == -1 or new_pos[1] == -1 or matrix[new_pos] * matrix[pos] > 0:
                break
            if can_move(pos, new_pos, matrix):
                if matrix[new_pos] == 0:
                    pos_can_moves.append(new_pos)
                    continue
                elif matrix[new_pos] * matrix[pos] < 0:
                    pos_can_takes.append(new_pos)
                break

        for i in range(1, 8):
            new_pos = (pos[0] - i, pos[1] + i)
            if new_pos[0] == -1 or new_pos[1] == 8 or matrix[new_pos] * matrix[pos] > 0:
                break
            if can_move(pos, new_pos, matrix):
                if matrix[new_pos] == 0:
                    pos_can_moves.append(new_pos)
                    continue
                elif matrix[new_pos] * matrix[pos] < 0:
                    pos_can_takes.append(new_pos)
                break

        return [pos_can_moves, pos_can_takes]

    def way_to_opp_king(self, opp_king_pos: tuple) -> list:
        return Bishop.to_opp_king(self.pos, opp_king_pos)
    
    def possible_moves(self, matrix: ndarray) -> list:
        return Bishop.get_possible_move(self.pos, matrix)

class Knight(ChessPiece):
    around =(
        (-2, -1), (-2, 1), (2, -1), (2, 1),
        (-1, -2), (1, -2), (-1, 2), (1, 2)
    )

    def __init__(self, pos: tuple, is_white: bool) -> None:
        super().__init__(pos, is_white)

    def __str__(self) -> str:
        if self.is_white:
            return 'wN' + pos_to_index(self.pos)
        return 'bN' + pos_to_index(self.pos)
    
    @staticmethod
    def to_opp_king(pos, opp_king_pos):
        return [pos]

    @staticmethod
    def is_attack_at(pos: tuple, goal: tuple, matrix: ndarray) -> bool:
        for index in Knight.around:
            new_pos = (pos[0] + index[0], pos[1] + index[1])
            if new_pos == goal:
                return True

        return False
    
    @staticmethod
    def get_possible_move(pos: tuple, matrix: ndarray):
        pos_can_moves = []
        pos_can_takes = []
        
        for index in Knight.around:
            new_pos = (pos[0] + index[0], pos[1] + index[1])
            if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] > 7 or new_pos[1] > 7:
                continue

            if can_move(pos, new_pos, matrix):
                if matrix[new_pos] == 0:
                    pos_can_moves.append(new_pos)
                elif matrix[new_pos] * matrix[pos] < 0:
                    pos_can_takes.append(new_pos)

        return [pos_can_moves, pos_can_takes]          

    def way_to_opp_king(self, opp_king_pos: tuple) -> list:
        return [self.pos]
    
    def possible_moves(self, matrix: ndarray) -> list:
        return Knight.get_possible_move(self.pos, matrix)

class Rook(ChessPiece):
    def __init__(self, pos: tuple, is_white: bool) -> None:
        super().__init__(pos, is_white)
        # Kiểm tra xem quân vua đã di chuyển hay chưa, để có thể nhập thành (castle)
        self.is_moved = False

    def __str__(self) -> str:
        if self.is_white:
            return 'wR' + pos_to_index(self.pos)
        return 'bR' + pos_to_index(self.pos)
    
    @staticmethod
    def to_opp_king(pos, opp_king_pos):
        result = [pos]

        if opp_king_pos[0] > pos[0] and opp_king_pos[1] == pos[1]:
            for i in range(1, 8):
                position = (pos[0] + i, pos[1])
                if position == opp_king_pos:
                    return result
                result.append(position)
        
        elif opp_king_pos[0] < pos[0] and opp_king_pos[1] == pos[1]:
            for i in range(1, 8):
                position = (pos[0] - i, pos[1])
                if position == opp_king_pos:
                    return result
                result.append(position)

        elif opp_king_pos[1] > pos[1] and opp_king_pos[0] == pos[0]:
            for i in range(1, 8):
                position = (pos[0], pos[1] + i)
                if position == opp_king_pos:
                    return result
                result.append(position)

        elif opp_king_pos[1] < pos[1] and opp_king_pos[0] == pos[0]:
            for i in range(1, 8):
                position = (pos[0], pos[1] - i)
                if position == opp_king_pos:
                    return result
                result.append(position)

        return result

    @staticmethod
    def is_attack_at(pos: tuple, goal: tuple, matrix: ndarray) -> bool:
        if goal[0] > pos[0] and goal[1] == pos[1]:
            for i in range(1, 8):
                new_pos = (pos[0] + i, pos[1])
                if new_pos == goal:
                    return True
                if new_pos[0] == 8 or matrix[new_pos] != 0:
                    break
        
        if goal[0] < pos[0] and goal[1] == pos[1]:
            for i in range(1, 8):
                new_pos = (pos[0] - i, pos[1])
                if new_pos == goal:
                    return True
                if new_pos[0] == -1 or matrix[new_pos] != 0:
                    break
        
        if goal[1] > pos[1] and goal[0] == pos[0]:
            for i in range(1, 8):
                new_pos = (pos[0], pos[1] + i)
                if new_pos == goal:
                    return True
                if new_pos[1] == 8 or matrix[new_pos] != 0:
                    break
        
        if goal[1] < pos[1] and goal[0] == pos[0]:
            for i in range(1, 8):
                new_pos = (pos[0], pos[1] - i)
                if new_pos == goal:
                    return True
                if new_pos[1] == -1 or matrix[new_pos] != 0:
                    break
        
        return False
    
    @staticmethod
    def get_possible_move(pos: tuple, matrix: ndarray):
        pos_can_moves = []
        pos_can_takes = []

        for i in range(1, 8):
            new_pos = (pos[0] + i, pos[1])
            if new_pos[0] == 8 or matrix[new_pos] * matrix[pos] > 0:
                break
            if can_move(pos, new_pos, matrix):
                if matrix[new_pos] == 0:
                    pos_can_moves.append(new_pos)
                    continue
                elif matrix[new_pos] * matrix[pos] < 0:
                    pos_can_takes.append(new_pos)
                break
                    
        for i in range(1, 8):
            new_pos = (pos[0] - i, pos[1])
            if new_pos[0] == -1 or matrix[new_pos] * matrix[pos] > 0:
                break
            if can_move(pos, new_pos, matrix):
                if matrix[new_pos] == 0:
                    pos_can_moves.append(new_pos)
                    continue
                elif matrix[new_pos] * matrix[pos] < 0:
                    pos_can_takes.append(new_pos)
                break
                    
        for i in range(1, 8):
            new_pos = (pos[0], pos[1] + i)
            if new_pos[1] == 8 or matrix[new_pos] * matrix[pos] > 0:
                break
            if can_move(pos, new_pos, matrix):
                if matrix[new_pos] == 0:
                    pos_can_moves.append(new_pos)
                    continue
                elif matrix[new_pos] * matrix[pos] < 0:
                    pos_can_takes.append(new_pos)
                break
                    
        for i in range(1, 8):
            new_pos = (pos[0], pos[1] - i)
            if new_pos[1] == -1 or matrix[new_pos] * matrix[pos] > 0:
                break
            if can_move(pos, new_pos, matrix):
                if matrix[new_pos] == 0:
                    pos_can_moves.append(new_pos)
                    continue
                elif matrix[new_pos] * matrix[pos] < 0:
                    pos_can_takes.append(new_pos)
                break

        return [pos_can_moves, pos_can_takes]

    def way_to_opp_king(self, opp_king_pos: tuple) -> list:
        return Rook.to_opp_king(self.pos, opp_king_pos)
    
    def possible_moves(self, matrix: ndarray) -> list:
        return Rook.get_possible_move(self.pos, matrix)

class Pawn(ChessPiece):
    def __init__(self, pos: tuple, is_white: bool) -> None:
        super().__init__(pos, is_white)
        # Kiểm tra xem quân vua đã di chuyển hay chưa, để có thể đi hai nước ở lần đi đầu tiên
        self.is_moved = False

    def __str__(self) -> str:
        if self.is_white:
            return 'wP' + pos_to_index(self.pos)
        return 'bP' + pos_to_index(self.pos)
    
    @staticmethod
    def to_opp_king(pos, opp_king_pos):
        return [pos]

    @staticmethod
    def is_attack_at(pos: tuple, goal: tuple, matrix: ndarray) -> bool:
        if matrix[pos] > 0:
            if (pos[0] + 1, pos[1] + 1) == goal:
                return True
            elif (pos[0] - 1, pos[1] + 1) == goal:
                return True
                        
        else:
            if (pos[0] + 1, pos[1] - 1) == goal:
                return True
            elif (pos[0] - 1, pos[1] - 1) == goal:
                return True
            
        return False
    
    @staticmethod
    def get_possible_move(pos: tuple, matrix: ndarray):
        pos_can_moves = []
        pos_can_takes = []

        if matrix[pos] > 0:
            new_pos = (pos[0], pos[1] + 1)
            if matrix[new_pos] == 0: 
                if can_move(pos, new_pos, matrix):
                    pos_can_moves.append(new_pos)
            
                if pos[1] == 1:
                    new_pos = (pos[0], pos[1] + 2)
                    if matrix[new_pos] == 0 and can_move(pos, new_pos, matrix):
                        pos_can_moves.append(new_pos)

            new_pos = (pos[0] + 1, pos[1] + 1)
            if 8 not in new_pos and matrix[new_pos] < 0 and can_move(pos, new_pos, matrix):
                pos_can_takes.append(new_pos)

            new_pos = (pos[0] - 1, pos[1] + 1)
            if -1 not in new_pos and matrix[new_pos] < 0 and can_move(pos, new_pos, matrix):
                pos_can_takes.append(new_pos)

        else:
            new_pos = (pos[0], pos[1] - 1)
            if matrix[new_pos] == 0:
                if can_move(pos, new_pos, matrix):
                    pos_can_moves.append(new_pos)
            
                if pos[1] == 6:
                    new_pos = (pos[0], pos[1] - 2)
                    if matrix[new_pos]  == 0 and can_move(pos, new_pos, matrix):
                        pos_can_moves.append(new_pos)

            new_pos = (pos[0] + 1, pos[1] - 1)
            if 8 not in new_pos and matrix[new_pos] > 0 and can_move(pos, new_pos, matrix):
                pos_can_takes.append(new_pos)

            new_pos = (pos[0] - 1, pos[1] - 1)
            if -1 not in new_pos and matrix[new_pos] > 0 and can_move(pos, new_pos, matrix):
                pos_can_takes.append(new_pos)

        return [pos_can_moves, pos_can_takes]

    def way_to_opp_king(self, opp_king_pos: tuple) -> list:
        return [self.pos]
    
    def possible_moves(self, matrix: ndarray) -> list:
        return Pawn.get_possible_move(self.pos, matrix)