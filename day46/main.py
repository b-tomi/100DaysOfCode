# Musical Time Machine

import datetime as dt

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import config

# number of years to go back, make sure there was a Billboard chart published
YEARS_AGO = 20
PAGE_URL = "https://www.billboard.com/charts/hot-100/"
# the scope required by the Spotify API, to allow the creation and modification of playlists
SCOPE = "playlist-modify-private"
# instead of some fake website address, just using localhost for this
REDIRECT_URL = "http://localhost:8888/callback"


def get_date():
    """Returns the date in the past as STR, as going back the defined amount of years."""
    # get today's date as a list
    today = dt.datetime.now().strftime("%Y-%m-%d").split("-")
    past_year = int(today[0]) - YEARS_AGO
    # just replace the year
    past_date = f"{past_year}-{today[1]}-{today[2]}"
    return past_date


def load_site(past_date):
    """Takes a date as STR and scrapes the defined site, returns songs and artists as LISTs."""
    page_url = PAGE_URL + past_date
    response = requests.get(url=page_url)
    # check the encoding of the file, this returned "ISO-8859-1"
    # print(response.encoding)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    all_songs = soup.select(".chart-element__information .chart-element__information__song")
    all_artists = soup.select(".chart-element__information .chart-element__information__artist")
    # using list comprehensions, just get the texts
    songs = [song.get_text() for song in all_songs]
    artists = [artist.get_text() for artist in all_artists]
    return songs, artists


# calculate the date in the past
date = get_date()
# get lists of songs and artists for that year
song_list, artist_list = load_site(date)

# authorize through spotipy, at the first run this will open the web browser for confirmation and generate token.txt
oauth = SpotifyOAuth(scope=SCOPE, redirect_uri=REDIRECT_URL,
                     client_id=config.SPOTIFY_ID,
                     client_secret=config.SPOTIFY_SECRET,
                     show_dialog=True, cache_path="token.txt")
sp = spotipy.Spotify(auth_manager=oauth)

song_urls = []
for i in range(100):
    # used just for verification, the artist name turned out to be unnecessary in the end
    # print(f"#{i + 1}: {song_list[i]} by {artist_list[i]}")
    result = sp.search(q=f"track:{song_list[i]} year:{date[:4]}", type="track")
    try:
        url = result["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"{song_list[i]} by {artist_list[i]} doesn't seem to exist in Spotify.")
    else:
        song_urls.append(url)

# get the user ID
user_id = sp.current_user()["id"]
# create the playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# add the songs
result = sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_urls)
