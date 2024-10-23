import pygame
from .util import *

class HomePage(View):
    broad_img = resize(pygame.image.load('client/images/broad_img.png'), (550, 550))
    def __init__(self, user: User, surface: pygame.Surface = None) -> None:
        super().__init__(user, surface)
        self.buttons = [
            Button((800, 200, 200, 100), id='Play Online', text='Play Online', color=COLOR['green-button-color'], hover_color=COLOR[ 'green-button_hover-color'], border_radius=1),
            Button((800, 400, 200, 100), id='Play Computer', text='Play Computer', color=COLOR['gray-button-color'], hover_color=COLOR[ 'gray-button_hover-color'], border_radius=1),
        ]

    def repaint(self):
        self.surface.fill(COLOR['background-color'])
        for btn in self.buttons:
            btn.draw(self.surface)
        self.surface.blit(self.broad_img, (100, 125))

    def listener(self, event):
        
        return super().listener(event)