import pygame
import socket
import pickle
import threading
from views import *

class MainScreen(View):
    surface = None
    
    header_buttons = []


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
        self.active_button = None 

        MainScreen.header_buttons = [
            Button((0, 0, HEADER_WIDTH, 50), id='home', text='Home', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
            Button((0, 50, HEADER_WIDTH, 50), id='play', text='Play', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
            Button((0, 100, HEADER_WIDTH, 50), id='login', text='Login', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
            Button((0, 150, HEADER_WIDTH, 50), id='signup', text='Signup', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
    
        ]

    @staticmethod
    def click_button_login():
        MainScreen.header_buttons = MainScreen.header_buttons[:2]
        MainScreen.header_buttons.append(
            Button((0, 100, HEADER_WIDTH, 50), id='logout', text='Logout', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
        )
        
    def click_button_logout(self):
        self.user.logout()
        MainScreen.header_buttons = MainScreen.header_buttons[:2]
        MainScreen.header_buttons.extend([
            Button((0, 100, HEADER_WIDTH, 50), id='login', text='Login', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
            Button((0, 150, HEADER_WIDTH, 50), id='signup', text='Signup', color=COLOR['header-color'], hover_color=COLOR['header-button-color'], border_radius=1),
        ])


    def repaint_header(self):
        self.header_layout.fill(COLOR['header-color'])
        for button in MainScreen.header_buttons:
            button.draw(self.header_layout)

        self.screen.blit(self.header_layout, (0, 0))

    def repaint(self):
        pass

    def listener_button(self, event):
        mouse_pos = pygame.mouse.get_pos()
        for button in MainScreen.header_buttons:
            if button.is_clicked(event, mouse_pos):
                if button.id == 'logout':
                    self.click_button_logout()
                    self.user.client_socket.send('logout'.encode())
                    self.user.client_socket.send('logout'.encode())
                else:
                    self.active_button = button
                    self.change_page(button.id)
            if button == self.active_button:
                button.color = COLOR['header-button-color'] 
            else:
                button.color = COLOR['header-color']
        self.repaint_header()


    def listener(self, event):
        pass

    def change_page(self, page):
        print(self.page)
        print(self.page is Chess)
        if type(self.page) is Chess and len(self.page.all_move_info) != 0:
            self.page.user.client_socket.send('play'.encode())
            self.page.user.client_socket.send('resign'.encode())

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
                message = self.user.client_socket.recv(1024)
                try:
                    message = message.decode('utf-8')
                except:
                    message = pickle.loads(message)

                if header == 'play':
                    if 'start' in message:
                        info = message.split()
                        self.index.page.set_color(info[1])
                        self.index.page.set_opp(info[2:])

                    elif message == 'draw':
                        self.index.page.chat += '\n' + 'This game is draw!'
                    
                    elif message == 'wanna draw':
                        self.index.page.chat += '\n' + 'Opponent wanna draw!'
                        self.index.page.opp_wanna_draw()

                    elif message == 'decline draw':
                        self.index.page.chat += '\n' + 'Opponent refused to draw!'

                    elif message[:4] == 'chat':
                        self.index.page.chat += '\n' + message[4:]
                    
                    else:
                        if type(message) is list:
                            self.index.page.possible_moves = message[0]
                            self.index.page.possible_takes = message[1]
                            self.index.page.draw_broad()
                        
                        else: 
                            self.index.page.move(message)

                elif header == 'login':
                    if message[:2] == 'ok':
                        self.index.page.user.username = self.index.page.username
                        self.index.page.user.password = self.index.page.password
                        self.index.change_page('home')
                        self.index.page.user.elo = int(message.split()[1])
                        MainScreen.click_button_login()
                    elif message == 'no':
                        self.index.page.error_message_login = "Incorrect username or password."
                        self.index.page.repaint()
                elif header == 'reset_password':
                    if message == 'updateok':
                        self.index.change_page('login')
                        print("change ok")
                    elif message == 'updateno':
                        self.index.page.error_message_forgot = "Incorrect username"
                        print("change not ok")
                elif header == 'signup':
                    if message == 'DKok':
                        self.index.change_page('home')
                    elif message == 'DKno':
                        print('dang ki sai')
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        
    def run(self):
        self.index = MainScreen(self.user)      
        self.index.run()

if __name__ == '__main__':
    client = Client('10.10.76.31')
    client.run()