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


def download_song():
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

def delayed_function():
  label = Label(window,text="you ran out of time")
  label.pack()

def play_audio():
  playing = AudioSegment.from_mp3("cook.mp3")
  ten_seconds = 10 * 1000
  first_10_seconds = playing[:ten_seconds]
  play(first_10_seconds)

def download_commmand():
  download_thread = Thread(target=download_song)
  download_thread.start()
  #wait for download to finish
  download_thread.join()
  #play the song
  Thread(target=play_audio, daemon=True).start()
  window.after(17000,delayed_function)


def deleting():
  try:
    os.remove("cook.mp3")
  except OSError as e:
    print(f"Error: {e.strerror}. File cook.mp3 could not be removed.")


from tkinter import (
  Toplevel,
  Label,
  Button,
  Entry,
  Tk
)
import tkinter as tkinter

def open_window():
  global window
  window = Toplevel()
  window.geometry('500x300')
  window.title('Guess the artist or song')
  
  Button(window,text='Close',command=deleting).pack()
  Button(window,text='Play',command=download_commmand).pack()
  Label(window,text="Guess:").pack()
  value_entry = Entry(window)
  value_entry.pack()

  # Define our answers
  funcid = None
  global track_name
  track_name = ""
  global artist_name
  artist_name = ""
  answers = [track_name, artist_name]

  # Called whenever we press the enter key
  def key_pressed(key: tkinter.Event):
    # Grab the user input
    value = str(value_entry.get()).strip()

    # Check their answer is within the answers array
    if value in answers:
      Label(window, text="correct").pack()
      

      # Clear the text they entered
      value_entry.delete(0, tkinter.END)
    else:
      # Clear the text they entered
      value_entry.delete(0, tkinter.END)
      Label(window, text="incorrect").pack()


  
  # Listen to when user presses enter
  funcid = window.bind("<Return>",key_pressed)

  window.bind('<Return>', key_pressed)
  window.grab_set()

if __name__ == "__main__":
  app = Tk()
  app.geometry('300x200')
  app.title('Music Quiz ?')
  Button(app,text='Start Game',command=open_window).pack()
  Button(app,text='Exit',command=app.destroy).pack()
  app.mainloop()


#need to loop wihthout changing the tk section somehow
#def the downloading of the song and loop it as a command?




#guess = input("Enter the song or artist name without spaces and caps:\n")
#if guess == track_name or guess == artist_name:
#  print("Correct!")
#  os.remove("cook.mp3")
#  exit()
#else:
#  print("Incorrect!")
#  os.remove("cook.mp3")
#  exit()



