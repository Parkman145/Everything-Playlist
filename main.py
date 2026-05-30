import requests
import json
from pprint import pprint

url = "https://api.spotify.com/v1/me/playlists"


with open("tokens.json") as f:
    token = json.load(f)["token"]

headers = {
    "User-Agent": "Python",
    "Authorization": f"Bearer {token}"
}

response = requests.request("GET", url, headers=headers)

playlists = json.loads(response.text)
print(type(playlists))