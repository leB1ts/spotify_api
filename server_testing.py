import socket
import threading

class GameServer:
    def __init__(self, host='localhost', port=8080):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = []

    def start(self):
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            # Receive data from the client and process it
            data = client.recv(4096)
            if not data:
                break
            #game logic functions go here
            # For example, if data == 'play_next', call self.play_next()

    def play_next(self):
        pass


if __name__ == "__main__":
    server = GameServer()
    server.start()