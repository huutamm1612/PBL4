import pygame
import socket
import pickle
import threading
from views import *

class MainScreen(View):
    surface = None
    def __init__(self, user: User, surface: pygame.Surface = None) -> None:
        super().__init__(user, surface)
        
        pygame.init()
        self.width, self.height = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess")
        
        self.header_width, self.header_height = HEADER_WIDTH, HEADER_HEIGHT

        self.layout = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.header_layout = self.layout.subsurface(pygame.Rect(0, 0, self.header_width, self.header_height))
        self.surface = self.layout.subsurface(pygame.Rect(self.header_width, 0, self.width - self.header_width, self.height))
        self.surface.fill(COLOR['background-color'])
        self.header_layout.fill(COLOR['header-color'])
        self.page = HomePage(user, self.surface)

        self.header_buttons = [
            Button((0, 0, self.header_width, 50), id='home', text='Home', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
            Button((0, 50, self.header_width, 50), id='play', text='Play', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
            Button((0, 100, self.header_width, 50), id='login', text='login', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
            Button((0, 150, self.header_width, 50), id='signup', text='signup', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
        ]



    def repaint_header(self):
        for button in self.header_buttons:
            button.draw(self.header_layout)

        self.screen.blit(self.header_layout, (0, 0))

    def repaint(self):
        pass

    def listener_button(self, event):
        for button in self.header_buttons:
            if button.is_clicked(event, mouse_pos=pygame.mouse.get_pos()):
                self.change_page(button.id)

    def listener(self, event):
        pass

    def change_page(self, page):
        if page == 'home':
            self.surface.fill(COLOR['background-color'])
            self.page = HomePage(self.user, self.surface)
        elif page == 'login':
            self.surface.fill(COLOR['background-color'])
            self.page = Login(self.user, self.surface)
        elif page == 'signup':
            self.surface.fill(COLOR['background-color'])
            self.page = Signup(self.user, self.surface)
        elif 'play' in page:
            self.surface.fill(COLOR['background-color'])
            if page == 'play':
                self.page = Play(self.user, self.surface)

            if len(page) > 4:
                self.page = Chess(self.user, self.surface)
                self.user.client_socket.send('play'.encode())
                self.user.client_socket.send(page.encode())


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                self.listener_button(event)
                page = self.page.listener(event)
                if page is not None:
                    self.change_page(page)
    
            self.page.repaint()
            self.repaint_header()
            self.screen.blit(self.page.surface, (self.header_width, 0))
            pygame.display.flip()
        
        pygame.quit()

class Client:
    def __init__(self, host='127.0.0.1', port=12345) -> None:
        self.user = User(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        try:
            self.user.client_socket.connect((host, port))
            print('Connect successfully!')
        except Exception as e:
            print(f"Error connecting to server: {e}")
            pygame.quit()
            return
        
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()
        
    def receive_messages(self):
        while True:
            try:
                header = self.user.client_socket.recv(1024).decode('utf-8')
                print(header)
                message = self.user.client_socket.recv(1024)
                try:
                    message = message.decode('utf-8')
                except:
                    message = pickle.loads(message)

                if header == 'play':
                    if 'start' in message:
                        info = message.split()
                        if info[1] == 'black':
                            self.index.page.is_white = False
                            self.index.page.is_white_view = False
                            self.index.page.can_move = False
                            self.index.page.draw_broad()

                        elif info[1] == 'white':
                            self.index.page.is_white = True
                            self.index.page.is_white_view = True
                            self.index.page.can_move = True
                            self.index.page.draw_broad()

                        print(info)

                    else:
                        if type(message) is list:
                            self.index.page.possible_moves = message[0]
                            self.index.page.possible_takes = message[1]
                            self.index.page.draw_broad()
                        
                        else: 
                            self.index.page.all_move_info.append(message)
                            self.index.page.change_broad(message)
                            self.index.page.draw_broad()
                            self.index.page.can_move = not self.index.page.can_move
                elif header == 'login':
                    if message == 'ok':
                        self.index.change_page('home')
                    elif message == 'no':
                        print('sai')
                        

            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        
    def run(self):
        self.index = MainScreen(self.user)
        self.index.run()

if __name__ == '__main__':
    client = Client()
    client.run()