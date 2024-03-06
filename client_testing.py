import socket
from tkinter import Tk, Button
import cleaner_code
import code_1

points = 0


class GameClient:
    def __init__(self, host="localhost", port=6942, game_window=code_1.GameWindow()):
        self.game_window = game_window
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def send(self, data):
        self.client.sendall(data.encode())

    def start_game(self):
        # Send a message to the server to start the game
        self.send("start_game")
        self.game_window.start_game()

    def play_next(self):
        # Send a message to the server to play the next song
        self.send("play_next")

    def points(self):
        self.send("update_points")


if __name__ == "__main__":
    client = GameClient()

    app = Tk()
    app.geometry("300x200")
    app.title("Music Quiz ?")
    Button(app, text="Start Game", command=client.start_game).pack()
    Button(app, text="login", command=cleaner_code.login_register).pack()
    Button(app, text="Play Next Song", command=client.play_next).pack()
    Button(app, text="Exit", command=app.destroy).pack()
    app.mainloop()
