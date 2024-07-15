
from flask import Flask, request
from flask_cors import CORS, cross_origin
from main import find_songs
from local import find_fake
from database import get_database_size, find_song
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/analysis", methods=['GET'])
@cross_origin()
def get_songs():
    if request.args.get("key") != os.environ.get("API_KEY"):
        return json.dumps({"error": "Invalid key", "code": 2})
    
    playlist = request.args.get('playlist')
    if not playlist or playlist.find('https://open.spotify.com/') == -1:
        return json.dumps({"error": "Playlist not found", "code": 3})
 
    amount = request.args.get('amount')
    if not amount:
        return json.dumps({"error": "Amount not found", "code": 3})
    amount = int(amount)

    try:
        infos, data = find_songs(playlist, amount)
        return json.dumps({"code": 0, "infos": {"name": infos.name, "cover": infos.cover}, "tracks": [obj.__dict__ for obj in data]})
    except Exception as error:
        if str(error).find("at least") != -1:
            return json.dumps({"error": "The server is down due high number of requests", "code": 1})
        return json.dumps({"error": "Couldn't process your request", "code": 1, "exception": str(error)})

## To use when the Spotify API is unavailable.
@app.route("/fake", methods=['GET'])
@cross_origin()
def fake_songs():
    if request.args.get("key") != os.environ.get("API_KEY"):
        return json.dumps({"error": "Invalid key", "code": 2})
    
    data = [obj.__dict__ for obj in find_fake(int(request.args.get('amount')), int(request.args.get('offset')), int(request.args.get('limit')))]
    return json.dumps({"code": 0,  "infos": {"name": "Is it really you?", 'cover': 'https://i.pinimg.com/564x/53/4f/a4/534fa4d80a6efe5ced3d03690d39c40b.jpg'}, "tracks": data})

@app.route("/size", methods=['GET'])
def get_size():
    if request.args.get("key") != os.environ.get("API_KEY"):
        return json.dumps({"error": "Invalid key", "code": 2})
    
    return {"size": get_database_size()}

@app.route("/find", methods=['GET'])
def find():
    if request.args.get("key") != os.environ.get("API_KEY"):
        return json.dumps({"error": "Invalid key", "code": 2})
    
    track_id = request.args.get("track") 
    return json.dumps(find_song(track_id), default=lambda o: o.__dict__,  indent=4)

if __name__ == '__main__':
    app.run(debug=True)