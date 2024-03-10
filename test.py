from tinytag import TinyTag
tag = TinyTag.get('f.wav')

artist = tag.artist
genre = tag.genre
year = tag.year
print(artist)
print(genre)
print(year)