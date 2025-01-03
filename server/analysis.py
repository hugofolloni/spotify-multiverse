import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances
import os
from dotenv import load_dotenv
load_dotenv()

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

def connect_to_spotify():
    client_id = os.environ.get("SPOTIFY_CLIENT")
    client_secret = os.environ.get("SPOTIFY_SECRET")

    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def get_playlist_info(playlist_url):
    sp = connect_to_spotify()

    playlist_ids = []
    playlist_songs = []
    playlist_analysis = []
    data = sp.playlist(playlist_url)

    name = data['name']
    cover = data['images'][0]['url']

    for item in data['tracks']['items']:
        try:
            item_id = item['track']['id']
            playlist_ids.append(item_id)
            item_name = item['track']['name']
            item_artists = []
            for artist in item['track']['artists']:
                item_artists.append(artist['name'])
            playlist_songs.append(Track(item_name, item_artists, item_id))
            item_features = sp.audio_features(item_id)[0]
            item_infos = [item_features['danceability'], item_features['energy'], item_features['loudness'] / -10, item_features['speechiness'], item_features['acousticness'], item_features['instrumentalness'], item_features['liveness'], item_features['valence'], item_features['tempo'] / 180]
            playlist_analysis.append(item_infos)
        except: 
            pass

    return Playlist(name, cover, playlist_analysis, tuple(playlist_ids), playlist_songs)

def apply_pca(infos):
    dataframe = np.array(infos).T
    scaler = StandardScaler()
    scaled = scaler.fit_transform(dataframe)
    _PCA = PCA(n_components=1)
    pca = _PCA.fit_transform(scaled)
    reduced = _PCA.inverse_transform(pca)
    unscaled = scaler.inverse_transform(reduced)
    centroid = unscaled.T.mean(axis=0)
    return centroid

def find_similarity(user, database, amount: int):
    comparitions = []
    
    for track in database:
        track_vector = np.array(track.attributes)
        comparitions.append(Similarity(track.id, euclidean_distances([user], [track_vector])[0][0]))

    comparitions.sort(key=lambda x: x.distance, reverse=False)

    return comparitions[:amount]

def find_infos_about_songs(ids):
    sp = connect_to_spotify()

    if len(ids) > 50:
        return sp.tracks(ids[:50])['tracks'] + sp.tracks(ids[50:])['tracks']
    
    if len(ids) > 100:
        return sp.tracks(ids[:50])['tracks'] + sp.tracks(ids[50:100])['tracks']

    return sp.tracks(ids)['tracks']