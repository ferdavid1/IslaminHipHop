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
import simplejson
import os
from operator import itemgetter
import urllib
import spotipy
import sys
import io
from search import search, setup
import pandas as pd
from more_itertools import unique_everseen
import matplotlib
matplotlib.use("Pdf")
import numpy as np
import matplotlib.pyplot as plt

# coding=utf-8
client_id = 't3OnC4Qg3c9LnGJICuyI3Oo3uoSn095HvOrkZsfABVixM7_ONvumxsM0Fyqe7zDe'
client_secret = 'xtfVDI4l5K3umFml14LDccNpkdKci2u0pXMfNv6SfgVYjGDfZaLuNrv9ykj4WkywWfpOS5ulw89-h4biRw4uBw'
access_token = 'sBJ2OYn3KjvA9VvVxhTetiMNPTGDWlg0fEjuwwE4K2Yb4HM6TP_F3TZr24YOOW-0'
# look for songs that have genre of rap and contain the words in list
islamic_words = ['allah', 'Allah', 'Assalaamu', 'Alaikum', 'assalaamu', 'As-Salaam-Alaikum','alaikum', 'Alaikum', 'Ayatollah', 'ayatollah', 'Barakah', 'barakah', 'Caliph', 'caliph', 'Hajj', 'hajj', 'Hijra', 'hijra', 'Iman', 'iman', 'jinn', 'Jinn', 'jihad', 'Jihad', "Ka'ba", "ka'ba", 'Kafir', 'kafir', 'Koran', "Qur'an", 'koran', 'Mosque', 'mosque', 'Muhammed', 'Ramadan', 'Salaam', 'salaam', "Shari'ah", "shari'ah", "Shi'ite", 'Sufi', 'sufi', 'Zakat', 'zakat']
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
    for i in range(30):
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
            data = pd.read_csv('output/' + file, encoding='utf-8')
            print('Parsing file for key terms...')
            for x in range(3):
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
                except (TypeError, IndexError, simplejson.scanner.JSONDecodeError,requests.exceptions.ConnectionError):
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

ax.set_ylabel('number of times a word from list was used')
ax.set_title('Number of words by artist')
ax.set_xticks(ind + width / 2)

plt.savefig('top_artists')

