import pygame
from .util import *

# wPb4b3 wPb2xe2
CHESS_POINT = {
    'Q' : 9,
    'B' : 3,
    'N' : 3,
    'R' : 5,
    'P' : 1,
}

class Chess(View):
    images = {
        'wK' : resize(pygame.image.load('client/images/chess_pieces/wk.png'), (CHESS_SIZE, CHESS_SIZE)),
        'wQ' : resize(pygame.image.load('client/images/chess_pieces/wq.png'), (CHESS_SIZE, CHESS_SIZE)),
        'wB' : resize(pygame.image.load('client/images/chess_pieces/wb.png'), (CHESS_SIZE, CHESS_SIZE)),
        'wN' : resize(pygame.image.load('client/images/chess_pieces/wn.png'), (CHESS_SIZE, CHESS_SIZE)),
        'wR' : resize(pygame.image.load('client/images/chess_pieces/wr.png'), (CHESS_SIZE, CHESS_SIZE)),
        'wP' : resize(pygame.image.load('client/images/chess_pieces/wp.png'), (CHESS_SIZE, CHESS_SIZE)),

        'bK' : resize(pygame.image.load('client/images/chess_pieces/bk.png'), (CHESS_SIZE, CHESS_SIZE)),
        'bQ' : resize(pygame.image.load('client/images/chess_pieces/bq.png'), (CHESS_SIZE, CHESS_SIZE)),
        'bB' : resize(pygame.image.load('client/images/chess_pieces/bb.png'), (CHESS_SIZE, CHESS_SIZE)),
        'bN' : resize(pygame.image.load('client/images/chess_pieces/bn.png'), (CHESS_SIZE, CHESS_SIZE)),
        'bR' : resize(pygame.image.load('client/images/chess_pieces/br.png'), (CHESS_SIZE, CHESS_SIZE)),
        'bP' : resize(pygame.image.load('client/images/chess_pieces/bp.png'), (CHESS_SIZE, CHESS_SIZE)),

        'wAvt' : resize(pygame.image.load('client/images/chess_pieces/wp.png'), (34, 34)),
        'bAvt' : resize(pygame.image.load('client/images/chess_pieces/bp.png'), (34, 34)),
        
        'swK' : resize(pygame.image.load('client/images/chess_pieces/wk.png'), (20, 20)),
        'swQ' : resize(pygame.image.load('client/images/chess_pieces/wq.png'), (20, 20)),
        'swB' : resize(pygame.image.load('client/images/chess_pieces/wb.png'), (20, 20)),
        'swN' : resize(pygame.image.load('client/images/chess_pieces/wn.png'), (20, 20)),
        'swR' : resize(pygame.image.load('client/images/chess_pieces/wr.png'), (20, 20)),
        'swP' : resize(pygame.image.load('client/images/chess_pieces/wp.png'), (20, 20)),

        'sbK' : resize(pygame.image.load('client/images/chess_pieces/bk.png'), (20, 20)),
        'sbQ' : resize(pygame.image.load('client/images/chess_pieces/bq.png'), (20, 20)),
        'sbB' : resize(pygame.image.load('client/images/chess_pieces/bb.png'), (20, 20)),
        'sbN' : resize(pygame.image.load('client/images/chess_pieces/bn.png'), (20, 20)),
        'sbR' : resize(pygame.image.load('client/images/chess_pieces/br.png'), (20, 20)),
        'sbP' : resize(pygame.image.load('client/images/chess_pieces/bp.png'), (20, 20)),
    }

    def __init__(self, user: User, surface: pygame.Surface = None) -> None:
        super().__init__(user, surface)
        self.chess_size = CHESS_SIZE
        self.broad_widht, self.broad_height = self.chess_size * 8, self.chess_size * 8
        self.broad_x, self.broad_y = 80, 80
        self.game_rect = pygame.Rect(self.broad_x, self.broad_y, self.broad_widht, self.broad_height)
        self.game_surface = self.surface.subsurface(self.game_rect)
        self.font = pygame.font.Font(None, 20)

        self.is_white = True
        self.is_white_view = True
        self.can_move = None
        self.all_move_info = []
        self.opp_info = None

        self.buttons = [
            Button((800, 0, 100, 50), id='spin', text='Home', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1)
        ]

        self.game_init()
        self.draw_broad()

    def game_init(self):
        self.all_chess_pieces = [
            'bR18', 'bN28', 'bB38', 'bQ48', 'bK58', 'bB68', 'bN78', 'bR88',
            'bP17', 'bP27', 'bP37', 'bP47', 'bP57', 'bP67', 'bP77', 'bP87',
            'wP12', 'wP22', 'wP32', 'wP42', 'wP52', 'wP62', 'wP72', 'wP82',
            'wR11', 'wN21', 'wB31', 'wQ41', 'wK51', 'wB61', 'wN71', 'wR81'
        ]

        self.point = 0
        self.pieces_taken = {
            'P' : 0,
            'B' : 0,
            'N' : 0,
            'R' : 0,
            'Q' : 0,
        }

        self.pieces_is_taken = {
            'P' : 0,
            'B' : 0,
            'N' : 0,
            'R' : 0,
            'Q' : 0,
        }

        self.possible_moves = []
        self.possible_takes = []
        self.highlight = []
        self.curr_position = ''

    def replay(self, move_infos):
        self.game_init()

        for move_info in move_infos:
            self.change_broad(move_info)
        
        self.draw_broad()

    def change_broad(self, move_info):
        if 'O' not in move_info:
            goal_pos = move_info[-2:]
            if not move_info[-1].isdigit():
                goal_pos = move_info[-3:-1]

            start_pos = pos_to_coor(move_info[2:4])
            goal_pos = pos_to_coor(goal_pos)

            chess = self.get_chess_piece(start_pos)

            if 'x' in move_info:
                piece_taken = self.get_chess_piece(goal_pos)
                point = CHESS_POINT[piece_taken[1]]
                if move_info[0] == 'w' and self.is_white or move_info[0] == 'b' and not self.is_white:
                    self.point += point
                    self.pieces_taken[piece_taken[1]] += 1
                elif move_info[0] == 'b' and self.is_white or  move_info[0] == 'w' and not self.is_white:
                    self.point -= point
                    self.pieces_is_taken[piece_taken[1]] += 1
                self.draw_player_info()

            self.remove_chess_piece_at(start_pos)
            self.remove_chess_piece_at(goal_pos)

            self.highlight = [start_pos, goal_pos]

            self.all_chess_pieces.append(chess[:2] + goal_pos)

        else:
            if move_info[1:] == 'O-O':
                if move_info[0] == 'w':
                    self.remove_chess_piece_at('wK51')
                    self.remove_chess_piece_at('wR81')
                    self.all_chess_pieces.extend(['wR61', 'wK71'])
                else:
                    self.remove_chess_piece_at('bK58')
                    self.remove_chess_piece_at('bR88')
                    self.all_chess_pieces.extend(['bR68', 'bK78'])

            else:
                if move_info[0] == 'w':
                    self.remove_chess_piece_at('wK51')
                    self.remove_chess_piece_at('wR11')
                    self.all_chess_pieces.extend(['wR41', 'wK31'])
                else:
                    self.remove_chess_piece_at('bK58')
                    self.remove_chess_piece_at('bR18')
                    self.all_chess_pieces.extend(['bR48', 'bK38'])

        if self.curr_position != '':
            self.select_cell(self.curr_position)
    
    def chess_pos_to_sreen_pos(self, pos):
        if self.is_white_view:
            return (int(pos[0]) - 1, 8 - int(pos[1]))
        return (8 - int(pos[0]), int(pos[1]) - 1)
    
    def mouse_pos_to_chess_pos(self, mouse_pos):
        x = (mouse_pos[0] - self.broad_x) // self.chess_size
        y = (mouse_pos[1] - self.broad_y) // self.chess_size

        if self.is_white_view:
            return str(x + 1) + str(8 - y)
        return str(8 - x) + str(y + 1)

    def draw_chess(self):
        for chess in self.all_chess_pieces:
            name = chess[:2]
            pos = self.chess_pos_to_sreen_pos(chess[2:])
                
            self.game_surface.blit(self.images[name], (pos[0] * self.chess_size, pos[1] * self.chess_size))

    def draw_broad(self):
        font = pygame.font.SysFont('Trebuchet MS', 17)
        for i in range(0, 8):
            for j in range(0, 8):
                if (i + j) % 2 == 1:
                    pygame.draw.rect(self.game_surface, COLOR['broad-green'], (i * self.chess_size, j * self.chess_size, self.chess_size, self.chess_size))
                else:
                    pygame.draw.rect(self.game_surface, COLOR['broad-white'], (i * self.chess_size, j * self.chess_size, self.chess_size, self.chess_size))

        if self.curr_position != '':
            self.highlight_broad(self.curr_position)
            
        for hl in self.highlight:
            self.highlight_broad(hl)

        for can_move in self.possible_moves:
            pos = self.chess_pos_to_sreen_pos(can_move)
            color = COLOR['broad-possible-white']
            if sum(pos) % 2 == 1:
                color = COLOR['broad-possible-green']
            pygame.draw.circle(self.game_surface, color, (pos[0] * self.chess_size + self.chess_size // 2, pos[1] * self.chess_size + self.chess_size // 2), 15)

        for can_take in self.possible_takes:
            pos = self.chess_pos_to_sreen_pos(can_take)
            color = COLOR['broad-possible-white']
            if sum(pos) % 2 == 1:
                color = COLOR['broad-possible-green']
            pygame.draw.circle(self.game_surface, color, (pos[0] * self.chess_size + self.chess_size // 2, pos[1] * self.chess_size + self.chess_size // 2), 37, 10)


        for j in range(8):
            text_color = COLOR['broad-green']
            if j % 2 == 1:
                text_color = COLOR['broad-white']
            
            index = str(j + 1)
            if self.is_white_view:
                index = str(8 - j)

            text = font.render(index, True, text_color)
            text_rect = text.get_rect(center=(10, j * self.chess_size + 13))

            self.game_surface.blit(text, text_rect)

        for i in range(8):
            text_color = COLOR['broad-green']
            if i % 2 == 0:
                text_color = COLOR['broad-white']

            index = chr((7 - i) + 97)
            if self.is_white_view:
                index = chr(i + 97)
            
            text = font.render(index, True, text_color)
            text_rect = text.get_rect(center=(i * self.chess_size + 70, 7 * self.chess_size + 67))

            self.game_surface.blit(text, text_rect)

        self.draw_chess()

    def highlight_broad(self, possition):
        pos = self.chess_pos_to_sreen_pos(possition)
        color = COLOR['broad-highlight-white']
        if sum(pos) % 2 == 1:
            color = COLOR['broad-highlight-green']

        pygame.draw.rect(self.game_surface, color, (pos[0] * self.chess_size, pos[1] * self.chess_size, self.chess_size,self.chess_size))

    def get_chess_piece(self, position):
        for chess in self.all_chess_pieces:
            if chess[2:] == position:
                return chess
            
        return None
    
    def remove_chess_piece_at(self, position):
        self.all_chess_pieces = [chess for chess in self.all_chess_pieces if not chess.endswith(position)]


    def get_mouse_pos(self, mouse_pos):
        mouse_x = mouse_pos[0] - HEADER_WIDTH
        mouse_y = mouse_pos[1]
        return (mouse_x, mouse_y)
    
    def select_cell(self, position):
        message = ''
        self.curr_position = ''
        chess_piece = self.get_chess_piece(position)

        if chess_piece is not None and (chess_piece[0] == 'w' and self.is_white or chess_piece[0] == 'b' and not self.is_white):
            self.curr_position = position
            message = 'select ' + position

        elif self.can_move is not None:
            if position in self.possible_moves:
                if self.can_move:
                    message = 'move ' + position
                else:
                    return
            elif position in self.possible_takes:
                if self.can_move:
                    message = 'take ' + position
                else:
                    return
            else:
                message = 'out ' + position
            
            self.possible_moves = []
            self.possible_takes = []

        self.user.client_socket.send('play'.encode())
        self.user.client_socket.send(message.encode())

        self.draw_broad()

    def draw_player_info(self):
        opp = 'Computer'
        if self.opp_info is not None:
            # opp = user.name + (user.elo)
            pass

        if self.is_white:
            opp_img = 'sw'
            player_img = 'sb'
        else:
            opp_img = 'sb'
            player_img = 'sw'

        # opponent information
        pygame.draw.rect(self.surface, COLOR['background-color'], (80, 35, 400, 40))
        pygame.draw.rect(self.surface, COLOR['avt-black'], (80, 35, 40, 40), border_radius=1)
        self.surface.blit(self.images['bAvt'], (83, 36))
        self.surface.blit(self.font.render(opp, False, COLOR['white']), (130, 35))
        pygame.draw.rect(self.surface, COLOR['background-color'], (130, 55, 200, 20))
        x = 130
        for piece, num in self.pieces_is_taken.items():
            if num == 0:
                continue
            for _ in range(num):
                self.surface.blit(self.images[opp_img + piece], (x, 55))
                x += 5
            x += 8

        if self.point < 0:
            x += 10
            self.surface.blit(self.font.render(f'+{abs(self.point)}', False, COLOR['white']), (x, 60))

        # player information
        pygame.draw.rect(self.surface, COLOR['background-color'], (80, 725, 400, 40))
        pygame.draw.rect(self.surface, COLOR['avt-white'], (80, 725, 40, 40), border_radius=1)
        self.surface.blit(self.images['wAvt'], (83, 726))
        # Player = user.name (user.elo)
        self.surface.blit(self.font.render('Player', False, COLOR['white']), (130, 725))
        pygame.draw.rect(self.surface, COLOR['background-color'], (130, 745, 200, 20))
        x = 130
        for piece, num in self.pieces_taken.items():
            if num == 0:
                continue
            for _ in range(num):
                self.surface.blit(self.images[player_img + piece], (x, 745))
                x += 8
            x += 12
            
        if self.point > 0:
            x += 10
            self.surface.blit(self.font.render(f'+{self.point}', False, COLOR['white']), (x, 750))

    def listener(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = self.get_mouse_pos(pygame.mouse.get_pos())
            if is_clicked(mouse_pos, self.game_rect):
                position = self.mouse_pos_to_chess_pos(mouse_pos)
                self.select_cell(position)

        for button in self.buttons:
            if button.is_clicked(event, self.get_mouse_pos(pygame.mouse.get_pos())):
                if button.id == 'spin':
                    self.is_white_view = not self.is_white_view 
                    self.draw_broad()

    def repaint(self):
        pygame.draw.rect(self.surface, COLOR['header-color'], (760, 30, 400, 740), border_radius=5)
        for button in self.buttons:
            button.draw(self.surface)
        
