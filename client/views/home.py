import pygame
from .util import *

class HomePage(View):
    broad_img = resize(pygame.image.load('client/images/broad_img.png'), (550, 550))
    def __init__(self, user: User, surface: pygame.Surface = None) -> None:
        super().__init__(user, surface)
        self.name = 'GUEST'
        self.buttons = [
            Button((800, 200, 200, 100), id='Play Online', text='Play Online', color=COLOR['green-button-color'], hover_color=COLOR[ 'green-button_hover-color'], border_radius=1),
            Button((800, 400, 200, 100), id='Play Computer', text='Play Computer', color=COLOR['gray-button-color'], hover_color=COLOR[ 'gray-button_hover-color'], border_radius=1),
        ]
        self.header_font = pygame.font.Font(None, 32)

    def repaint(self):
        self.surface.fill(COLOR['background-color'])
        title_surface = self.header_font.render(self.name, True, (255, 255, 255))
        text_width = title_surface.get_width()
        screen_width = self.surface.get_width()
        x_position = screen_width - text_width - 20  
        y_position = 20  

        self.surface.blit(title_surface, (x_position, y_position))

        for btn in self.buttons:
            btn.draw(self.surface)

        self.surface.blit(self.broad_img, (100, 125))


    def listener(self, event):
        
        return super().listener(event)