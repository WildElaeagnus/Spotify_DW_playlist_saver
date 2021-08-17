# save discover weekly playlist
import requests
import SpotifyAPI
import configparser
import json

from urllib.parse import urlencode

import web_token

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

# get token from spotify website
t = web_token.WebToken()
w_token = t.get_token()

def url(pl_endpoint, pl_data):
    '''form a valid url from endpoint and data'''
    return f'{pl_endpoint}?{pl_data}'

# header for request
headers = {
    "Authorization": f"Bearer {token}"
}
# request to get DW playlist
pl_endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'
pl_data = urlencode({"limit": 50})
r = requests.get(url(pl_endpoint, pl_data), headers=headers)
# find DW playlist id in response
loaded_json = json.loads(r.text)
items = loaded_json['items']
for i in items:
	if i['name'] == 'Discover Weekly':
		DW_playlist_url = i['external_urls']
		DW_playlist_href = i['href']
        # TODO add a condition if DW playlist not found
DW_id = DW_playlist_href.split("/")[-1]
print(f'DW_id: {DW_id}')

# create dict with tracks ids and names from req
pl_endpoint = f'https://api.spotify.com/v1/playlists/{DW_id}/tracks'
pl_data = urlencode({"market": "Ru"})
r = requests.get(url(pl_endpoint, pl_data), headers=headers)
loaded_json = json.loads(r.text)
items = loaded_json['items']
tracks_dw = {}
# id is a key cuz names can be same
for i in range(loaded_json['total']):
    j = items[i]['track']
    tracks_dw[j['id']] = j['name']
print(tracks_dw)

# play first song from dict and see req code

# anyway 
# send req to play song
# send req what playing right now
# if response dont math then pass
# if math add key and val to new dict dw_likes
# after loaded_json['total'] cycles 
# create a req to make new playlist with dw_likes dict

# after all figure out how to scedule this thing
# TODO 
# u can find out if song was disliked if it not appears when
# this py script trying to play it on any devise
# (but what to do if none of devices is up???)
# and if first song of a DW playlist is disliked nothin happened
# need to check response code of that

# mb cycle fo 30 possible songs, then delet unlplayable

# TODO u need to decide how to schedle this skript each week
# mb it can be executed only when spotify is up on a device
