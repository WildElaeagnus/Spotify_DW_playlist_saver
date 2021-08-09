# save discover weekly playlist
import SpotifyAPI

client_id = 'f70377e4b42340178d8839ff58dc61b8'
client_secret = '25568d1f9110471190a2e4dfc723bd26'

spotify_login = SpotifyAPI.SpotifyAPI(client_id, client_secret)
print(spotify_login.perform_auth())
token = spotify_login.access_token
print(token)

