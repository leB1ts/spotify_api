# Dependencies
# https://stackoverflow.com/questions/65240392/how-can-i-use-spotdl-inside-python
import os
from os import system
import random
from spotdl import Spotdl
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotdl.utils.ffmpeg import download_ffmpeg
import glob
import time
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
import threading
import sqlite3
from collections import Counter
import re


from tkinter import Toplevel, Label, Button, Entry, Tk
import tkinter as tkinter

points = 0
global total_guesses
total_guesses = 0
global correct_guesses
correct_guesses = 0


# connect to the database
conn = sqlite3.connect("users_client.db")
cursor = conn.cursor()
# add streaks maybe
cursor.execute(
    """
  CREATE TABLE IF NOT EXISTS stats(
    user_id INTEGER PRIMARY KEY,
    best_genre TEXT,
    best_artist TEXT,
    best_year INTEGER,
    best_points INTEGER,
    accuracy INTEGER 
  )
"""
)
conn.commit()

load_dotenv()

client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")


spotify = Spotify(client_credentials_manager=SpotifyClientCredentials())
spotdl = Spotdl(client_id, client_secret)




class GameWindow:
    def __init__(self):
        pass

    def start_game(self, client):
        self.client = client
        self.first_window = Toplevel()
        self.first_window.geometry("500x300")
        self.first_window.title("Song Guesser")
        Button(self.first_window, text="Start Game", command=self.playing_game).pack()
        # stats page link to stats menu
        Button(self.first_window, text="Stats", command=self.show_stats).pack()
        Button(self.first_window, text="Exit", command=self.first_window.destroy).pack()

    def playing_game(self):
        self.window2 = Toplevel()
        self.window2.geometry("500x300")
        self.window2.title("Guess the artist or song")
        Button(self.window2, text="Close", command=self.deleting).pack()
        Button(self.window2, text="Play", command=self.download_song).pack()

    def show_stats(self):
        stats_window = Toplevel()
        stats_window.geometry("300x200")
        stats_window.title("Stats")
        # get the best genre from the text file
        def most_common_genre():
            with open("genre.txt", "r") as f:
                genre = f.read()
            words = re.findall(r'\w+', genre.lower())
            most_common_genre = Counter(words).most_common(1)
            return most_common_genre[0] if most_common_genre else None
        highest_genre = most_common_genre()
        
        def most_common_year():
            with open("year.txt", "r") as f:
                year = f.read()
            words = re.findall(r'\w+', year.lower())
            most_common_year = Counter(words).most_common(1)
            return most_common_year[0] if most_common_year else None   
        highest_year = most_common_year()
        
        def most_common_artist():
            with open("artist.txt", "r") as f:
                artist = f.read()
            words = re.findall(r'\w+', artist.lower())
            most_common_artist = Counter(words).most_common(1)
            return most_common_artist[0] if most_common_artist else None  
        highest_artist = most_common_artist()
        
        #send the highest genre, year and artist to the database
        cursor.execute(
              "INSERT INTO stats(best_genre, best_artist, best_year) VALUES(?,?,?)",
                    (highest_genre, highest_artist, highest_year),
                )
        conn.commit()
        # get the highest points from the database
        cursor.execute("SELECT best_artist FROM stats")
        best_artist = cursor.fetchone()
        # get the highest accuracy from the database
        cursor.execute("SELECT accuracy FROM stats")
        accuracy = cursor.fetchone()
        # get the highest genre from the database
        cursor.execute("SELECT best_genre FROM stats")
        highest_genre = cursor.fetchone()
        #get the highest year from the database
        cursor.execute("SELECT best_year FROM stats")
        highest_year = cursor.fetchone()
        # display the highest genre, year, artist, points and accuracy
        Label(stats_window, text=f"Best Genre: {highest_genre}").pack()
        Label(stats_window, text=f"Best Artist: {best_artist}").pack()
        Label(stats_window, text=f"Best Year: {highest_year}").pack()
        Label(stats_window, text=f"Accuracy: {accuracy}").pack()
        
        



    def the_genre(self):
        #offset = random.randint(0, 1000)
        genre_window = Toplevel()
        genre_window.geometry("300x200")
        Label(genre_window, text="Choose a specific genre").pack()
        genre_entry = Entry(genre_window)
        genre_entry.pack()

        # Called whenever we press the enter key
        def key_pressed(key: tkinter.Event):
            # Grab the user input
            global genre_value
            genre_value = str(genre_entry.get()).strip()
            #SEND THE GENRE VALUE TO THE SERVER WHERE THE SERVER WILL DOWNLOAD THE SONG
            # NEED A TRY AND EXCEPT FOR THE GENRE TO ACTUALLY EXIST
            genre = "genre:" + genre_value
            #how to send the genre to the server?
            self.client.send(genre)
            #track_urls = [
            #    [x["name"], x["external_urls"]["spotify"]]
             #   for x in spotify.search(genre, offset=offset)["tracks"]["items"]
            #]

            # Attempt to download the song

            #songs = spotdl.search(random.choice(track_urls))
            #song = spotdl.download(songs[0])
            # find the song name of the mp3
            #mp3_files = glob.glob("*.mp3")
            #print(mp3_files)

            # need to get the name without the [" "] so it can be played using playsound
            #song_name = mp3_files[0].replace("[", "").replace("]", "").replace(" ", "")
            #print(song_name)

            #file = mp3_files[0]

            #global track_name
            #global artist_name

            #split = song_name.partition("-")
            #track_name = split[0]
            #artist = split[2]
            #artist_name = artist.partition(".")
            #artist_name = artist_name[0]

            #print(track_name, artist_name)

            #print(file)

            #os.rename(file, "cook.mp3")

        # could create a thread to download the other 10 songs in the background instead of one then rerunning to get another
        genre_window.bind("<Return>", key_pressed)
        genre_window.grab_set()

    def the_artist(self):
        offset = random.randint(0, 50)
        artist_window = Toplevel()
        artist_window.geometry("300x200")
        Label(artist_window, text="Choose a specific Artist").pack()
        artist_entry = Entry(artist_window)
        artist_entry.pack()

        # Called whenever we press the enter key
        def key_pressed(key: tkinter.Event):
            # Grab the user input
            global artist_value
            artist_value = str(artist_entry.get()).strip()
            artist = "name:" + artist_value
            self.client.send(artist)
            #track_urls = [
            #    [x["name"], x["external_urls"]["spotify"]]
             #   for x in spotify.search(artist, offset=offset)["tracks"]["items"]
            #]

            # Attempt to download the song

            #songs = spotdl.search(random.choice(track_urls))
            #song = spotdl.download(songs[0])
            # could create a thread to download the other 10 songs in the background instead of one then rerunning to get another
            # find the song name of the mp3
            #mp3_files = glob.glob("*.mp3")
            #print(mp3_files)

            # need to get the name without the [" "] so it can be played using playsound
            #song_name = mp3_files[0].replace("[", "").replace("]", "").replace(" ", "")
            #print(song_name)

            #file = mp3_files[0]

            #global track_name
            #global artist_name

            #split = song_name.partition("-")
            #track_name = split[0]
            #artist = split[2]
            #artist_name = artist.partition(".")
            #artist_name = artist_name[0]

            #print(track_name, artist_name)

            #print(file)

            #os.rename(file, "cook.mp3")

        artist_window.bind("<Return>", key_pressed)
        artist_window.grab_set()

    def the_year(self):
        offset = random.randint(0, 1000)
        year_window = Toplevel()
        year_window.geometry("300x200")
        Label(
            year_window, text="Enter a specific Year or a range/n i.e 1960-1969"
        ).pack()
        year_entry = Entry(year_window)
        year_entry.pack()

        # Called whenever we press the enter key
        def key_pressed(key: tkinter.Event):
            # Grab the user input
            global year_value
            year_value = str(year_entry.get()).strip()
            year = "year:" + year_value
            self.client.send(year)
            #track_urls = [
            #    [x["name"], x["external_urls"]["spotify"]]
            #    for x in spotify.search(year, offset=offset)["tracks"]["items"]
            #]

            # Attempt to download the song

            #songs = spotdl.search(random.choice(track_urls))
            #song = spotdl.download(songs[0])
            # find the song name of the mp3
            #mp3_files = glob.glob("*.mp3")
            #print(mp3_files)

            # need to get the name without the [" "] so it can be played using playsound
            #song_name = mp3_files[0].replace("[", "").replace("]", "").replace(" ", "")
            #print(song_name)

            #file = mp3_files[0]

            #global track_name
            #global artist_name

            #split = song_name.partition("-")
            #track_name = split[0]
            #artist = split[2]
            #artist_name = artist.partition(".")
            #artist_name = artist_name[0]

            #print(track_name, artist_name)

            #print(file)

            #os.rename(file, "cook.mp3")

            # could create a thread to download the other 10 songs in the background instead of one then rerunning to get another

        year_window.bind("<Return>", key_pressed)
        year_window.grab_set()

    def all_random(self):
        self.client.send("random")

    def download_song(self):

        parameters_window = Toplevel()
        parameters_window.geometry("300x200")
        parameters_window.title(
            "Choose one field to narow the game down or try a challenge of all random"
        )
        Button(parameters_window, text="Genre", command=self.the_genre).pack()
        Button(parameters_window, text="Year", command=self.the_year).pack()
        Button(parameters_window, text="Artist", command=self.the_artist).pack()
        Button(parameters_window, text="All Random", command=self.all_random).pack()

    def countdown_timer(self):
        global seconds
        seconds = 20
        # needs to a threads
        while seconds > 0:
            print(f"Time remaining: {seconds} seconds")
            time.sleep(1)
            seconds -= 1

    def guess(self, audio_file):
        guess_window = Toplevel()
        guess_window.geometry("300x200")
        guess_window.title("Guess the song or artist")

        # thread for countdown
        thread = threading.Thread(target=self.countdown_timer, daemon=False)

        Label(guess_window, text="Guess:").pack()
        thread.start()
        value_entry = Entry(guess_window)
        value_entry.pack()
        # Define our answers
        funcid = None
        file_name = os.path.basename(audio_file)
        split = file_name.partition("-")
        track_name = split[2]
        artist_name = split[0]
        print(track_name, artist_name)
        answers = [track_name, artist_name]

        # Called whenever we press the enter key
        def key_pressed(key: tkinter.Event):
            # Grab the user input
            value = str(value_entry.get()).strip()
            global total_guesses
            total_guesses += 1

            # Check their answer is within the answers array
            if value in answers:
                Label(guess_window, text="correct").pack()
                points = points + seconds
                global correct_guesses
                correct_guesses += 1
                accuracy = (correct_guesses / total_guesses) * 100
                # wrtie the genre to a text file
                with open("genre.txt", "w") as f:
                    f.write(genre_value)
                # for the most common value of the genre store it in the database

                # wrtie the artist to a text file
                with open("artist.txt", "w") as f:
                    f.write(artist_value)
                # wrtie the year to a text file
                with open("year.txt", "w") as f:
                    f.write(year_value)
                # send key info to stats page via sql
                cursor.execute(
                    """
              INSERT INTO stats(accuracy) VALUES(?)
            """,
                    accuracy,
                )
                conn.commit()

                # Clear the text they entered
                value_entry.delete(0, tkinter.END)
            else:
                # Clear the text they entered
                value_entry.delete(0, tkinter.END)
                Label(guess_window, text="incorrect").pack()

        # Listen to when user presses enter

        guess_window.bind("<Return>", key_pressed)
        guess_window.grab_set()

    def play_audio(self, audio_file):
        playing = AudioSegment.from_mp3(audio_file)
        ten_seconds = 10 * 1000
        first_10_seconds = playing[:ten_seconds]
        threading.Thread(target=play, args=(first_10_seconds,)).start()

        self.guess(audio_file)

    def choose_random_mp3(self):
        # Get a list of all MP3 files in the directory
        # run as adminm if not work kms
        mp3_files = glob.glob("C:\\Users\\wiloj\\Documents\\GitHub\\Project\\spotify_api\\*.mp3")
        audio_file_ = random.choice(mp3_files)
        return audio_file_
    
    def play_next(self):
        # choose the first song to play
        audio_file = self.choose_random_mp3()
        #guess bit here aswell
        threading.Thread(target=self.play_audio, args=(audio_file,)).start()
        

    def deleting(self):
        try:
            os.remove("cook.mp3")
        except OSError as e:
            print(f"Error: {e.strerror}. File cook.mp3 could not be removed.")

    # Rest of your functions...


if __name__ == "__main__":
    app = Tk()
    #app.geometry("300x200")
    #app.title("Music Quiz ?")
    game_window = GameWindow()
    #Button(app, text="Start Game", command=game_window.start_game).pack()
    # stats page link to a new window
    #Button(app, text="Stats", command=game_window.show_stats).pack()
    #Button(app, text="Exit", command=app.destroy).pack()
    app.mainloop()
