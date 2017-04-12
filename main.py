'''references: 
https://www.namb.net/apologetics/popular-islamic-terms
https://github.com/jasonqng/genius-lyrics-search
https://github.com/plamere/spotipy
'''
import requests
import six
import lxml
from bs4 import BeautifulSoup
import argparse
import json
import os
from operator import itemgetter
import urllib
import spotipy
import sys
import io
from search import search, setup
import pandas as pd
from more_itertools import unique_everseen
import numpy as np
import matplotlib.pyplot as plt

client_id = ''
client_secret = ''
access_token = ''
# look for songs that have genre of rap and contain the words in list
islamic_words = ['allah', 'Allah', 'Assalaamu', 'Álaikum', 'assalaamu', 'As-Salaam-Alaikum','alaikum', 'Alaikum', 'Ayatollah', 'ayatollah', 'Barakah', 'barakah', 'Caliph', 'caliph', 'Hajj', 'hajj', 'Hijra', 'hijra', 'Iman', 'iman', 'jinn', 'Jinn', 'jihad', 'Jihad', "Ka'ba", "ka'ba", 'Kafir', 'kafir', 'Koran', "Qur'an", 'koran', 'Mosque', 'mosque', 'Muhammed', 'Ramadan', 'Salaam', 'salaam', "Shari'ah", "shari'ah", "Shi'ite", 'Sufi', 'sufi', 'Zakat', 'zakat']
sp = spotipy.Spotify()

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def get_genres(artist):
    artist = get_artist(artist)
    return artist['genres']


def find_lyrics():
    for i in range(len(islamic_words)):
        try: 
            search(islamic_words[i], setup(islamic_words[i]), access_token)
        except (UnicodeEncodeError, urllib.error.HTTPError):
            pass
    # search(islamic_words[0], setup(islamic_words[0]), access_token)

# find_lyrics() --> this creates the datasets

songs = []
artists = []
final_dict = {}

for parent, blank, files in os.walk('output/'):
    for file in files:
        try:
            data = pd.read_csv('output/' + file)
            print('Parsing file for key terms...')
            for x in range(10):
                song = data.iloc[x]
                try: 
                    genres = get_genres(song['primaryartist_name'])
                    for genre in genres:
                        if 'hip hop' in genre:
                            songs.append(song['title'])
                            artists.append(song['primaryartist_name'])
                        elif 'rap' in genre:
                            songs.append(song['title'])
                            artists.append(song['primaryartist_name'])
                        elif 'hip-hop' in genre:
                            songs.append(song['title'])
                            artists.append(song['primaryartist_name'])
                except (TypeError, IndexError):
                    pass
            print('...' + file + ' parsed')
        except OSError:
            pass
    

unique_songs = list(unique_everseen(songs))
# print(unique_songs)
unique_artists = list(unique_everseen(artists))

for artist in artists:
    final_dict[artist] = artists.count(artist)
# print(final_dict)
final_dict['Joey Badass'] = final_dict.pop('Joey Bada$$') # the '$$' in joey's name causes a matplotlib Error, as it interprets it as a symbol, instead of text

sorted_dict = sorted(final_dict.items(), key=itemgetter(1))
sorted_dict.reverse()
print('\nThe top 10 ranked artists who most use any of the popular islamic words are: {}'.format(sorted_dict[:10]))

N = len(sorted_dict[:10])
ind = np.arange(N)  # the x locations for the groups
width = 0.5       # the width of the bars

fig, ax = plt.subplots()
ax.bar(ind, [artist[1] for artist in sorted_dict[:10]], width)
    # add some text for labels, title and axes ticks
ax.set_xticklabels([artist[0] for artist in sorted_dict[:10]])

ax.set_ylabel('# of times a word from list was used')
ax.set_title('Number of words by artist')
ax.set_xticks(ind + width / 2)

plt.show()