import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import seaborn as sns
import sys

#Declare API Key
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
    plot_playlist(playlist_df)

def get_playlist():
    #Retreive playlistID
    try:
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
            
    except Exception:
        print("Please provide a valid URL")
        sys.exit()
    return tracks

def get_playlist_info(playlist):
    #Retreive track info
    track_dict = {}
    for item in playlist:
        track = item["track"]
        track_name = track["name"]
        try:
            release_date = track["album"]["release_date"]
            year_released = release_date.split("-")[0]
        except spotipy.SpotifyException:
            continue
        #Add track to dictionary
        track_dict[track_name] = {
            "year_released": year_released,
            "popularity": track["popularity"],
            "duration_ms": track["duration_ms"]
        }

    return track_dict
        
def plot_playlist(playlist_df):
    fig, axs = plt.subplots(2, 2, figsize=(10,8))

    #Top Left Plot
    axs[0,0].hist(playlist_df["duration_ms"] / 1000, bins="auto", edgecolor="black", color="yellow")
    axs[0,0].set_title("Distribution of Song Durations")
    axs[0,0].set_xlabel("Duration (seconds)")
    axs[0,0].set_ylabel("Count")

    #Top Right Plot
    axs[0,1].hist(playlist_df["popularity"], bins="auto", edgecolor="black", color="orange")
    axs[0,1].set_title("Distribution of Song Popularity")
    axs[0,1].set_xlabel("Popularity (0-100)")
    axs[0,1].set_ylabel("Count")

    #Bottom Left Plot
    axs[1,0].scatter(x=playlist_df["duration_ms"]/1000, y=playlist_df["popularity"])
    axs[1,0].set_title("Song Popularity vs Duration")
    axs[1,0].set_xlabel("Duration (seconds)")
    axs[1,0].set_ylabel("Popularity")

    #Bottom Right Plot (Seaborns heatmap)
    #Declare bins and labels
    bins = [0,3,4,5,6,10]
    labels = ["<3", "3-4", "4-5", "5-6", "6+"]
    playlist_df["duration_min"] = playlist_df["duration_ms"] / 60000
    playlist_df["duration_bin"] = pd.cut(playlist_df["duration_min"], bins=bins, labels=labels)
    heatmap_data = playlist_df.pivot_table(
    values="popularity",
    index="duration_bin",
    columns="year_released",
    aggfunc="mean"
    )
    #Plot heatmap on figure
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", ax=axs[1,1])
    axs[1,1].set_title("Popularity Heatmap by Duration and Year")
    axs[1,1].set_xlabel("Year Released")
    axs[1,1].set_ylabel("Duration (minutes)")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()



