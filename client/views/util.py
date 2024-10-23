import pygame
from abc import ABC, abstractmethod

COLOR = {
    'white' : (255, 255, 255),
    'broad-white' : (232, 234, 205),
    'broad-green' : (117, 150, 84),
    'broad-highlight-white' : (245, 246, 130),
    'broad-highlight-green' : (185, 202, 67),
    'broad-possible-white' : (202,203,179),
    'broad-possible-green' : (99,128,70),
    'header-color' : (38, 36, 33),
    'header-button-color' : (26, 24, 24),
    'black' : (0, 0, 0),
    'green1' : (),
    'green-button-color' : (129, 182, 76),
    'green-button_hover-color' : (163, 209, 96),
    'gray-button-color' : (142, 154, 131),
    'gray-button_hover-color' : (132, 141, 119),
    'background-color' : (49, 46, 43),
    'avt-black' : (71, 69, 66),
    'avt-white' : (231, 229, 227),
}

WIDTH = 1500
HEIGHT = 800  
HEADER_WIDTH = 200
HEADER_HEIGHT = 800 
CHESS_SIZE = 80
PIECE_SCALE = 5

class View(ABC):
    def __init__(self, client_socket, surface: pygame.Surface=None) -> None:
        self.client_socket = client_socket
        self.surface = surface
        super().__init__()

    @abstractmethod
    def repaint(self):
        pass

    @abstractmethod
    def listener(self, event):
        pass

    
def resize(img, new_size: tuple):
    return pygame.transform.smoothscale(img, new_size)

def is_clicked(mouse_pos, surface_rect: pygame.Rect):
    return surface_rect.collidepoint(mouse_pos)

# ví dụ 'e1' -> '51'
def pos_to_coor(pos):
    return str(ord(pos[0]) - 96) + pos[1]

class Button:
    def __init__(
            self, 
            rect: tuple, 
            id: str='',
            text: str='', 
            color: tuple=(0, 0, 0), 
            hover_color: tuple=None, 
            text_color: tuple=(255, 255, 255), 
            font_size: int=30, 
            font_family: str='Helvetica',
            border_radius: int=0,
        ) -> None:

        self.id = id
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font_family = font_family
        self.font = pygame.font.SysFont(self.font_family, font_size, bold=True)
        self.border_radius = border_radius

        if self.hover_color is None:
            self.hover_color = self.color 
    
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height), border_radius=self.border_radius)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=self.border_radius)

        if self.text != '':
            text_surface = self.font.render(self.text, True, self.text_color)
            screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))

    def is_hovered(self, mouse_pos):
        return self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height

    def is_clicked(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if self.is_hovered(mouse_pos):
                return True
        return False
