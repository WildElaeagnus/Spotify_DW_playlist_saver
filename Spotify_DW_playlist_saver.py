# save discover weekly playlist
import requests
import SpotifyAPI
import configparser
import json
from time import sleep
import datetime
from selenium.common.exceptions import ElementClickInterceptedException

from urllib.parse import urlencode

import web_token

# read file with auth info if it not exist then create it
try:    
    with open("auth_info.txt", "r+") as f:
        print(f.readlines())
        config = configparser.ConfigParser()
        config.read("auth_info.txt")
        # if we have only client id secret and user id we can only save whole DW playlist and cant see witch song were disliked
        client_id = str(config.get("Spotify_auth_info", "client_id"))
        client_secret = str(config.get("Spotify_auth_info", "client_secret"))
        # userid(manual)
        user_id = str(config.get("Spotify_auth_info", "user_id"))
        # token(manual)
except FileNotFoundError:
    with open("auth_info.txt", "w+") as f:
        f.write('[Spotify_auth_info]\nclient_id: \nclient_secret: \nuser_id: \n')

# wrap in try: except: in case we using no webdriver to obtain powerful token
# print(f'id: {client_id}\nsecret: {client_secret}')
# spotify_login = SpotifyAPI.SpotifyAPI(client_id, client_secret)
# print(spotify_login.perform_auth())
# token = spotify_login.access_token
# print(token)

# get token from spotify website
t = web_token.WebToken(
    browser_profile_path=r'C:\Users\Akorz\AppData\Roaming\Mozilla\Firefox\Profiles\rwe75su1.auto',
    webdriver_exec_path=r'C:\Users\Akorz\Desktop\Python_code\SPOTIFY_pl\webdrivers\geckodriver.exe',
    firefox_binary_path=r"C:\Program Files\Mozilla Firefox\firefox.exe",
    web_browser='firefox'
)
try:
    w_token = t.get_token()
except ElementClickInterceptedException:
    t.close()
    w_token = t.get_token()

def url(pl_endpoint, pl_data):
    '''form a valid url from endpoint and data'''
    return f'{pl_endpoint}?{pl_data}'

# header for request
headers = {
    "Authorization": f"Bearer {w_token}"
}
# request to get DW playlist
pl_endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'
pl_data = urlencode({"limit": 50})
r = requests.get(url(pl_endpoint, pl_data), headers=headers)
print(r)
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
# pl_endpoint = f'https://api.spotify.com/v1/playlists/{DW_id}/tracks'
# pl_data = urlencode({"market": "Ru"})
# r = requests.get(url(pl_endpoint, pl_data), headers=headers)
# loaded_json = json.loads(r.text)
# items = loaded_json['items']
# tracks_dw = {}
# # id is a key cuz names can be same
# for i in range(loaded_json['total']):
#     j = items[i]['track']
#     tracks_dw[j['id']] = j['name']

#region
# fav_device_name = "DESKTOP-BRRGN4B" TODO append to config file of sth
def get_aval_device(*args, **kwargs):
    '''get list of avaliable devices'''
    fav_device_name = kwargs.pop('fav_device_name', None)
    device_id = None
    endpoint = 'https://api.spotify.com/v1/me/player/devices'
    data = None
    r = requests.get(url(endpoint, data), headers=headers)
    print(r)
    loaded_json = json.loads(r.text)
    devices = loaded_json['devices']
    # print(devices[0]['name'])
    for i in devices:
        if(i['name'] == fav_device_name): device_id = i['id']
        elif(i['is_active'] == True): device_id = i['id']
    if( device_id == None): device_id = devices[0]['id']
    return device_id
# play detached song
def play_detached_song():
    endpoint = 	f'https://api.spotify.com/v1/me/player/play'
    playlist_id = '65fjS0iiSX4PhClIzO5aGb'
    id_data = urlencode({"device_id": f"{device_id}"})
    data = {
        "context_uri": f"spotify:playlist:{playlist_id}",
        "offset": {
        "position": 0
        },
        "position_ms": 0
    }
    return requests.put(url(endpoint, id_data), json.dumps(data), headers=headers)
# toggle off shuffle 
def toggle_off_shuffle():
    endpoint = 	f'https://api.spotify.com/v1/me/player/shuffle'
    data = urlencode({"state": "false"})
    return requests.put(url(endpoint, data), headers=headers)

# pause song
def pause_song():
    endpoint = 	f'https://api.spotify.com/v1/me/player/pause'
    data = None
    return requests.put(url(endpoint, data), headers=headers)

def play_song(position , playlist_id):
    endpoint = 	f'https://api.spotify.com/v1/me/player/play'
    # data = '{\"context_uri\":\"spotify:playlist:37i9dQZEVXcWlsrx2rT0bU\",\"offset\":{\"position\":0},\"position_ms\":0}'
    data = {
        "context_uri": f"spotify:playlist:{playlist_id}",
        "offset": {
        "position": position
        },
        "position_ms": 0
    }
    return requests.put(endpoint, json.dumps(data), headers=headers)

# req to get currently plaing song
def get_playback_state():
    endpoint = 	f'https://api.spotify.com/v1/me/player'
    # data = urlencode({"market": "Ru"})
    data = None
    r = requests.get(url(endpoint, data), headers=headers)
    # print(r)
    # 204 no content
    # parse json with currently playing song
    loaded_json__ = json.loads(r.text)
    items = loaded_json__['item']
    type(loaded_json)
    shuffle = loaded_json__['shuffle_state']
    is_playing = loaded_json__['is_playing']
    try:
        track_id = items['id']
        track_name = items['name']
    except TypeError:
        track_id = None
        track_name = None
    return track_id, track_name, shuffle, is_playing

# endregion

# init of algoritm
device_id = get_aval_device()
play_detached_song()
toggle_off_shuffle()
pause_song()

# body of algoritm

# get liked songs id
DW_likes = []
for i in range(30):
    play_song(i, DW_id)
    sleep(1)
    # if is_playing == true add to list
    track_id, track_name, shuffle, is_playing = get_playback_state()
    if is_playing == True: DW_likes.append(track_id) 
# stop playback
pause_song()

# if len(DW_id) == 30: raise print('nothing is disliked')

# some prep for playlist creating
d = datetime.datetime.today()
# get year, mm, dd
time_dmy = f'{d.day}-{d.month}-{d.year}'
# get full time
time_ymdhms = f'{d.day}-{d.month}-{d.year} {d.hour}:{d.minute:02}:{d.second:02}'
# get week number
week = datetime.date(d.year, d.month, d.day).strftime("%V")

DW_likes_name = f'{d.year}_{week}'
DW_likes_description = f'Creation date: {time_ymdhms}. This playlist was created by robot. Link to github repo /akorzunin/Spotify_DW_playlist_saver'

# create плейлист
DW_is_public = True
def create_DW_playlist():
    endpoint = 	f'https://api.spotify.com/v1/users/{user_id}/playlists'
    id_data = urlencode({"user_id": f"{user_id}"})
    data = {
    "name": DW_likes_name,
    "description": DW_likes_description,
    "public": str(DW_is_public).lower()
    }

    return requests.post(url(endpoint, id_data), json.dumps(data), headers=headers)

resp = create_DW_playlist()
# get new playlist id
loaded_json = json.loads(r.text)
# loaded_json['items'][-1]
new_DW_id = dict(resp.headers)['location'].split('/')[-1]

# add songs from list to new playlist
def fill_DW_playlist():
    endpoint = 	f'	https://api.spotify.com/v1/playlists/{new_DW_id}/tracks'
    # id_data = urlencode({"playlist_id ": f"{new_DW_id}"})
    id_data = None
    data = {"uris": [f'spotify:track:{i}' for i in DW_likes]}

    return requests.post(url(endpoint, id_data), json.dumps(data), headers=headers)
fill_DW_playlist()



# TODO u need to decide how to schedle this skript each week
# (but what to do if none of devices is up???)

