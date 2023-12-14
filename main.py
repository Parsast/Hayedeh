import argparse
import requests
import json
import pandas as pd
import csv
import schedule
import time

def request_spotify_access_token(client_id, client_secret):
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
        # print(type(response.json()))
        tracks = response.json()["tracks"]
        
        for track in tracks:
            if track["id"] in top_tracks.keys():
                top_tracks[track["id"]][market] = 1
            else:
                top_tracks[track["id"]] = dict()
                top_tracks[track["id"]][market] = 1
                for key in track.keys():
                    if isinstance(track[key] ,str) or isinstance(track[key] ,int):
                        top_tracks[track["id"]][key] = track[key]

    return top_tracks

def get_audio_analysis(trackId,access_token):
    response = requests.get(f'https://api.spotify.com/v1/audio-analysis/{trackId}',
    headers = {
         'Authorization':f'Bearer {access_token}'
        }
    )
    response = response.json()
    return response

def get_audio_features_track(trackId,access_token):
    response = requests.get(f'https://api.spotify.com/v1/audio-features/{trackId}',
    headers = {
        'Authorization':f'Bearer {access_token}'
    }
    )
    response = response.json()
    # response = json.load(response)
    return response

def get_artist_albums(artistId, access_token):
    response = requests.get(f'https://api.spotify.com/v1/artists/{artistId}/albums',
    headers = {
        'Authorization':f'Bearer {access_token}'
    }
    )

    response = response.json()
    albums = dict()
    for album in response["items"]:
        albums[album["name"]] = album["uri"].split(":")[-1]
    return albums

def get_album_tracks(albumId, access_token):

    response = requests.get(f'https://api.spotify.com/v1/albums/{albumId}/tracks',
    headers = {
        'Authorization':f'Bearer {access_token}'
    }
    )
    response = response.json()
    tracks = dict()
    for track in response["items"]:
        tracks[track["name"]] = track["uri"].split(":")[-1]
    return tracks


def make_csv_all_tracks_artist(artistId, access_token):
    
    albums = get_artist_albums(artistId, access_token)

    tracks = dict()

    for album in albums.keys():
        album_tracks = get_album_tracks(albums[album], access_token)
        for track in album_tracks.keys():
            features = get_audio_features_track(album_tracks[track], access_token)
            tracks[track] = dict()
            for feature in features:
                tracks[track][feature] = features[feature]
    df = pd.DataFrame.from_dict(tracks, orient='index')
    df.to_csv("output.csv")
    print("output saved!")



parser = argparse.ArgumentParser(description="Generate the CSV file of all the tracks of a Spotify Artist")
parser.add_argument("client_id", help = "Spotify API client ID")
parser.add_argument("client_secret", help = "Spotify API client secret")
parser.add_argument("artist_id", help = "artist Spotify Id")
args = parser.parse_args()
print(str(args.artist_id))
access_token = request_spotify_access_token(args.client_id,args.client_secret)
make_csv_all_tracks_artist(args.artist_id, access_token)
    
# client_id = ''
# client_secret = ''


# trackId = ""
# artistId = ''
# albumId =  ""

