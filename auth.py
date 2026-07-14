import json
import webbrowser
import urllib.parse
import socket
import requests
import hashlib
import secrets
import base64
import time


def get_token():
    min_remaining_time = 60*5  # 5 Min

    try:
        with open("token.json") as f:
            token_json = json.load(f)
        time_remaining = token_json["expire_time"] - time.time()
    except FileNotFoundError:
        time_remaining = 0

    if (time_remaining < min_remaining_time):
        token_response = request_token()
        token = token_response["access_token"]
        expire_time = time.time() + token_response["expires_in"]

        # Maybe not the best idea to store tokens in plaintext, but it doesn't have that many scopes, and it expires in an hour so I don't care
        data = {"token": token, "expire_time": expire_time}
        with open("token.json", "w") as f:
            json.dump(data, f)
    else:
        token = token_json["token"]

    return token


def generate_code():
    code = secrets.token_urlsafe(64)
    hasher = hashlib.sha256()
    hasher.update(code.encode("utf-8"))
    code_hash = hasher.digest()
    code_challenge = base64.urlsafe_b64encode(
        code_hash).decode("utf-8").replace("=", "")

    return (code, code_challenge)


def request_token():
    with open("config.json") as f:
        config = json.load(f)

    s = socket.create_server(('127.0.0.1', 3000))

    client_id = urllib.parse.quote(config["client_id"])
    redirect_uri = urllib.parse.quote(config["redirect_uri"])
    scope = urllib.parse.quote(
        "user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private")

    code_verifier, code_challenge = generate_code()

    auth_url = (
        "https://accounts.spotify.com/authorize?"
        f"client_id={client_id}"
        "&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        "&code_challenge_method=S256"
        f"&code_challenge={code_challenge}"
    )

    webbrowser.open_new_tab(auth_url)
    conn, addr = s.accept()
    message = conn.recv(1024)

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        "\r\n"
        "<h1>Auth Successful.</h1>"
    )
    conn.sendall(response.encode("utf-8"))

    conn.close()

    path = message.decode().split("\r\n")[0].split(" ")[1]

    query = urllib.parse.urlsplit(path).query
    code = urllib.parse.parse_qs(query)["code"][0]

    spotify_token_url = "https://accounts.spotify.com/api/token"

    payload = (
        "grant_type=authorization_code"
        f"&redirect_uri={redirect_uri}"
        "&client_id=49c2202ae61a478f8b337ffc521843d9"
        f"&code={code}"
        f"&code_verifier={code_verifier}"
    )
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "python ig????"
    }

    response = requests.request(
        "POST", spotify_token_url, data=payload, headers=headers)

    return json.loads(response.text)


if __name__ == "__main__":
    print(get_token())
