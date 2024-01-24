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

      # Grab ten random songs that are "metal", return their names
      offset = random.randint(0, 1000)
      query = "genre:metal"
      track_urls = [[x["name"], x["external_urls"]["spotify"]]
                    for x in spotify.search(query, offset=offset)["tracks"]["items"]]

      # Search for the song
      print(track_urls)
      songs = spotdl.search(random.choice(track_urls))

      # Attempt to download the song
      #results = spotdl.download_songs(songs)

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
  
