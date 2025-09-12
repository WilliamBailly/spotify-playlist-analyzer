# Spotify Playlist Analyzer
A python program that allows users to input a spotify URL and receive graphical information about the makeup of the playlists. This is done using the Spotify API to pull key information about each of the tracks in the playlist in a dictionary. The program then uses pandas to sort the data into a dataframe. Matplotlib is used to show key elements of the playlist such as a histogram of song durations and a heatmap of the popularity based on year released and song duration.

# Highlights
* Uses Spotify API, Spotipy, Pandas, Seaborn, and Matplotlib
* Provides graphical information in an easy to digest format

# How to use this program

This program requires a spotify API key and a number of libraries.
The Spotify API key can be retrieved by making a spotify developer account at https://developer.spotify.com/documentation/web-api


Once a key is made you will need to make a .env file in the same directory as the playlist_analyzer.py

The .env should contain the following code:

`SPOTIPY_CLIENT_ID="f951f120009f4413bec12f3611daaa97"   
SPOTIPY_CLIENT_SECRET="a479aa6053c24ce99fb4ae23162264f5"`

Install the required libraries using the following command:
`pip install -r requirements.txt`

Now running the program should prompt you for a URL, inputting any public playlist URL will auto-generate the information for you (Given you are in an IDE that supports plotting such as VSCode).
