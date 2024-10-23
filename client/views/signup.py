import pygame
from .util import *

class Signup(View):
    def __init__(self, client_socket, surface: pygame.Surface = None):
        super().__init__(client_socket, surface)
        
        self.x = 500
        self.y = 300
        self.username = ""
        self.password = ""
        self.confirm_password = ""
        self.input_box_username = pygame.Rect(self.x, self.y, 200, 40)
        self.input_box_password = pygame.Rect(self.x, self.y + 60, 200, 40)
        self.input_box_confirm_password = pygame.Rect(self.x, self.y + 120, 200, 40)
        self.buttons = [
            Button((self.x, self.y + 180, 200, 40), id='Signup', text='Signup', color=COLOR['green-button-color'], hover_color=COLOR['green-button_hover-color'], border_radius=1, font_size=20),
        ]
        self.color_inactive = pygame.Color('white')
        self.color_active = pygame.Color('white')
        self.color_username = self.color_inactive
        self.color_password = self.color_inactive
        self.color_confirm_password = self.color_inactive
        self.active_username = False
        self.active_password = False
        self.active_confirm_password = False
        self.header_font = pygame.font.Font(None, 32)
        self.font = pygame.font.Font(None, 25)
        self.small_font = pygame.font.Font(None, 16)

        self.background_rect = pygame.Rect(self.x - 50, self.y - 110, 300, 500)

    def repaint(self):
        pygame.draw.rect(self.surface, COLOR['header-color'], self.background_rect, border_radius=10)
        
        # Title
        title_surface = self.header_font.render("Login to your account", True, (255, 255, 255))
        self.surface.blit(title_surface, (self.x - 10, self.y - 60))
        
        # Username
        username_label = self.small_font.render("Username:", True, (255, 255, 255))
        self.surface.blit(username_label, (self.x, self.y - 15))
        pygame.draw.rect(self.surface, COLOR['white'], self.input_box_username)
        user_text_surface = self.font.render(self.username, True, pygame.Color('black'))
        self.surface.blit(user_text_surface, (self.input_box_username.x + 5, self.input_box_username.y + 10))
        
        # Password
        password_label = self.small_font.render("Password:", True, (255, 255, 255))
        self.surface.blit(password_label, (self.x, self.y + 45))
        pygame.draw.rect(self.surface, COLOR['white'], self.input_box_password)
        password_text_surface = self.font.render('*' * len(self.password), True, pygame.Color('black'))
        self.surface.blit(password_text_surface, (self.input_box_password.x + 5, self.input_box_password.y + 10))

        # Confirm Password
        confirm_password_label = self.small_font.render("Confirm password:", True, (255, 255, 255))
        self.surface.blit(confirm_password_label, (self.x, self.y + 105))
        pygame.draw.rect(self.surface, COLOR['white'], self.input_box_confirm_password)
        confirm_password_text_surface = self.font.render('*' * len(self.confirm_password), True, pygame.Color('black'))
        self.surface.blit(confirm_password_text_surface, (self.input_box_confirm_password.x + 5, self.input_box_confirm_password.y + 10))

        # Draw buttons
        for btn in self.buttons:
            btn.draw(self.surface)
        
        # Link for existing account
        forgot_text_surface = self.font.render("Do you have an account?", True, (100, 100, 100))
        self.surface.blit(forgot_text_surface, (self.x, self.y + 230))
        
        # Update the display
        pygame.display.flip()

    def listener(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - HEADER_WIDTH, event.pos[1])
            # Check if the user clicked on the username input box
            if self.input_box_username.collidepoint(pos):
                self.active_username = True
                self.active_password = False
                self.active_confirm_password = False
            # Check if the user clicked on the password input box
            elif self.input_box_password.collidepoint(pos):
                self.active_username = False
                self.active_password = True
                self.active_confirm_password = False
            # Check if the user clicked on the confirm password input box
            elif self.input_box_confirm_password.collidepoint(pos):
                self.active_username = False
                self.active_password = False
                self.active_confirm_password = True
            else:
                self.active_username = False
                self.active_password = False
                self.active_confirm_password = False

            # Update the colors of the input boxes
            self.color_username = self.color_active if self.active_username else self.color_inactive
            self.color_password = self.color_active if self.active_password else self.color_inactive
            self.color_confirm_password = self.color_active if self.active_confirm_password else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active_username:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
            elif self.active_password:
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode
            elif self.active_confirm_password:
                if event.key == pygame.K_BACKSPACE:
                    self.confirm_password = self.confirm_password[:-1]
                else:
                    self.confirm_password += event.unicode

