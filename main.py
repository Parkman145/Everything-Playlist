import json
import webbrowser
import urllib.parse
import socket
import requests
import hashlib
import secrets
import base64


def generate_code():
    code = secrets.token_urlsafe(64)
    hasher = hashlib.sha256()
    # hasher.update(code.encode("utf-8"))
    hasher.update(code.encode("utf-8"))
    code_hash = hasher.digest()
    code_challenge = base64.urlsafe_b64encode(code_hash).decode("utf-8").replace("=", "")
    
    return (code, code_challenge)
# Auth
with open("config.json") as f:
    config = json.load(f)


s = socket.create_server(('127.0.0.1', 3000))


client_id = urllib.parse.quote(config["client_id"])
redirect_uri = urllib.parse.quote(config["redirect_uri"])
scope = urllib.parse.quote("user-read-private user-read-email playlist-read-private")

auth_url = (
    "https://accounts.spotify.com/authorize?"
    f"client_id={client_id}"
    "&response_type=code"
    f"&redirect_uri={redirect_uri}"
    f"&scope={scope}"
)
webbrowser.open_new_tab(auth_url)
conn, addr  = s.accept()
message = conn.recv(1024)

response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "\r\n"
    "<h1>Auth Successful.</h1>" 
)
conn.sendall(response.encode("utf-8"))

path = message.decode().split("\r\n")[0].split(" ")[1]

query = urllib.parse.urlsplit(path).query
code = urllib.parse.parse_qs(query)["code"][0]




spotify_token_url = "https://accounts.spotify.com/api/token"

payload = (
    "grant_type=authorization_code"
    "&redirect_uri=https%3A%2F%2F127.0.0.1%3A3000%2Fcallback"""
    f"&client_id=49c2202ae61a478f8b337ffc521843d9&code={code}"
    )
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "python ig????"
}

response = requests.request("POST", spotify_token_url, data=payload, headers=headers)

print(response.text)