import pygame

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Scrollable Text Example with Mouse Wheel")

# Đặt màu sắc và font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("Arial", 24)

# Thiết lập văn bản và vị trí khung nhìn
text = """Dòng đầu tiên
Dòng thứ hai
Dòng thứ ba
Dòng thứ tư
Dòng thứ năm
Dòng thứ sáu
Dòng thứ bảy
Dòng thứ tám
Dòng thứ chín
Dòng thứ mười
Dòng mười một
Dòng mười hai
Dòng mười ba
Dòng mười bốn
Dòng mười lăm
Dòng mười sáu"""

lines = text.splitlines()  # Chia văn bản thành các dòng
view_pos = 0  # Vị trí hiện tại của khung nhìn trên văn bản
line_height = font.get_linesize()  # Chiều cao của một dòng văn bản
view_height = 200  # Chiều cao của khung nhìn
view_lines = view_height // line_height  # Số dòng hiển thị được trong khung nhìn

# Hàm vẽ văn bản nhiều dòng với thanh cuộn
def draw_text_with_scroll(surface, lines, font, color, x, y, view_pos, view_lines):
    for i, line in enumerate(lines[view_pos:view_pos + view_lines]):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y + i * line_height))

# Vòng lặp game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_WHEELDOWN and view_pos < len(lines) - view_lines:
                view_pos += 1  # Cuộn xuống
            elif event.button == pygame.BUTTON_WHEELUP and view_pos > 0:
                view_pos -= 1  # Cuộn lên
    
    screen.fill(WHITE)

    # Vẽ khung nhìn văn bản với thanh cuộn
    pygame.draw.rect(screen, BLACK, (50, 50, 500, view_height), 2)  # Khung viền
    draw_text_with_scroll(screen, lines, font, BLACK, 55, 55, view_pos, view_lines)
    
    pygame.display.flip()

pygame.quit()
