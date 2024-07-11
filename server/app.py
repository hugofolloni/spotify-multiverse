
from flask import Flask, request
from main import find_songs
from local import find_fake
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/analysis", methods=['GET'])
def get_songs():
    if request.args.get("key") == os.getenv("API_KEY"):
        playlist = request.args.get('playlist')
        amount = request.args.get('amount')
        if amount:
            amount = int(amount)
        return json.dumps([obj.__dict__ for obj in find_songs(playlist, amount)])
    return "Chave inválida"

## To use when the API is unavailable.
@app.route("/fake", methods=['GET'])
def fake_songs():
    if request.args.get("key") == os.getenv("API_KEY"):
        return json.dumps([obj.__dict__ for obj in find_fake(int(request.args.get('amount')), int(request.args.get('offset')), int(request.args.get('limit')))])
    return "Chave inválida"

