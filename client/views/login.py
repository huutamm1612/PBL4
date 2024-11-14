import pygame
from .util import *

class Login(View):
    def __init__(self, user: User, surface: pygame.Surface = None):
        super().__init__(user, surface)

        self.x = 500
        self.y = 300

        self.username = ""
        self.password = ""
        self.new_password = ""
        self.confirm_password = ""

        self.input_box_username = pygame.Rect(self.x, self.y, 200, 40)
        self.input_box_password = pygame.Rect(self.x, self.y + 60, 200, 40)
        self.input_box_new_password = pygame.Rect(self.x, self.y + 60, 200, 40)
        self.input_box_confirm_password = pygame.Rect(self.x, self.y + 120, 200, 40)

        self.buttons = [
            Button((self.x, self.y + 120, 200, 40), id='login', text='Login', color=COLOR['green-button-color'], hover_color=COLOR['green-button_hover-color'], border_radius=1, font_size=20),
            Button((self.x, self.y + 180, 200, 40), id='signup', text='Signup', color=COLOR['gray-button-color'], hover_color=COLOR['gray-button_hover-color'], border_radius=1, font_size=20),
            Button((self.x, self.y + 230, 200, 20), id='forgot_password', text='Forgot your password?', text_color=COLOR['href-button-color'], color=COLOR['header-color'], border_radius=0, font_size=16),
            
            Button((self.x, self.y + 180, 200, 40), id='register', text='Register', color=COLOR['green-button-color'], hover_color=COLOR['gray-button_hover-color'], border_radius=1, font_size=20),
            Button((self.x, self.y + 240, 200, 20), id='back_login', text='Back to login', text_color=COLOR['href-button-color'], color=COLOR['header-color'], border_radius=0, font_size=16),
        ]

        self.color_inactive = COLOR['white']
        self.color_active = COLOR['white-focus']

        self.color_username = self.color_inactive
        self.color_password = self.color_inactive
        self.color_new_password = self.color_inactive
        self.color_confirm_password = self.color_inactive

        self.active_username = False
        self.active_password = False
        self.active_new_password = False
        self.active_confirm_password = False
        
        self.header_font = pygame.font.Font(None, 32)
        self.font = pygame.font.Font(None, 25)
        self.small_font = pygame.font.Font(None, 16)

        self.error_message = ""
        self.error_message_login = ""
        self.error_message_forgot = ""

        # Initialize background
        self.background_login_rect = pygame.Rect(self.x - 50, self.y - 110, 300, 400)
        self.background_forgotPassword_rect = pygame.Rect(self.x - 50, self.y - 110, 300, 450)
        self.is_login = True
        self.login_status = False
        
    def repaint(self):
        if self.is_login:
            pygame.draw.rect(self.surface, COLOR['header-color'], self.background_login_rect, border_radius = 10)
        
            title_surface = self.header_font.render("Login to your account", True, (255, 255, 255))
            self.surface.blit(title_surface, (self.x - 10, self.y - 60))
            
            username_surface = self.small_font.render("Username:",True, (255,255,255))
            self.surface.blit(username_surface, (self.x, self.y - 15))

            pygame.draw.rect(self.surface,  self.color_username, self.input_box_username)
            user_text_surface = self.font.render(self.username, True, COLOR['black'])
            self.surface.blit(user_text_surface, (self.input_box_username.x + 5, self.input_box_username.y + 10))

            password_surface = self.small_font.render("Password:", True, (255, 255, 255))
            self.surface.blit(password_surface, (self.x, self.y + 45))

            pygame.draw.rect(self.surface,  self.color_password, self.input_box_password)
            password_text_surface = self.font.render('*' * len(self.password), True, COLOR['black'])
            self.surface.blit(password_text_surface, (self.input_box_password.x + 5, self.input_box_password.y + 10))
            


            for btn in self.buttons:
                if btn.id == "login":
                    btn.draw(self.surface)
                elif btn.id == "signup":
                    btn.draw(self.surface)
                elif btn.id == "forgot_password":
                    btn.draw(self.surface)
            
            if self.error_message_login:
                error_surface = self.small_font.render(self.error_message_login, True, (255, 0, 0))
                self.surface.blit(error_surface, (self.x, self.y + 162))
        
        else:
            pygame.draw.rect(self.surface, COLOR['header-color'], self.background_forgotPassword_rect, border_radius=10)
            
            title_surface = self.header_font.render("Forgot password", True, (255, 255, 255))
            self.surface.blit(title_surface, (self.x - 10, self.y - 60))

            username_surface = self.small_font.render("Username:", True, (255, 255, 255))
            self.surface.blit(username_surface, (self.x, self.y - 15))
            pygame.draw.rect(self.surface,  self.color_username, self.input_box_username)
            user_text_surface = self.font.render(self.username, True, COLOR['black'])
            self.surface.blit(user_text_surface, (self.input_box_username.x + 5, self.input_box_username.y + 10))

            new_password_surface = self.small_font.render("New password:", True, (255, 255, 255))
            self.surface.blit(new_password_surface, (self.x, self.y + 45))
            pygame.draw.rect(self.surface,  self.color_new_password, self.input_box_new_password)
            new_password_text_surface = self.font.render('*' * len(self.new_password), True, COLOR['black'])
            self.surface.blit(new_password_text_surface, (self.input_box_new_password.x + 5, self.input_box_new_password.y + 10))

            confirm_password_surface = self.small_font.render("Confirm password:", True, (255, 255, 255))
            self.surface.blit(confirm_password_surface, (self.x, self.y + 105))
            pygame.draw.rect(self.surface,  self.color_confirm_password, self.input_box_confirm_password)
            confirm_password_text_surface = self.font.render('*' * len(self.confirm_password), True, COLOR['black'])
            self.surface.blit(confirm_password_text_surface, (self.input_box_confirm_password.x + 5, self.input_box_confirm_password.y + 10))


            for btn in self.buttons:
                if btn.id == "register":
                    btn.draw(self.surface)
                if btn.id == "back_login":
                    btn.draw(self.surface)
            if self.error_message_forgot:
                error_surface = self.small_font.render(self.error_message_forgot, True, (255, 0, 0))
                self.surface.blit(error_surface, (self.x + 90, self.y - 15))
            
            if self.error_message:
                error_surface_register = self.small_font.render(self.error_message, True, (255, 0, 0))
                self.surface.blit(error_surface_register, (self.x, self.y + 162))
            
        pygame.display.flip()

    def listener(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = (event.pos[0] - HEADER_WIDTH, event.pos[1])
            for button in self.buttons:
                if button.is_clicked(event, mouse_pos):
                    if self.is_login:
                        if button.id == 'login':
                            self.user.client_socket.send('login'.encode())
                            self.user.client_socket.send(f"{self.username},{self.password}".encode())
                        elif button.id == 'signup':
                            return 'signup'
                        elif button.id == 'forgot_password':
                            self.is_login = False
                    else:
                        if button.id == 'back_login':
                            return 'login'
                        elif button.id == 'register':
                            if self.new_password == self.confirm_password:
                                print('sdasd')
                                self.user.client_socket.send('reset_password'.encode())
                                self.user.client_socket.send(f"{self.username},{self.new_password}".encode())
                                self.error_message = ""
                            else:
                                self.error_message = "Passwords do not match."
                                self.repaint()
                                

            pos = (event.pos[0] - HEADER_WIDTH, event.pos[1])
            if self.input_box_username.collidepoint(pos):
                self.active_username = True
                self.active_password = False
                self.active_new_password = False
                self.active_confirm_password = False
            elif self.input_box_password.collidepoint(pos) and self.is_login == True:
                self.active_username = False
                self.active_password = True
                self.active_new_password = False
                self.active_confirm_password = False
            elif self.input_box_new_password.collidepoint(pos) and self.is_login == False:
                self.active_username = False
                self.active_password = False
                self.active_new_password = True
                self.active_confirm_password = False
            elif self.input_box_confirm_password.collidepoint(pos) and self.is_login == False:
                self.active_username = False
                self.active_password = False
                self.active_new_password = False
                self.active_confirm_password = True
            else:
                self.active_username = False
                self.active_password = False
                self.active_new_password = False
                self.active_confirm_password = False

            self.color_username = self.color_active if self.active_username else self.color_inactive
            self.color_password = self.color_active if self.active_password else self.color_inactive
            self.color_new_password = self.color_active if self.active_new_password else self.color_inactive
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
            elif self.active_new_password:
                if event.key == pygame.K_BACKSPACE:
                    self.new_password = self.new_password[:-1]
                else:
                    self.new_password += event.unicode
            elif self.active_confirm_password:
                if event.key == pygame.K_BACKSPACE:
                    self.confirm_password = self.confirm_password[:-1]
                else:
                    self.confirm_password += event.unicode 