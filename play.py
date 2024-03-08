import time
from threading import Thread
import playsound

song = "please.mp3"
def play_music():
    playsound.playsound(song)

t=Thread(target=play_music)
t.daemon = True
t.start()
print("Playing")
start_time = time.time()
while (time.time() - start_time) < 10:
    print("Running...")