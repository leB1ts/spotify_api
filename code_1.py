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
from threading import Thread

from tkinter import (
  Toplevel,
  Label,
  Button,
  Entry,
  Tk
)
import tkinter as tkinter

class GameWindow:
    def __init__(self):
        pass
        
    def start_game(self):
      self.window2 = Toplevel()
      self.window2.geometry('500x300')
      self.window2.title('Guess the artist or song')
      Button(self.window2,text='Close',command=self.deleting).pack()
      Button(self.window2,text='Play',command=self.play_next).pack()
      
      
    def download_song(self):
      load_dotenv()

      client_id = os.environ.get("SPOTIPY_CLIENT_ID")
      client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")


      spotify = Spotify(client_credentials_manager=SpotifyClientCredentials())
      spotdl = Spotdl(client_id,
                      client_secret)

      # Grab ten random songs and return their names
      
      

      pre_year = ""
      pre_artist = ""
      pre_genre = ""

      parameters_window = Toplevel()
      parameters_window.geometry('300x200')
      parameters_window.title('Choose one field to narow the game down or try a challenge of all random')
      Button(parameters_window, text="Genre", command = the_genre).pack()
      Button(parameters_window, text="Year", command = the_year).pack()
      Button(parameters_window, text="Artist", command = the_artist).pack()
      Button(parameters_window, text="All Random", command = all_random).pack()


      #need to do individualy where user chooses one or no metrics otherwise way too specific ie bob jazz 1975 is like one song for example
      #https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b
      def the_genre():
        genre_window = Toplevel():
        genre_window.geometery("300x200")
        Label(genre_window, text="Choose a specific genre").pack()
        genre_entry = Entry(genre_window)
        genre_entry.pack()
        # Called whenever we press the enter key
        def key_pressed(key: tkinter.Event):
          # Grab the user input
          global genre_value
          genre_value = str(genre_entry.get()).strip()

        genre_widnow.bind('<Return>', key_pressed)
        genre_window.grab_set()

        genre = "genre:",genre_value
        track_urls = [[x["name"], x["external_urls"]["spotify"]]
                    for x in spotify.search(genre, offset=offset)["tracks"]["items"]]

        # Attempt to download the song
      
        songs = spotdl.search(random.choice(track_urls))
        song = spotdl.download(songs[0])
        #could create a thread to download the other 10 songs in the background instead of one then rerunning to get another


      def Artist():
        artist_window = Toplevel()
        artist_window.geometry('300x200')
        Label(artist_window, text="Choose a specific Artist").pack()
        artisit_entry = Entry(artist_window)
        artisit_entry.pack()
        # Called whenever we press the enter key
        def key_pressed(key: tkinter.Event):
          # Grab the user input
          global artist_value
          artist_value = str(artist_entry.get()).strip()

        artist_widnow.bind('<Return>', key_pressed)
        artist_window.grab_set()

        artist = "name:",artist_value,"type:artist"
        track_urls = [[x["name"], x["external_urls"]["spotify"]]
                    for x in spotify.search(artist, offset=offset)["tracks"]["items"]]

        # Attempt to download the song
      
        songs = spotdl.search(random.choice(track_urls))
        song = spotdl.download(songs[0])
        #could create a thread to download the other 10 songs in the background instead of one then rerunning to get another

      def Year():
        year_window = Toplevel()
        year_window.geometry('300x200')
        Label(year_window, text="Enter a specific Year or a range/n i.e 1960-1969").pack()
        year_entry = Entry(year_window)
        year_entry.pack()
        # Called whenever we press the enter key
        def key_pressed(key: tkinter.Event):
          # Grab the user input
          global year_value
          year_value = str(artist_entry.get()).strip()

        artist_widnow.bind('<Return>', key_pressed)
        artist_window.grab_set()

        year = "year:",year_value
        track_urls = [[x["name"], x["external_urls"]["spotify"]]
                    for x in spotify.search(year, offset=offset)["tracks"]["items"]]

        # Attempt to download the song
      
        songs = spotdl.search(random.choice(track_urls))
        song = spotdl.download(songs[0])
        #could create a thread to download the other 10 songs in the background instead of one then rerunning to get another

      def Random():
        random_window = Toplevel()
        random_window.geometry('300x200')
        Label(random_window, text="Random").pack()


      Button(parameters_window, text="Genre",command=Genre).pack()

      Button(parameters_window, text="Artist", command= Artist).pack()

      Button(parameters_window, text="Year", command= Year).pack()

      Button(parameters_window, text="Random", command= Random).pack()


      

      def enter_data():
        global offset
        offset = random.randint(0, 1000)
        global pre_genre
        pre_genre = str(genre_entry.get())
        global pre_artist
        pre_artist = str(artist_entry.get())
        global pre_year
        pre_year = str(year_entry.get())
        parameters_window.destroy()
        
        genre = pre_genre
        if genre == "random":
          query1 = "genre:" + random.choice(["rock", "pop", "hip-hop", "country", "jazz", "classical", "metal"])
        else:
          query1 = "genre:" + genre

        artist = pre_artist
        if artist != "random":
          query2 = "artist:" + artist
        else:
          query2 = ""

        year = pre_year
        if year != "random":
          query3 = "year:" + year
        else:
          query3 = ""

        global track_urls
        track_urls = [[x["name"], x["external_urls"]["spotify"]]
                    for x in spotify.search(query1, query2, query3, offset=offset)["tracks"]["items"]]

      Button(parameters_window, text="Submit", command=enter_data).pack()

      
      # Attempt to download the song
      
      songs = spotdl.search(random.choice(track_urls))
      song = spotdl.download(songs[0])

      #find the song name of the mp3
      mp3_files = glob.glob("*.mp3")
      print(mp3_files)

      #need to get the name without the [" "] so it can be played using playsound
      song_name = mp3_files[0].replace("[", "").replace("]", "").replace(" ","")
      print(song_name)

      file = mp3_files[0]

      global track_name
      global artist_name

      split = song_name.partition("-")
      track_name = split[0]
      artist = split[2]
      artist_name = artist.partition(".")
      artist_name = artist_name[0]
      
      print(track_name,artist_name)
      

      print(file)

      os.rename(file,"cook.mp3")    

      #self.play_audio()

    def guess(self):
        Label(self.window2,text="Guess:").pack()
        value_entry = Entry(self.window2)
        value_entry.pack()
        # Define our answers
        funcid = None
        answers = [track_name, artist_name]

        # Called whenever we press the enter key
        def key_pressed(key: tkinter.Event):
          # Grab the user input
          value = str(value_entry.get()).strip()

          # Check their answer is within the answers array
          if value in answers:
            Label(self.window2, text="correct").pack()
            

            # Clear the text they entered
            value_entry.delete(0, tkinter.END)
          else:
            # Clear the text they entered
            value_entry.delete(0, tkinter.END)
            Label(self.window2, text="incorrect").pack()


        
        # Listen to when user presses enter
        funcid = self.window2.bind("<Return>",key_pressed)

        self.window2.bind('<Return>', key_pressed)
        self.window2.grab_set()

    def play_audio(self):
        playing = AudioSegment.from_mp3("cook.mp3")
        ten_seconds = 10 * 1000
        first_10_seconds = playing[:ten_seconds]
        #hasing out playing audio for now
        #play(first_10_seconds)
        self.guess()
    
    def play_next(self):
       self.download_song()
       self.play_audio()

    def deleting(self):
      try:
        os.remove("cook.mp3")
      except OSError as e:
        print(f"Error: {e.strerror}. File cook.mp3 could not be removed.")

    # Rest of your functions...
if __name__ == "__main__":
  app = Tk()
  app.geometry('300x200')
  app.title('Music Quiz ?')
  game_window = GameWindow()
  Button(app,text='Start Game',command=game_window.start_game).pack()
  Button(app,text='Exit',command=app.destroy).pack()
  app.mainloop()
  













# def game_over():
#   deleting()
#   windowend = Toplevel()
#   windowend.geometry('500x300')
#   windowend.title('Game Over')
#   Label(windowend,text='Game Over').pack()
#   Button(windowend,text='Exit',command=windowend.destroy).pack()



# def play_audio_and_then_delay():
#   play_audio()
#   window2.after(5000, delayed_function)

# def download_commmand():
#   download_thread = Thread(target=download_song)
#   download_thread.start()
#   #wait for download to finish
#   download_thread.join()
#   #play the song
#   #SCEW THE BACKGROUND TASK PLAY AUDIO THEN GUESS AFTER QUICK FIX MOVE ON
#   thread = Thread(target=play_audio, daemon=False)
#   thread.start()
  
