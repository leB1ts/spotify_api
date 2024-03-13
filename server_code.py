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
from urllib.parse import parse_qs

client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")


spotify = Spotify(client_credentials_manager=SpotifyClientCredentials())
loop = asyncio.new_event_loop()
spotdl = Spotdl(client_id, client_secret, loop=loop)

target_song_count = 3

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
                print(data)
                if data.startswith("genre="):
                    #download the 10 songs from the genre
                    genre = data
                    print(f"Downloading songs for {genre}")
                    self.download_genre(genre, client)
                if data.startswith("artist="): # name:Travis Scott genre:rock
                    #download the song
                    artist = data
                    print(f"Downloading {artist}")
                    self.download_artist(artist, client)
                # spotify searches cant be done by year so by song name will be done instead
                #if data.startswith("year="):
                    #download the song
                 #   year = data
                  #  print(f"Downloading song from {year}")
                   # self.download_year(year, client)
                if data.startswith("track="):
                    #download the song
                    name = data
                    print(f"Downloading songs called {name}")
                    self.download_name(name, client)
                if data.startswith("random"):
                    #download a random genre
                    print("Downloading random genre")
                    self.random_genre(client)

                
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
    
    def download_song(self, query, client, filter):
        i = 0
        download_count = 0
        #DOES BY SONGS OR ARITSTS WITH GENRE IN THE NAME
        #download 10 songs from the genre
        offset = random.randint(0, 100)
        query_parsed = parse_qs(query)

        while True:
            spotify_search_results = spotify.search(query, offset=offset)["tracks"]["items"]
            track_urls = [
                [x["name"], x["external_urls"]["spotify"]]
                for x in spotify_search_results 
            ]

            asyncio.set_event_loop(loop)

            # optional optimisation:
            # use threading to download all the songs at once
            for track in track_urls:
                if download_count >= target_song_count:
                    break
                print(f"Searching for song: {track[0]}")

                songs = spotdl.search(track)
                print(f"Found songs: {songs}")
                i += 1
                
                try:
                    print(f"Downloading song: {songs[0]}")
                    #how to get the song name and artist from the song object

                    for song in songs:
                        print(song, query_parsed)

                        if filter(song, query_parsed):
                            spotdl.download(song)
                            print(f"Downloaded song: {song}")
                        
                            download_count += 1
                            break
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
            if download_count >= target_song_count:
                break
            else:
                offset += target_song_count
        client.sendall("SONGS_DOWNLOADED".encode("utf-8"))

    def download_genre(self, genre, client):
        self.download_song(genre, client, lambda song, query: any(genre in query["genre"] for genre in song.genres))

    def download_artist(self, artist, client):
        self.download_song(artist, client, lambda song, query: any(artist in query["artist"] for artist in song.artists))

    # doesnt work correctly
    def download_name(self, name, client):
        print("Downloading song by ", name)
        self.download_song(name, client, lambda song, query: query["track"][0].lower() in song.name)

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