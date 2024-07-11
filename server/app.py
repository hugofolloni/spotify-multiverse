
from flask import Flask, request
from main import find_songs
from local import find_fake
from database import get_database_size
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/analysis", methods=['GET'])
def get_songs():
    if request.args.get("key") != os.getenv("API_KEY"):
        return json.dumps({"error": "Invalid key", "code": 2})
    
    playlist = request.args.get('playlist')
    if not playlist or playlist.find('https://open.spotify.com/') == -1:
        return json.dumps({"error": "Playlist not found", "code": 3})
 
    amount = request.args.get('amount')
    if not amount:
        return json.dumps({"error": "Amount not found", "code": 3})
    amount = int(amount)

    try:
        data = [obj.__dict__ for obj in find_songs(playlist, amount)]
        return json.dumps({"code": 0, "tracks": data})
    except:
        return json.dumps({"error": "Couldn't process your request", "code": 1})

## To use when the Spotify API is unavailable.
@app.route("/fake", methods=['GET'])
def fake_songs():
    if request.args.get("key") != os.getenv("API_KEY"):
        return json.dumps({"error": "Invalid key", "code": 2})
    
    data = [obj.__dict__ for obj in find_fake(int(request.args.get('amount')), int(request.args.get('offset')), int(request.args.get('limit')))]
    return json.dumps({"code": 0, "tracks": data})

@app.route("/size", methods=['GET'])
def get_size():
    if request.args.get("key") != os.getenv("API_KEY"):
        return json.dumps({"error": "Invalid key", "code": 2})
    
    return {"size": get_database_size()}

