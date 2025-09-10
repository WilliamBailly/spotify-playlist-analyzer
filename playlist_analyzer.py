import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas
import matplotlib
import sys

#Authenticate API Key
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

def main():
    playlist = get_playlist()
    for item in playlist:
        track = item["track"]
        print(track['name'])

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

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    
    return tracks



if __name__ == "__main__":
    main()



