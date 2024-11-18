
class User:
    def __init__(self, client_socket, username = 'guest', password = None, elo = 1000):
        self.client_socket = client_socket
        self.username = username
        self.password = password
        self.elo = elo

    def login(self, username, password):
        self.username = username
        self.password = password 
    
    
    def logout(self):
        self.username = 'guest'
        self.password = None

    
    