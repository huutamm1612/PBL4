import pygame
from .util import *

class Signup(View):
    def __init__(self, user: User, surface: pygame.Surface = None):
        super().__init__(user, surface)
        
        self.x = 500
        self.y = 300
        self.username = ""
        self.password = ""
        self.confirm_password = ""
        self.input_box_username = pygame.Rect(self.x, self.y, 200, 40)
        self.input_box_password = pygame.Rect(self.x, self.y + 60, 200, 40)
        self.input_box_confirm_password = pygame.Rect(self.x, self.y + 120, 200, 40)
        self.buttons = [
            Button((self.x, self.y + 180, 200, 40), id='signup', text='Signup', color=COLOR['green-button-color'], hover_color=COLOR['green-button_hover-color'], border_radius=1, font_size=20),
            Button((self.x, self.y + 230, 200, 20), id='account', text='Do you have an account?', text_color=COLOR['href-button-color'], color=COLOR['header-color'], border_radius=0, font_size=16),
        ]
        self.color_inactive = pygame.Color('white')
        self.color_active = COLOR['white-focus']

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
        self.error_message = ""

    def repaint(self):
        pygame.draw.rect(self.surface, COLOR['header-color'], self.background_rect, border_radius=10)
        
        # Title
        title_surface = self.header_font.render("Signup to your account", True, (255, 255, 255))
        self.surface.blit(title_surface, (self.x - 10, self.y - 60))
        
        # Username
        username_label = self.small_font.render("Username:", True, (255, 255, 255))
        self.surface.blit(username_label, (self.x, self.y - 15))
        pygame.draw.rect(self.surface, self.color_username, self.input_box_username)
        user_text_surface = self.font.render(self.username, True, COLOR['black'])
        self.surface.blit(user_text_surface, (self.input_box_username.x + 5, self.input_box_username.y + 10))
        
        # Password
        password_label = self.small_font.render("Password:", True, (255, 255, 255))
        self.surface.blit(password_label, (self.x, self.y + 45))
        pygame.draw.rect(self.surface, self.color_password, self.input_box_password)
        password_text_surface = self.font.render('*' * len(self.password), True, COLOR['black'])
        self.surface.blit(password_text_surface, (self.input_box_password.x + 5, self.input_box_password.y + 10))

        # Confirm Password
        confirm_password_label = self.small_font.render("Confirm password:", True, (255, 255, 255))
        self.surface.blit(confirm_password_label, (self.x, self.y + 105))
        pygame.draw.rect(self.surface, self.color_confirm_password, self.input_box_confirm_password)
        confirm_password_text_surface = self.font.render('*' * len(self.confirm_password), True, COLOR['black'])
        self.surface.blit(confirm_password_text_surface, (self.input_box_confirm_password.x + 5, self.input_box_confirm_password.y + 10))
       
        # Draw buttons
        for btn in self.buttons:
            btn.draw(self.surface)
        
        # Display error 
        if self.error_message:
            error_surface = self.small_font.render(self.error_message, True, (255, 0, 0))
            self.surface.blit(error_surface, (self.x, self.y + 162))
        
        # Update the display
        pygame.display.flip()

    def listener(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = (event.pos[0] - HEADER_WIDTH, event.pos[1])
            for button in self.buttons:
                if button.is_clicked(event, mouse_pos):
                    if button.id == 'signup':
                        if self.password == self.confirm_password:
                            self.user.client_socket.send('signup'.encode())
                            self.user.client_socket.send(f"{self.username},{self.password}".encode())
                            self.error_message = ""  # Clear any previous error messages
                        else:
                            self.error_message = "Passwords do not match."
                            self.repaint()
                    if button.id == 'account':
                        return 'login'

            pos = (event.pos[0] - HEADER_WIDTH, event.pos[1])
            # Check which input box was clicked
            if self.input_box_username.collidepoint(pos):
                self.active_username = True
                self.active_password = False
                self.active_confirm_password = False
            elif self.input_box_password.collidepoint(pos):
                self.active_username = False
                self.active_password = True
                self.active_confirm_password = False
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
