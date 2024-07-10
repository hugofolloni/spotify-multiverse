import psycopg2
from analysis import get_playlist_info
import os
from dotenv import load_dotenv
load_dotenv()

class TrackInfo:
    def __init__(self, id, attributes):
        self.id = id
        self.attributes = attributes

def add_songs(playlist):
    conn = psycopg2.connect(
        database = os.getenv("DB_DATABASE"),
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        port = os.getenv("DB_PORT")
    )
    cursor = conn.cursor()

    songs, infos = get_playlist_info(playlist)
    print("Foram obtidas as informações da playlist.")

    for index, item in enumerate(infos):
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

def retrieve_songs(filters = "", quantity = ""):
    conn = psycopg2.connect(
        database = os.getenv("DB_DATABASE"),
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        port = os.getenv("DB_PORT")
    )
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM tracks {filters} {quantity}")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return preprocess_data(data)

def preprocess_data(data):
    output = []

    for item in data:
        attr = []
        for index in range(2, 11):
            attr.append(float(item[index]))
        output.append(TrackInfo(item[1], attr))

    return output

def fake_user(data):
    infos = []
    ids = []

    for item in data:
        attr = []
        for index in range(2, 11):
            attr.append(float(item[index]))
        infos.append(attr)
        ids.append(item[1])

    return infos, tuple(ids)


