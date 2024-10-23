import pygame
from .util import *

class Login(View):
    def __init__(self, client_socket, surface: pygame.Surface = None):
        super().__init__(client_socket, surface)
        

        self.x = 500
        self.y = 300
        self.username = ""
        self.password = ""
        self.input_box_username = pygame.Rect(self.x, self.y, 200, 40)
        self.input_box_password = pygame.Rect(self.x, self.y + 60, 200, 40)
        self.buttons = [
            Button((self.x, self.y + 120, 200, 40), id='login', text='Login', color=COLOR['green-button-color'], hover_color=COLOR[ 'green-button_hover-color'], border_radius=1, font_size = 20),
            Button((self.x, self.y + 180, 200, 40), id='signup', text='Signup', color=COLOR['gray-button-color'], hover_color=COLOR[ 'gray-button_hover-color'], border_radius=1, font_size=20),
        ]
        self.color_inactive = pygame.Color('white')
        self.color_active = pygame.Color('white')
        self.color_username = self.color_inactive
        self.color_password = self.color_inactive
        self.active_username = False
        self.active_password = False
        self.header_font = pygame.font.Font(None, 32)
        self.font = pygame.font.Font(None, 25)
        self.small_font = pygame.font.Font(None, 16)

        # Khởi tạo vùng fill màu nền
        self.background_rect = pygame.Rect(self.x - 50, self.y - 110, 300, 400)
        

    def repaint(self):
        
        pygame.draw.rect(self.surface, COLOR['header-color'], self.background_rect, border_radius = 10)
     
        title_surface = self.header_font.render("Login to your account", True, (255, 255, 255))
        self.surface.blit(title_surface, (self.x - 10, self.y - 60))
        
        username_surface = self.small_font.render("Username:",True, (255,255,255))
        self.surface.blit(username_surface, (self.x, self.y - 15))

        pygame.draw.rect(self.surface, COLOR['white'], self.input_box_username)
        user_text_surface = self.font.render(self.username, True, pygame.Color('black'))
        self.surface.blit(user_text_surface, (self.input_box_username.x + 5, self.input_box_username.y + 10))
        

        username_surface = self.small_font.render("Password:",True, (255,255,255))
        self.surface.blit(username_surface, (self.x, self.y + 45))

        # Vẽ hộp nhập liệu "Mật khẩu" (hiển thị dấu sao)
        pygame.draw.rect(self.surface, COLOR['white'], self.input_box_password)
        password_text_surface = self.font.render('*' * len(self.password), True, pygame.Color('black'))
        self.surface.blit(password_text_surface, (self.input_box_password.x + 5, self.input_box_password.y + 10))
        
        for btn in self.buttons:
            btn.draw(self.surface)
        # Liên kết "Forgot your password?"
        forgot_text_surface = self.font.render("Forgot your password?", True, (100, 100, 100))
        self.surface.blit(forgot_text_surface, (self.x, self.y + 230))
        
        # Cập nhật giao diện
        pygame.display.flip()

    def listener(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = (event.pos[0] - HEADER_WIDTH, event.pos[1])
            for button in self.buttons:
                if button.is_clicked(event, mouse_pos):
                    if button.id == 'login':
                        pass
                    elif button.id == 'signup':
                        return 'signup'
                    
            pos = (event.pos[0] - HEADER_WIDTH, event.pos[1])
            # Kiểm tra nhấp chuột vào hộp nhập liệu "Tên đăng nhập"
            if self.input_box_username.collidepoint(pos):
                self.active_username = True
                self.active_password = False
            # Kiểm tra nhấp chuột vào hộp nhập liệu "Mật khẩu"
            elif self.input_box_password.collidepoint(pos):
                self.active_username = False
                self.active_password = True
            else:
                self.active_username = False
                self.active_password = False
            


            # Đổi màu các ô nhập liệu khi kích hoạt
            self.color_username = self.color_active if self.active_username else self.color_inactive
            self.color_password = self.color_active if self.active_password else self.color_inactive

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
    