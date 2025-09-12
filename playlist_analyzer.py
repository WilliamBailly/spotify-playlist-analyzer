import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import matplotlib
import sys
from dotenv import load_dotenv
import os

load_dotenv()
client_id=os.getenv("SPOTIPY_CLIENT_ID")
client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")

#Authenticate API Key
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

def main():
    playlist = get_playlist()
    playlist_info = get_playlist_info(playlist)
    playlist_df = pd.DataFrame.from_dict(playlist_info, orient="index")
    print(playlist_df)



def get_playlist():
    #Retreive playlistID
    playlist_url = input("Enter your spotify playlist url: ")
    parts = playlist_url.split('/')
    playlist_id_with_params = parts[-1] 
    if '?' in playlist_id_with_params:
        playlist_id = playlist_id_with_params.split('?')[0]
    else:
        playlist_id = playlist_id_with_params
    
    #Retrieve playlist
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]

    #Get extra pages
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    
    return tracks

def get_playlist_info(playlist):
    track_dict = {}
    for item in playlist:
        track = item["track"]
        track_name = track["name"]
        try:
            release_date = track["album"]["release_date"]
            year_released = release_date.split("-")[0]
        except spotipy.SpotifyException:
            continue

        track_dict[track_name] = {
            "year_released": year_released,
            "popularity": track["popularity"],
            "duration_ms": track["duration_ms"]
        }

    return track_dict
        

if __name__ == "__main__":
    main()



