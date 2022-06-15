import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from schlagerradio_hitparade import get_top_50
#
#scope = 'playlist-modify-public'
# scope="playlist-read-private"
# scope="playlist-modify-public"
username = 'docwi'
import json

token = SpotifyOAuth(client_id="6286b2e6875c4a3e80e9d948a6deffc2",
                     client_secret="f01f6b733bae4a709bf2d7731c330912",
                     redirect_uri="http://127.0.0.1:8080/",
                     scope="playlist-read-private",
                     )
spotifyObject = spotipy.Spotify(auth_manager = token)
playlist_db = []
playlists = spotifyObject.current_user_playlists()
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = spotifyObject.next(playlists)
    else:
        playlists = None