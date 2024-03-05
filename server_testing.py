import socket
import threading
import code_1

class GameServer:
    def __init__(self, host='localhost', port=6942):
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
        try:
            while True:
                # Receive data from the client and process it
                data = client.recv(4096)
                if not data:
                    break
                data = data.decode('utf-8')  # decode the data
                #game logic functions go here
                # For example, if data == 'play_next', call self.play_next()
                if data == 'start_game':
                    code_1.game_window.start_game()
                if data == "update_points":
                    #run update points system
                    pass
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()

if __name__ == "__main__":
    server = GameServer()
    server.start()