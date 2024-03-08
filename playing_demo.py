from pydub import AudioSegment
from pydub import *
from pydub.playback import play


playing = AudioSegment.from_mp3("C:\\Users\\wiloj\\Documents\\GitHub\\Project\\spotify_api\\please.mp3")

ten_seconds = 10 * 1000
sliced = playing[0:ten_seconds]

play(playing)