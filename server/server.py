import socket
import threading
import pickle
import time
import numpy as np
from game import *
from ai import AI
from database import Database

class Server:
    def __init__(self, host='127.0.0.1', port=12345) -> None:
        self.database = Database()
        self.host = host
        self.port = port
        self.client_logined = {}
        self.clients = {}
        self.client_in_game = {}

        self.games = []
        self.player_searching_game = []
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(6)
        print(f"Server listening on {self.host}:{self.port}")

    def get_game_from_address(self, client_address):
        for game in self.games:
            for player in game.players:
                if player.client_address == client_address:
                    return game
                
        return None
    
    def get_name(self, client_address):
        if self.client_logined[client_address] is None:
            return 'Guest 1000'
        else:
            print(self.client_logined[client_address])
            return self.client_logined[client_address][1] + ' ' + str(self.client_logined[client_address][-1])
        
    def handle_client(self, client_socket, client_address):
        while True:
            try:
                header = client_socket.recv(1024).decode('utf-8')
                msg = client_socket.recv(1024).decode('utf-8')

                if header == 'play':
                    if msg == 'play_online':
                        self.player_searching_game.append(client_address)

                        if len(self.player_searching_game) >= 2:
                            self.games.append(
                                Game([
                                    Player(self.player_searching_game[0], True), 
                                    Player(self.player_searching_game[1], False)
                                ])
                            )
                            self.clients[self.player_searching_game[0]].send('play'.encode())
                            self.clients[self.player_searching_game[0]].send(f'start white {self.get_name(self.player_searching_game[1])}'.encode())
                            self.clients[self.player_searching_game[1]].send('play'.encode())
                            self.clients[self.player_searching_game[1]].send(f'start black {self.get_name(self.player_searching_game[0])}'.encode())

                            self.client_in_game[self.player_searching_game[0]] = True
                            self.client_in_game[self.player_searching_game[1]] = True

                            self.player_searching_game = self.player_searching_game[2:]

                    elif msg == 'play_computer':
                        self.games.append(
                            Game([
                                Player(client_address, True),
                                Player('AI', False)
                            ], play_com=True)
                        )
                        self.clients[client_address].send('play'.encode())
                        self.clients[client_address].send('start white Computer'.encode())
                        self.client_in_game[client_address] = True

                    elif msg[:4] == 'chat':
                        game = self.get_game_from_address(client_address)
                        player_socket = [self.clients[game.players[0].client_address]]
                        if not game.play_com:
                            player_socket.append(self.clients[game.players[1].client_address])

                        for socket in player_socket:
                            socket.send('play'.encode())
                            if socket == client_socket:
                                socket.send((msg[:4] + 'You: ' + msg[4:]).encode())
                            else:
                                socket.send((msg[:4] + 'Opponent: ' + msg[4:]).encode())
                        
                    elif msg == 'resign':
                        game = self.get_game_from_address(client_address)
                        winner = 'bwin#'

                        player_socket = [self.clients[game.players[0].client_address]]
                        
                        if not game.play_com:
                            player_socket.append(self.clients[game.players[1].client_address])
                            if game.players[1].client_address == client_address:
                                winner = 'wwin#'
                        self.games.remove(game)
                        
                        for socket in player_socket:
                            socket.send('play'.encode())
                            socket.send(winner.encode())

                        if len(player_socket) == 2:
                            if 'w' == winner[0]:
                                user = self.client_logined[game.players[0].client_address]
                                if user is not None:
                                    self.database.change_elo(user[0], user[-1] + 10)
                                user = self.client_logined[game.players[1].client_address]
                                if user is not None:
                                    self.database.change_elo(user[0], user[-1] - 10)
                            else:
                                user = self.client_logined[game.players[1].client_address]
                                if user is not None:
                                    self.database.change_elo(user[0], user[-1] + 10)
                                user = self.client_logined[game.players[0].client_address]
                                if user is not None:
                                    self.database.change_elo(user[0], user[-1] - 10)

                    elif msg == 'draw':
                        game = self.get_game_from_address(client_address)
                        if client_address == game.players[0].client_address:
                            self.clients[game.players[1].client_address].send('play'.encode())
                            self.clients[game.players[1].client_address].send('wanna draw'.encode())
                        else:
                            self.clients[game.players[0].client_address].send('play'.encode())
                            self.clients[game.players[0].client_address].send('wanna draw'.encode())

                    elif msg == 'accept draw':
                        game = self.get_game_from_address(client_address)
                        self.clients[game.players[0].client_address].send('play'.encode())
                        self.clients[game.players[0].client_address].send('draw'.encode())
                        self.clients[game.players[1].client_address].send('play'.encode())
                        self.clients[game.players[1].client_address].send('draw'.encode())
                        self.games.remove(game)

                    elif msg == 'decline draw':
                        game = self.get_game_from_address(client_address)
                        if client_address == game.players[0].client_address:
                            self.clients[game.players[1].client_address].send('play'.encode())
                            self.clients[game.players[1].client_address].send('decline draw'.encode())
                        else:
                            self.clients[game.players[0].client_address].send('play'.encode())
                            self.clients[game.players[0].client_address].send('decline draw'.encode())
                    
                    else:
                        game = self.get_game_from_address(client_address)

                        player_socket = [self.clients[game.players[0].client_address]]
                        if not game.play_com:
                            player_socket.append(self.clients[game.players[1].client_address])

                        action, pos = msg.split(' ')
                        pos = (int(pos[0]) - 1, int(pos[1]) - 1)
                        if action == 'select':
                            can_move, can_take = game.pos_can_move(pos, client_address)
                            client_socket.send('play'.encode())
                            client_socket.sendall(pickle.dumps([self.encode_pos(*can_move), self.encode_pos(*can_take)]))

                        if action == 'out':
                            game.out(client_address)

                        if action == 'move' or action == 'take':
                            if action == 'move':
                                move_info = game.move(pos, client_address)
                                for socket in player_socket:
                                    socket.send('play'.encode())
                                    socket.send(move_info.encode())

                            elif action == 'take':
                                move_info = game.take(pos, client_address)
                                for socket in player_socket:
                                    socket.send('play'.encode())
                                    socket.send(move_info.encode())

                            if '#' in move_info:
                                if len(player_socket) == 2:
                                    if 'w' == move_info[0]:
                                        user = self.client_logined[game.players[0].client_address]
                                        if user is not None:
                                            self.database.change_elo(user[0], user[-1] + 10)
                                        user = self.client_logined[game.players[1].client_address]
                                        if user is not None:
                                            self.database.change_elo(user[0], user[-1] - 10)
                                    else:
                                        user = self.client_logined[game.players[1].client_address]
                                        if user is not None:
                                            self.database.change_elo(user[0], user[-1] + 10)
                                        user = self.client_logined[game.players[0].client_address]
                                        if user is not None:
                                            self.database.change_elo(user[0], user[-1] - 10)

                                self.client_in_game[self.clients[game.players[0].client_address]] = False
                                if len(player_socket) == 2:
                                    self.client_in_game[self.clients[game.players[1].client_address]] = False

                                self.games.remove(game)

                            if game.play_com:
                                threading.Thread(target=self.ai_move, args=(game, player_socket[0]), daemon=True).start()

                elif header == 'login':
                    username, password = msg.split(',')          
                    result = self.database.login(username, password)
                    if result is not None:
                        client_socket.send(header.encode())
                        client_socket.send(f"ok {result[-1]}".encode())
                        self.client_logined[client_address] = result
                    else:                        
                        client_socket.send(header.encode())
                        client_socket.send("no".encode())
                elif header == 'reset_password':
                    username, password = msg.split(',')       
                    if self.database.update_password(username, password):
                        client_socket.send(header.encode())
                        client_socket.send("updateok".encode())
                        print("change ok")
                    elif self.database.update_password(username, password) == False:
                        client_socket.send(header.encode())
                        client_socket.send("updateno".encode())
                        print("change not ok ")
                elif header == 'signup':
                    username, password = msg.split(',')
                    if self.database.signup(username, password):
                        client_socket.send(header.encode())
                        client_socket.send("DKok".encode())
                    else:
                        client_socket.send(header.encode())
                        client_socket.send("DKno".encode())
                elif header == 'logout':
                    self.client_logined[client_address] = None
        
            except ConnectionResetError:
                print(f"[-] Connection lost from {client_address}")
                game = self.get_game_from_address(client_address)
                try: 
                    if game is not None:
                        winner = 'wwin#'
                        player_socket = [self.clients[game.players[0].client_address]]
                        player_socket.append(self.clients[game.players[1].client_address])
                        if game.players[1].client_address == client_address:
                            winner = 'bwin#'
                        self.games.remove(game)

                        if len(player_socket) == 2:
                            if 'w' == winner[0]:
                                user = self.client_logined[game.players[0].client_address]
                                if user is not None:
                                    self.database.change_elo(user[0], user[-1] + 10)
                                user = self.client_logined[game.players[1].client_address]
                                if user is not None:
                                    self.database.change_elo(user[0], user[-1] - 10)
                            else:
                                user = self.client_logined[game.players[1].client_address]
                                if user is not None:
                                    self.database.change_elo(user[0], user[-1] + 10)
                                user = self.client_logined[game.players[0].client_address]
                                if user is not None:
                                    self.database.change_elo(user[0], user[-1] - 10)

                        for socket in player_socket:
                            try:
                                socket.send('play'.encode())
                                socket.send(winner.encode())
                            except:
                                pass
                except:
                    pass

                self.clients.pop(client_address)
                self.client_in_game.pop(client_address)
                self.client_logined.pop(client_address)
                break

        client_socket.close()
        pass
    
    def ai_move(self, game, socket):
        move_info = game.ai_move()
        socket.send('play'.encode())
        socket.send(move_info.encode())

    def encode_pos(self, *poses):
        li = []
        for pos in poses:
            li.append(str(pos[0] + 1) + str(pos[1] + 1))
            
        return li

    def run(self):
        self.running = True
        threading.Thread(target=self.stop_server).start()
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.clients[client_address] = client_socket
                self.client_in_game[client_address] = False
                self.client_logined[client_address] = None
                print(f"[+] New connection from {client_address}")

                threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()
                
            
            except Exception as e:
                if self.running:
                    print(f"Error accepting connections: {e}")
                break

    def stop_server(self):
        input('press "Enter" to stop server...\n')
        self.server_socket.close()
        for client_socket in self.clients.values():
            client_socket.close()

if __name__ == '__main__':
    server = Server('10.10.76.31')
    server.run()