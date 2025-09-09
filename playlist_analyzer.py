import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas
import matplotlib
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    print(client_id, client_secret)



if __name__ == "__main__":
    main()



