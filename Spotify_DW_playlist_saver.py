# save discover weekly playlist
import requests
import SpotifyAPI
import configparser
from urllib.parse import urlencode

# read file with auth info if it not exist then create it
try:    
    with open("auth_info.txt", "r+") as f:
        print(f.readlines())
        config = configparser.ConfigParser()
        config.read("auth_info.txt")
        client_id = str(config.get("Spotify_auth_info", "client_id"))
        client_secret = str(config.get("Spotify_auth_info", "client_secret"))
        user_id = str(config.get("Spotify_auth_info", "user_id"))
except FileNotFoundError:
    with open("auth_info.txt", "w+") as f:
        f.write('[Spotify_auth_info]\nclient_id: \nclient_secret: \nuser_id: \n')

print(f'id: {client_id}\nsecret: {client_secret}')
spotify_login = SpotifyAPI.SpotifyAPI(client_id, client_secret)
print(spotify_login.perform_auth())
token = spotify_login.access_token
print(token)

# how to use token
# user_id = 'wizzler'
pl_endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'
sh_endpoint = f'https://api.spotify.com/v1/search'
header = {
    "Authorization": f"Bearer {token}"
}
data = urlencode({"q": "time", "type": "track"})
pl_data = urlencode({"limit": 5})
q_url = f'{pl_endpoint}?{pl_data}'
r = requests.get(q_url, headers=header)
print(r.json())
# TODO 
# GET	/v1/playlists/{playlist_id}/tracks	Get a Playlist's Items
# implement code from notebook
# parse out DW playlist id
# mb detect user id automatically
# 
# u can find out if song was disliked if it not appears when
# this py script trying to play it on any devise
# (but what to do if none of devices is up???)
# and if first song of a DW playlist is disliked nothin happened
# need to check response code of that

# mb cycle fo 30 possible songs, then delet unlplayable

# TODO u need to decide how to schedle this skript each week
# mb it can be executed only when spotify is up on a device
