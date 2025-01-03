import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import psycopg2
from database import preprocess_data

class PlaylistInfos:
    def __init__(self, name, cover):
        self.name = name
        self.cover = cover
class Playlist:
    def __init__(self, name, cover, analysis, ids, songs):
        self.infos = PlaylistInfos(name, cover)
        self.analysis = analysis
        self.ids = ids
        self.songs = songs

class Track:
    def __init__(self, name, artists, id):
        self.id = id
        self.name = name
        self.artists = artists

class Similarity:
    def __init__(self, track_id, distance):
        self.track_id = track_id
        self.distance = distance

def get_database_ids(filters = "", quantity = ""):
    conn = psycopg2.connect(
        database = "brkanprod74pdkfy9yvk",
        host = "brkanprod74pdkfy9yvk-postgresql.services.clever-cloud.com",
        user = "ug3heau5juubxgihbkv5",
        password = "CSW5GBLb5mQJo5aKd83RGV3I1Qflbv",
        port = "50013"
    )
    cursor = conn.cursor()

    cursor.execute(f"SELECT track_id FROM tracks {filters} {quantity}")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    ids = []

    for item in data:
        ids.append(item[0])

    return ids

def connect_to_spotify():
    client_id = os.environ.get("SPOTIFY_CLIENT")
    client_secret = os.environ.get("SPOTIFY_SECRET")

    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def find_infos_about_songs(ids, start, end):
    sp = connect_to_spotify()

    playlist_songs = []

    if len(ids) > 50:
        for item in sp.tracks(ids[start:end])['tracks']:
            item_id = item['id']
            item_name = item['name']
            item_artists = item['artists'][0]['name']
            playlist_songs.append(Track(item_name, item_artists, item_id))
    return playlist_songs

def print_songs(playlist_songs):
    for item in playlist_songs:
        print(item.name, '-', item.artists, '-', item.id)

def generate_filter(artists):
    query_filter = ''
    for item in artists:
        query_filter += f"lower('{item}'), "
    return query_filter[:-2]

def find_songs_by_same_artist(artists):
    conn = psycopg2.connect(
        database = os.environ.get("DB_DATABASE"),
        host = os.environ.get("DB_HOST"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        port = os.environ.get("DB_PORT")
    )
    cursor = conn.cursor()

    cursor.execute(f"select danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo from tracks inner join infos on tracks.track_id = infos.fk_track where lower(main_artist) in ({generate_filter(artists)})")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    same_artist_songs = []
    for item in data:
        item_infos = [float(item[0]), float(item[1]), float(item[2]), float(item[3]), float(item[4]), float(item[5]), float(item[6]), float(item[7]), float(item[8])]
        same_artist_songs.append(item_infos)

    return same_artist_songs

def find_similar_songs(playlist_url):
    sp = connect_to_spotify()

    playlist_ids = []
    playlist_songs = []
    playlist_analysis = []
    playlist_artists = []
    data = sp.playlist(playlist_url)

    name = data['name']
    cover = data['images'][0]['url']

    for item in data['tracks']['items']:
        try:
            item_id = item['track']['id']
            playlist_ids.append(item_id)
            ### check if exists that song in database. if so, add three times and pass

            item_name = item['track']['name']
            item_artists = []
            already_in_list = False
            for artist in item['track']['artists']:
                if artist['name'] in playlist_artists:
                    already_in_list = True
                else:
                    print(artist['name'], playlist_artists)
                    item_artists.append(artist['name'])
                    playlist_artists.append(artist['name'])
            playlist_songs.append(Track(item_name, item_artists, item_id))

            if already_in_list:
                continue

            print('Trying', item_name)
            same_artist_songs = find_songs_by_same_artist(item_artists)
            print('Found', len(same_artist_songs), 'songs')
            for song in same_artist_songs:
                playlist_analysis.append(song)
        except: 
            pass

    return Playlist(name, cover, playlist_analysis, tuple(playlist_ids), playlist_songs)


def add_info_to_database(infos):
    conn = psycopg2.connect(
        database = os.environ.get("DB_DATABASE"),
        host = os.environ.get("DB_HOST"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        port = os.environ.get("DB_PORT")
    )
    cursor = conn.cursor()

    
    for item in infos:
        try:
            print(f'Adicionou {item.name}')
            cursor.execute(f"INSERT INTO infos(fk_track, title, main_artist) values ('{item.id}', '{item.name}', '{item.artists}')", )
            conn.commit()
        except Exception as error:
            print(error)
            conn.rollback()
  
    cursor.close()
    conn.close()

if __name__ == '__main__':
    find_songs_by_same_artist(['Bring me the Horizon','Avenged Sevenfold'])
