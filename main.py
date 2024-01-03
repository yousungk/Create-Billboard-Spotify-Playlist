from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# set up connection to spotify
auth_client_id = os.environ.get("auth_client_id")
auth_client_secret = os.environ.get("auth_client_secret")
spotify_username = os.environ.get("spotify_username")
OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=auth_client_id,
            client_secret=auth_client_secret,
            redirect_uri="http://example.com",
            scope="playlist-modify-private",
            cache_path="token.txt",
            username=spotify_username,
        )
    )

user_id = sp.current_user()["id"]

# set target date
year = input("What date do you want to retrieve the Billboard 100 from? Type the data in this format YYYY-MM-DD:\n")

# scrape top 100 song titles on that date into list
URL = f"https://www.billboard.com/charts/hot-100/{year}"
response = requests.get(URL)
data = response.text
soup = BeautifulSoup(data, "html.parser")
songs = soup.select("li ul li h3")
songs = [song.getText().strip() for song in songs]

# create spotify playlist
playlist_id = sp.user_playlist_create(
    user=user_id,
    name=f"{year} Billboard 100",
    public=False,
    collaborative=False
)

# create list of song URLs
song_uris = []
year = year.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesnt' exist in Spotify. Skipped.")

# add songs to playlist
sp.playlist_add_items(
    playlist_id=playlist_id["id"],
    items=song_uris
)






