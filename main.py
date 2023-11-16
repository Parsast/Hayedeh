import requests
import json
import pandas as pd
import csv
import schedule
import time

def get_spotify_token(client_id, client_secret):
    # Get the access token from Spotify
    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }
    )
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

def get_markets(access_token):
    response = requests.get('https://api.spotify.com/v1/markets',
    headers = {
        'Authorization':f'Bearer {access_token}'
        }
    )
    data = response.json()
    return data["markets"]
def get_top_tracks_Allcountries(artist_Spotify_Id, access_token):
    markets = get_markets(access_token)
    top_tracks = dict()
    for market in markets:
        response = requests.get(f'https://api.spotify.com/v1/artists/5b1CDxqOGnXr5M1DUn2XQh/top-tracks?market={market}',
        headers = {
         'Authorization':f'Bearer {access_token}'
        }
        )

        top_tracks[market] = response.json()

    return top_tracks
    

token = get_spotify_token("c7d8869f7af34cbf8087e1c2e446b38a",
"dc8c26ca8e1b490bb24dceb701916751")
Hayedeh = "5b1CDxqOGnXr5M1DUn2XQh"
top_tracks = get_top_tracks_Allcountries(Hayedeh, token)
# with open('data.json', "w") as j:
#     json.dump(top_tracks, j)

# with open('data.json','r') as r:
#     top_tracks_json = json.load(r)

# data = pd.read_json(top_tracks)
# flattened_data = pd.json_normalize(data)
# with open('data.json', "w") as j:
#     json.dump(top_tracks, j)
with open('hayedeh.csv','w', newline='') as file:
    fieldnames = top_tracks[next(iter(top_tracks))].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for key in top_tracks:
        writer.writerow(top_tracks[key])
# flattened_data.to_csv('flattened_data.csv', index=False)
