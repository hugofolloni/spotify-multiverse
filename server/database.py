import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

class TrackInfo:
    def __init__(self, id, attributes):
        self.id = id
        self.attributes = attributes
    
class DatabaseModel:
    def __init__ (self, args):
        self.id = int(args[0])
        self.track_id = args[1]
        self.danceability = float(args[2])
        self.energy = float(args[3])
        self.loudness = float(args[4])
        self.speechiness = float(args[5])
        self.acousticness = float(args[6])
        self.instrumentalness = float(args[7])
        self.liveness = float(args[8])
        self.valence = float(args[9])
        self.tempo = float(args[10])

def add_songs(infos, songs):
    conn = psycopg2.connect(
        database = os.environ.get("DB_DATABASE"),
        host = os.environ.get("DB_HOST"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        port = os.environ.get("DB_PORT")
    )
    cursor = conn.cursor()
    
    for index, item in enumerate(infos):
        try:
            cursor.execute("INSERT INTO tracks(track_id, danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (songs[index].id, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]))
            conn.commit()
        except Exception as error:
            conn.rollback()
  
    cursor.close()
    conn.close()

def retrieve_songs(filters = "", quantity = "", fake=False):
    conn = psycopg2.connect(
        database = os.environ.get("DB_DATABASE"),
        host = os.environ.get("DB_HOST"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        port = os.environ.get("DB_PORT")
    )
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM tracks {filters} {quantity}")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    if fake:
       return data 
    
    return preprocess_data(data)

def get_database_size():
    conn = psycopg2.connect(
        database = os.environ.get("DB_DATABASE"),
        host = os.environ.get("DB_HOST"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        port = os.environ.get("DB_PORT")
    )
    cursor = conn.cursor()

    cursor.execute(f"SELECT count(*) FROM tracks")
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return data[0]

def preprocess_data(data):
    output = []

    for item in data:
        attr = []
        for index in range(2, 11):
            attr.append(float(item[index]))
        output.append(TrackInfo(item[1], attr))

    return output

def find_song(track_id):
    conn = psycopg2.connect(
        database = os.environ.get("DB_DATABASE"),
        host = os.environ.get("DB_HOST"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        port = os.environ.get("DB_PORT")
    )
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM tracks where track_id = '{track_id}'")
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    try:
        model = DatabaseModel(data)
        return model
    except:
        return {"error": "Not Found"}
    
def get_database_ids(filters = "", quantity = ""):
    conn = psycopg2.connect(
        database = os.environ.get("DB_DATABASE"),
        host = os.environ.get("DB_HOST"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        port = os.environ.get("DB_PORT")
    )
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM tracks {filters} {quantity}")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data 
    