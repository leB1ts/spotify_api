#fresh server code that actually works and runs as intended
import socket
import threading
import random
from spotdl import Spotdl
from spotipy import Spotify
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from spotdl.utils.ffmpeg import download_ffmpeg

load_dotenv()

client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")


spotify = Spotify(client_credentials_manager=SpotifyClientCredentials())
spotdl = Spotdl(client_id, client_secret)

class GameServer:
    def __init__(self, host="localhost", port=6942):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = []

    def start(self):
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            #sends the client a message to start the login window
            start_message = "LOGIN_WINDOW"
            client.sendall(start_message.encode("utf-8"))
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        try:
            while True:
                # Receive data from the client and process it
                data = client.recv(4096)
                if not data:
                    break
                data = data.decode("utf-8")
                # game logic functions go here
                if data == "LOGIN_SUCCESSFUL":
                    #open the game window
                    client.sendall("GAME_WINDOW".encode("utf-8"))
                if data.startswith("genre:"):
                    #download the 10 songs from the genre
                    genre = data.split(":")[1]
                    print(f"Downloading songs for genre: {genre}")
                    self.download_genre(genre)

                
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
    
    def download_genre(self, genre):
        #download 10 songs from the genre
        offset = random.randint(0, 100)
        track_urls = [
                [x["name"], x["external_urls"]["spotify"]]
                for x in Spotify.search(genre, offset=offset)["tracks"]["items"]
            ]
        i = 0
        for track in track_urls:
            songs = spotdl.search(track[0])
            song = spotdl.download_song(songs[0])
            i += 1
            os.rename(song, "song"+i+".mp3")

if __name__ == "__main__":
    server = GameServer()
    server.start()