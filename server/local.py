from database import retrieve_songs
from analysis import find_infos_about_songs, find_similarity, apply_pca, get_playlist_info

import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
import time

def add_songs_by_playlist(playlist):
    conn = psycopg2.connect(
        database = os.environ.get("DB_DATABASE"),
        host = os.environ.get("DB_HOST"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        port = os.environ.get("DB_PORT")
    )
    cursor = conn.cursor()

    data = get_playlist_info(playlist)
    analysis = data.analysis
    songs = data.songs
    print("Foram obtidas as informações da playlist.")

    for index, item in enumerate(analysis):
        try:
            cursor.execute("INSERT INTO tracks(track_id, danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (songs[index].id, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]))
            conn.commit()
            print("Adicionado", songs[index].name)
        except Exception as error:
            print("Já exisitia", songs[index].name)
            conn.rollback()
  
    cursor.close()
    conn.close()

    return print("Itens adicionados com sucesso.")

def iterate_list(playlists):
    for playlist in playlists:
        print(playlist)
        add_songs_by_playlist(playlist)
        print()
        time.sleep(40)

def fake_user(filters = "", quantity = ""):
    data = retrieve_songs(filters, quantity, fake=True)
    analysis = []
    ids = []

    for item in data:
        attr = []
        for index in range(2, 11):
            attr.append(float(item[index]))
        analysis.append(attr)
        ids.append(item[1])

    return analysis, tuple(ids)

def find_fake(amount, offset, limit):
    user_infos, user_ids = fake_user(quantity=f"OFFSET {offset} LIMIT {limit}")
    database_infos = retrieve_songs(filters=f"WHERE track_id NOT IN {user_ids}")
    user_vector = apply_pca(user_infos)

    return find_similarity(user_vector, database_infos, amount)

def print_fake_playlist(ids):
    print("We are using this fake playlist:")
    infos = find_infos_about_songs(ids)
    for song in infos['tracks']:
        item_name = song['name']
        item_artists = []
        for artist in song['artists']:
            item_artists.append(artist['name'])
        print(item_name, '-', item_artists)
    print()

def print_data(recommendations):
    ids = []
    for item in recommendations:
        ids.append(item.track_id)

    infos = find_infos_about_songs(ids)

    for index, song in enumerate(infos):
        item_name = song['name']
        item_artists = []
        for artist in song['artists']:
            item_artists.append(artist['name'])
        item_id = recommendations[index].track_id
        distance = recommendations[index].distance
        print(f'{item_name} - {", ".join(item_artists)} : https://open.spotify.com/track/{item_id} - {distance}')

def faking(offset, limit):
    recommendations = find_fake(15, offset, limit)
    print_data(recommendations)

if __name__ == '__main__':
    print_data(find_fake(20, 10, 20))