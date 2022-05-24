import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from schlagerradio_hitparade import get_top_50
scope = 'playlist-modify-public'
username = 'docwi'
import json

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6286b2e6875c4a3e80e9d948a6deffc2",
#                                                client_secret="f01f6b733bae4a709bf2d7731c330912",
#                                                redirect_uri="http://127.0.0.1:8080/",
#                                                scope="user-library-read"))

schlagerradio_titles_db = get_top_50()
for title in schlagerradio_titles_db:
    search_title = title.split(' - ')[1]
    print('search_title: ', search_title)




token = SpotifyOAuth(client_id="6286b2e6875c4a3e80e9d948a6deffc2",
                     client_secret="f01f6b733bae4a709bf2d7731c330912",
                     redirect_uri="http://127.0.0.1:8080/",
                     scope="playlist-modify-public")
spotifyObject = spotipy.Spotify(auth_manager = token)

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

# create the playlist
playlist_name = "MySchlagerradio"
playlist_description = "MySchlagerradio"


# playlist_name = input("Enter a playlist name: ")
# playlist_description = input("Enter a playlist description: ")

# Create new playlist
spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)

#user_input = input('Enter the song: ')
list_of_songs = []

# while user_input != 'quit':
#     print('list: ', list_of_songs)
#     result = spotifyObject.search(q=user_input)
#     list_of_songs.append(result['tracks']['items'][0]['uri'])
#     print('list: ', list_of_songs)
#     user_input = input('Enter the song: ')
for single_title in schlagerradio_titles_db[:]:
    print(single_title)
    search_title = single_title.split(' - ')[1]
    result = spotifyObject.search(q=search_title)
    list_of_songs.append(result['tracks']['items'][0]['uri'])
#    time.sleep(2)

    #user_input = input('Enter song: ')

# find the new playlist
# prePlaylist = spotifyObject.user_playlists(user=username)
# playlist = prePlaylist['items'][0]['id']
#
# # Add songs
# spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist,
#                                         tracks=list_of_songs)
# #print('Playlist: ', playlist)
#
