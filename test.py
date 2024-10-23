import pygame
import sys

# Hàm hiển thị text lên màn hình
def draw_text(surface, text, position, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# Hàm đăng nhập
def login():
    pygame.init()

    # Kích thước màn hình
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Login Form')

    # Màu sắc và font chữ
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    input_color = color_inactive
    password_color = color_inactive
    input_box = pygame.Rect(150, 200, 200, 40)
    password_box = pygame.Rect(150, 260, 200, 40)
    button_box = pygame.Rect(150, 320, 200, 40)

    active_input = False
    active_password = False
    username = ''
    password = ''

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nhấp chuột vào hộp nhập liệu "Username"
                if input_box.collidepoint(event.pos):
                    active_input = True
                    active_password = False
                # Kiểm tra nhấp chuột vào hộp nhập liệu "Password"
                elif password_box.collidepoint(event.pos):
                    active_input = False
                    active_password = True
                else:
                    active_input = False
                    active_password = False

                # Kiểm tra nhấp chuột vào nút đăng nhập
                if button_box.collidepoint(event.pos):
                    print(f"Username: {username}, Password: {password}")

                # Đổi màu khi được nhấn vào
                input_color = color_active if active_input else color_inactive
                password_color = color_active if active_password else color_inactive

            if event.type == pygame.KEYDOWN:
                if active_input:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        # Vẽ màn hình
        screen.fill((230, 230, 230))  # Màu nền

        # Tiêu đề "Login to your account"
        draw_text(screen, "Login to your account", (150, 100), font, (0, 128, 255))

        # Vẽ hộp nhập liệu "Username"
        pygame.draw.rect(screen, input_color, input_box, 2)
        draw_text(screen, username, (input_box.x + 5, input_box.y + 5), font, (0, 0, 0))

        # Vẽ hộp nhập liệu "Password" (hiển thị dấu *)
        pygame.draw.rect(screen, password_color, password_box, 2)
        draw_text(screen, '*' * len(password), (password_box.x + 5, password_box.y + 5), font, (0, 0, 0))

        # Vẽ nút "Login"
        pygame.draw.rect(screen, pygame.Color('dodgerblue'), button_box)
        draw_text(screen, "Login", (button_box.x + 65, button_box.y + 5), font, (255, 255, 255))

        # Liên kết "Forgot your password?"
        draw_text(screen, "Forgot your password?", (150, 370), small_font, (100, 100, 100))

        pygame.display.flip()
        clock.tick(30)

# Chạy hàm login
if __name__ == '__main__':
    login()
