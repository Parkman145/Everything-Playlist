import json
import requests

import auth

token = auth.get_token()

# Setup Config
with open("config.json") as f:
    config = json.load(f) 

exclude_other_users = config["exclude"]["exclude_other_users"]
exclude_playlists = config["exclude"]["playlists"]
exclude_songs = config["exclude"]["songs"]

