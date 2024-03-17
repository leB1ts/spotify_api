#fresh clent code that actually works and runs as intended
import socket
import login_or_register
from tkinter import *
import game
import glob
import random
import threading

class GameClient:
    # setting up the host and local host for the server and client to both connect to this means they both have to be the same
    def __init__(self, host="localhost", port=4096):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    # defining the send function to send data to the server
    def send(self, data):
        self.client.sendall(data.encode())

    # defining the receive function to receive data from the server
    def receive(self):
        try:
            # 4096 is the buffer size
            data = self.client.recv(4096)
            if not data:
                return None
            # decoding the data from utf-8
            return data.decode("utf-8")
        except BlockingIOError:
            return None

if __name__ == "__main__":
    # creating a new client
    client = GameClient()
    client.client.setblocking(False)  # Set the socket to non-blocking mode
    root = Tk()
    root.withdraw()  # Hide the root window
    global game_window
    game_window = None

    # function to run the game
    def run_game(mp3_files):
        for audio_file_ in mp3_files:
            # need to get rid of everything but relative path
            audio_file_ = audio_file_.replace("C:\\Users\\wiloj\\Documents\\GitHub\\Project\\spotify_api\\", "")
            print(audio_file_)
            #make a blocking thread to play the next song 
            game_window.play_next(audio_file_).join()
    
        # everything is done, show game over here.
        game_window.game_over()

    # function to check for data
    def check_for_data():
        global game_window
        data = client.receive()
        if data is not None:
            print(f"Received data: {data}")
            # Process the data and run game function based on response
            if data == "LOGIN_WINDOW":
                print("Starting login window")
                # start the login window passning the client
                login_or_register.login_register(client)
            if data == "GAME_WINDOW":
                print("Starting game window")
                game_window = game.GameWindow()
                game_window.start_game(client)
            
            if data == "SONGS_DOWNLOADED":
                print("starting game")
                if game_window is not None:
                    # get all the mp3 files in the directory
                    mp3_files = glob.glob("C:\\Users\\wiloj\\Documents\\GitHub\\Project\\spotify_api\\*.mp3")
                    # shuffle the list of mp3 files
                    random.shuffle(mp3_files)
                    # start the game in a new thread
                    threading.Thread(target=run_game, args=(mp3_files,)).start()
            if data == "ERROR":
                print("Game over")
                # show the game over window
                game_window.game_over()
        # check for new data every 100 ms
        root.after(100, check_for_data)  # Check for new data every 100 ms

    # start the main loop
    check_for_data()
    root.mainloop()
   
  