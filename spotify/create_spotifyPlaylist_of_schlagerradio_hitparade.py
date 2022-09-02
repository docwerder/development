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

print('schlagerradio_titles_db', schlagerradio_titles_db)
#for nr, title in enumerate(schlagerradio_titles_db):
#    if nr == 45:
#        continue
    #print('nr: ', nr)
#    search_title = title.split(' - ')[1]
    #print('search_title: ', search_title)




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
playlist_name = input('Name of the playlist: ')
#playlist_name = "MySchlagerradio_05_06"
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


artist = []
single_title = []
for lf in schlagerradio_titles_db[:]:
    artist_tmp = lf.split(' - ')[0].split('.', 1)[1]
    single_title_tmp = lf.split(' - ')[1]
    searchQuery = artist_tmp + ' ' + single_title_tmp

    if "Wolfgang Petry" in artist_tmp:
        searchQuery = 'Wolfgang Petry Geboren für den Augenblick'


    # elif "Cora" in artist_tmp:
    #     continue
    # elif "Alva" in artist_tmp:
    #     continue
    # elif "Wolfgang" in artist_tmp:
    #     continue
    # elif "Andreas" in artist_tmp:
    #     continue

    # elif "Francine" in artist_tmp:   # anpassen mit dem Code aus dem ersten Teil, nur Title suchen!
    #     continue
    # elif "Howard" in artist_tmp:
    #     continue
    #single_title_tmp = lf.split(' - ')[1]

    #searchQuery = artist_tmp + ' ' + single_title_tmp
    searchResults = spotifyObject.search(q=searchQuery)
    print('searchResults: ', searchResults)
    if not bool(searchResults['tracks']['items']):
        print('List is empty!')
    else:
        single_title_tmp_1 = searchResults['tracks']['items'][0]['uri']
        list_of_songs.append(single_title_tmp_1)
        #list_of_songs.append(searchResults['tracks']['items'][0]['uri'])
    print('list_of_songs: ', list_of_songs)

    #artist.append(lf.split(' - ')[0].split('.', 1)[1])
    #single_title.append(lf.split(' - ')[1])


# for nr, single_title in enumerate(schlagerradio_titles_db[:5]):
#
#
#     print('Nr: ', nr)
#     if nr == 24:
#         continue
#
#     # print(single_title)
#     # artist = single_title.split(' - ')[0]
#     # track = single_title.split(' - ')[1]
#     # search_title = single_title.split(' - ')#[1]
#     #print('search_title: ', search_title)
#     searchQuery = artist + ' ' + track
#     #print('query: ', searchQuery)
#     #result = spotifyObject.search(q=searchQuery)
#     ##result = spotifyObject.search(q=search_title)
#     ##list_of_songs.append(result['tracks']['items'][0]['uri'])
#
#     searchQuery = artist + ' ' + track
#     searchResults = spotifyObject.search(q=searchQuery)
#     print('searchResults: ', searchResults)
#     #print('list: ', list_of_songs);
#
#     #user_input = input('Enter song: ')
#
# find the new playlist
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']


# Add songs
spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist,
                                         tracks=list_of_songs)

print('end...')
#
