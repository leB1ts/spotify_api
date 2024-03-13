#fresh clent code that actually works and runs as intended
import socket
import login_or_register
from tkinter import *
import game
import glob
import random
import threading

class GameClient:
    def __init__(self, host="localhost", port=7000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def send(self, data):
        self.client.sendall(data.encode())

    def receive(self):
        try:
            data = self.client.recv(4096)
            if not data:
                return None
            return data.decode("utf-8")
        except BlockingIOError:
            return None

if __name__ == "__main__":
    client = GameClient()
    client.client.setblocking(False)  # Set the socket to non-blocking mode
    root = Tk()
    root.withdraw()  # Hide the root window
    global game_window
    game_window = None

    def run_game(mp3_files):
        for audio_file_ in mp3_files:
            # need to get rid of everything but relative path
            audio_file_ = audio_file_.replace("C:\\Users\\wiloj\\Documents\\GitHub\\Project\\spotify_api\\", "")
            print(audio_file_)
            #make a blocking threa
            game_window.play_next(audio_file_).join()
    
        # everything is done, show game over here.
        game_window.game_over()

    def check_for_data():
        global game_window
        data = client.receive()
        if data is not None:
            print(f"Received data: {data}")
            if data == "LOGIN_WINDOW":
                print("Starting login window")
                login_or_register.login_register(client)
            if data == "GAME_WINDOW":
                print("Starting game window")
                game_window = game.GameWindow()
                game_window.start_game(client)
            
            if data == "SONGS_DOWNLOADED":
                print("starting game")
                if game_window is not None:
                    mp3_files = glob.glob("C:\\Users\\wiloj\\Documents\\GitHub\\Project\\spotify_api\\*.mp3")
                    random.shuffle(mp3_files)

                    threading.Thread(target=run_game, args=(mp3_files,)).start()

        root.after(100, check_for_data)  # Check for new data every 100 ms

    check_for_data()
    root.mainloop()
   
  