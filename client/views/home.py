import pygame
from .util import *

class HomePage(View):
    broad_img = resize(pygame.image.load('client/images/broad_img.png'), (550, 550))
    def __init__(self, client_socket, surface: pygame.Surface = None) -> None:
        super().__init__(client_socket, surface)

    def repaint(self):
        self.surface.blit(self.broad_img, (100, 125))

    def listener(self, event):
        return super().listener(event)