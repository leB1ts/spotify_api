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
import game


# load the environment variables
client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")

# setting up the spotify api
spotify = Spotify(client_credentials_manager=SpotifyClientCredentials())
loop = asyncio.new_event_loop()
spotdl = Spotdl(client_id, client_secret, loop=loop)

# this can be any number but just refers to how many songs the game will be
target_song_count = 3

class GameServer:
    # setting up the host and local host for the server and client to both connect to this means they both have to be the same
    def __init__(self, host="localhost", port=4096):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(50)
        # list of clients
        self.clients = []

    def start(self):
        while True:
            # Accept a new connection
            client, addr = self.server.accept()
            self.clients.append(client)
            #sends the client a message to start the login window
            start_message = "LOGIN_WINDOW"
            #encoding the message to utf-8
            client.sendall(start_message.encode("utf-8"))
            # Start a new thread to handle the client
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
                
                if data.startswith("genre="):
                    #download the songs from the genre
                    genre = data
                    print(f"Downloading songs for {genre}")
                    self.download_genre(genre, client)

                if data.startswith("artist="): 
                    #download the song for that artist
                    artist = data
                    print(f"Downloading {artist}")
                    self.download_artist(artist, client)
                
                if data.startswith("track="):
                    #download the song
                    name = data
                    print(f"Downloading songs called {name}")
                    self.download_name(name, client)

                if data.startswith("random"):
                    #download a random genre
                    print("Downloading random song")
                    self.random_song(client)

                
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
    
    def download_song(self, query, client, filter):
        
        # once downloadcount greater than target song count it ends the loop
        download_count = 0  
        # setting the offset parameter for the search
        offset = random.randint(0, 100)
        #parse the query
        query_parsed = parse_qs(query)

        while True:
            #search for the song via the spotify api
            spotify_search_results = spotify.search(query, offset=offset)["tracks"]["items"]
            # get the track urls from the search results
            track_urls = [
                [x["name"], x["external_urls"]["spotify"]]
                for x in spotify_search_results 
            ]

            asyncio.set_event_loop(loop)

            # for each track url, download the song
            for track in track_urls:
                if download_count >= target_song_count:
                    break
                
                # songs is a list of song objects from the search results using the spotdl library
                songs = spotdl.search(track)
                
                
                # try and except block to catch any errors in the download
                try:
                    # letting the user know the song is being downloaded
                    print(f"Downloading song: {songs[0]}")
                    

                    for song in songs:
                        # return true if the song passes the filter
                        if filter(song, query_parsed):
                            # if the song passes the filter, download it
                            spotdl.download(song)
                            
                            # increment the download count
                            download_count += 1
                            # break the loop to move onto the next song
                            break
                # if an error occurs, print the error    
                except Exception as e:
                    # tells the client an error occured
                    client.sendall("ERROR".encode("utf-8"))
                    print(f"An error occurred: {e}")
            # if the download count is greater than the target song count, break the loop
            if download_count >= target_song_count:
                break
            # if the download count is not greater than the target song count, increment the offset and try a new song
            else:
                offset += target_song_count
        # send the client a message to let them know the songs have been downloaded
        client.sendall("SONGS_DOWNLOADED".encode("utf-8"))

    # download the songs from the genre
    def download_genre(self, genre, client):
        # runs the download song function with the genre filter
        self.download_song(genre, client, lambda song, query: any(genre in query["genre"] for genre in song.genres))

    # download the songs from the artist
    def download_artist(self, artist, client):
        # runs the download song function with the artist filter
        self.download_song(artist, client, lambda song, query: any(artist in query["artist"] for artist in song.artists))

    # download the song with the name
    def download_name(self, name, client):
        # runs the download song function with the name filter
        self.download_song(name, client, lambda song, query: query["track"][0].lower() in song.name)

    # download a random song from the given playlist
    def random_song(self, client):
        
        download_count = 0
        # the playlist link
        playlist_link = "5ABHKGoOzxkaa28ttQV9sE"

        while True:
            # get the songs from the playlist
            results = spotify.playlist_tracks(playlist_id=playlist_link, limit=target_song_count, offset=0)
            # get the tracks from the results
            tracks = results['items']
            
            asyncio.set_event_loop(loop)
            # for each track in the playlist, download the song
            for track in tracks:
                if download_count >= target_song_count:
                    break
                
                # get the track uri, name and artist
                track_uri = track["track"]["uri"]
                name = track["track"]["name"]
                artist = track["track"]["artists"][0]["name"]
                # search for the song using the spotdl library
                songs = spotdl.search(track["track"]["external_urls"]["spotify"])

                
                try:

                    for song in songs:
                        # download the song
                        spotdl.download(song)
                    
                        download_count += 1
                        break
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
            if download_count >= target_song_count:
                break
          
        client.sendall("SONGS_DOWNLOADED".encode("utf-8"))





if __name__ == "__main__":
    server = GameServer()
    server.start()