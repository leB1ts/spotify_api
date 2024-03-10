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
import asyncio
load_dotenv()

client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")


spotify = Spotify(client_credentials_manager=SpotifyClientCredentials())
loop = asyncio.new_event_loop()
spotdl = Spotdl(client_id, client_secret, loop=loop)

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
                    genre = data
                    print(f"Downloading songs for {genre}")
                    self.download_genre(genre, client)
                if data.startswith("name:"):
                    #download the song
                    name = data
                    print(f"Downloading {name}")
                    self.download_name(name, client)
                if data.startswith("year:"):
                    #download the song
                    year = data
                    print(f"Downloading song from {year}")
                    self.download_year(year, client)
                if data.startswith("random"):
                    #download a random genre
                    print("Downloading random genre")
                    self.random_genre(client)

                
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
    
    def download_genre(self, genre, client):
        i = 0
        #DOES BY SONGS OR ARITSTS WITH GENRE IN THE NAME
        #download 10 songs from the genre
        offset = random.randint(0, 100)
        if not genre or genre.isspace():
            print("No genre provided")
            return
        print(f"Offset: {offset} for genre: {genre}")
        spotify_search_results = spotify.search(str(genre), offset=offset)["tracks"]["items"]
        track_urls = [
            [x["name"], x["external_urls"]["spotify"]]
            for x in spotify_search_results 
        ]

        asyncio.set_event_loop(loop)

        # optional optimisation:
        # use threading to download all the songs at once
        for track in track_urls:
            print(f"Searching for song: {track[0]}")

            songs = spotdl.search(track)
            print(f"Found songs: {songs}")
            i += 1
            
            try:
                print(f"Downloading song: {songs[0]}")
                #how to get the song name and artist from the song object
                artist = songs[0].artist
                name = songs[0].name
                song = spotdl.download(songs[0]) # if doesnt work, try loop.run_until_complete(spotdl.download(songs[0]))
                
            except Exception as e:
                print(f"An error occurred: {e}")
                
        client.sendall("SONGS_DOWNLOADED".encode("utf-8"))



    def download_name(self, name, client):
        i = 0
        offset = random.randint(0, 100)
        #download the song
        if not name or name.isspace():
            print("No name provided")
            return
        print(f"Searching for song: {name}")
        artist_r = name.split(":")[1]

        songs = spotdl.search(name)
        print(f"Found songs: {songs}")

        spotify_search_results = spotify.search(str(name), offset=offset)["tracks"]["items"]
        track_urls = [
            [x["name"], x["external_urls"]["spotify"]]
            for x in spotify_search_results
        ]
        asyncio.set_event_loop(loop)
        for track in track_urls:
            print(f"Searching for song: {track}")
            i += 1
            songs = spotdl.search(track)
            

            print(f"Found songs: {songs}")
            try:
                print(f"Downloading song: {songs[0]}")
                #how to get the song name and artist from the song object
                artist = songs[0].artist
                name = songs[0].name
                
                for i in range(len(songs)):
                    if songs[i].artist == artist_r:
                        song = spotdl.download(songs[i])
                        break
                # if doesnt work, try loop.run_until_complete(spotdl.download(songs[0]))
                
            except Exception as e:
                print(f"An error occurred: {e}")
            
        client.sendall("SONGS_DOWNLOADED".encode("utf-8"))


    # doesnt work correctly
    def download_year(self, year, client):
        i = 0
        offset = random.randint(0, 100)
        if not year or year.isspace():
            print("No year provided")
            return
        print(f"Offset: {offset} for year: {year}")

        songs = spotdl.search(year)
        print(f"Found songs: {songs}")

        year_r = year.split(":")[1]

        spotify_search_results = spotify.search(year, offset=offset)["tracks"]["items"]
        track_urls = [
            [x["name"], x["external_urls"]["spotify"]]
            for x in spotify_search_results
        ]
        asyncio.set_event_loop(loop)
        for track in track_urls:
            print(f"Searching for song: {track[0]}")
            i += 1
            songs = spotdl.search(track)
            print(f"Found songs: {songs}")
            try:
                print(f"Downloading song: {songs[0]}")
                #how to get the song name and artist from the song object
                artist = songs[0].artist
                name = songs[0].name
                for i in range(len(songs)):
                    if songs[i].year == year_r:
                        song = spotdl.download(songs[i])
                        break
            except Exception as e:
                print(f"An error occurred: {e}")

        client.sendall("SONGS_DOWNLOADED".encode("utf-8"))

    def random_genre(self, client):
        options = [
            "pop",
            "rock",
            "rap",
            "country",
            "metal",
            "hip-hop",
            "indie",
            "alternative",
            "electronic",
            "folk",
            "blues",
            "jazz",
            "reggae",
            "latin",
            "classical",
        ]
        random_genre = random.choice(options)
        print(f"Random genre: {random_genre}")
        self.download_genre(random_genre, client)





if __name__ == "__main__":
    server = GameServer()
    server.start()