#psuedocode for the points system
import time
points = 0
#countdown and answers need to be integrated seperately from each other? because your setting seconds to score points

#countdown timer
def countdown_timer():
    global seconds
    seconds = 20
    #needs to a threads
    while seconds > 0:
        print(f"Time remaining: {seconds} seconds")
        time.sleep(1)
        seconds -= 1

if answer in answers:
    points = points + seconds


