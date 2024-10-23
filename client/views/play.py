import pygame
from .util import *

class Play(View):
    images = {
        'image': resize(pygame.image.load('client/images/broad_img.png'), (640, 640)),
        'wAvt' : resize(pygame.image.load('client/images/chess_pieces/wp.png'), (34, 34)),
        'bAvt' : resize(pygame.image.load('client/images/chess_pieces/bp.png'), (34, 34))
    }
    def __init__(self, client_socket, surface = None):
        super().__init__(client_socket, surface)
        self.buttons = [
            Button((800, 200, 320, 70), id='play_online', text='Play Online', color=COLOR['green-button-color'], border_radius=4),
            Button((800, 300, 320, 70), id='play_computer', text='Play Computer', color=COLOR['green-button-color'], border_radius=4),
            Button((800, 400, 320, 70), id='play_friend', text='Play With Friend', color=COLOR['green-button-color'], border_radius=4),
        ]

        self.font = pygame.font.Font(None, 20)
    
    def repaint(self):
        pygame.draw.rect(self.surface, COLOR['header-color'], (760, 30, 400, 740), border_radius=5)
        for btn in self.buttons:
            btn.draw(self.surface)
        self.surface.blit(self.images['image'], (80, 80))   
        
        pygame.draw.rect(self.surface, COLOR['background-color'], (80, 35, 400, 40))
        pygame.draw.rect(self.surface, COLOR['avt-black'], (80, 35, 40, 40), border_radius=1)
        self.surface.blit(self.images['bAvt'], (83, 36))
        self.surface.blit(self.font.render('Opponent', False, COLOR['white']), (130, 35))
        
        pygame.draw.rect(self.surface, COLOR['background-color'], (80, 725, 400, 40))
        pygame.draw.rect(self.surface, COLOR['avt-white'], (80, 725, 40, 40), border_radius=1)
        self.surface.blit(self.images['wAvt'], (83, 726))
        self.surface.blit(self.font.render('Player', False, COLOR['white']), (130, 725))

    def listener(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = (event.pos[0] - HEADER_WIDTH, event.pos[1])
            for button in self.buttons:
                if button.is_clicked(event, mouse_pos):
                    return button.id