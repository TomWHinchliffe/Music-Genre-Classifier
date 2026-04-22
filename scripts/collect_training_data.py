import os
import time
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
    )
)

from spotipy.exceptions import SpotifyException

# Helper function for safe API calls to handle rate limits
def safe_call(func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get("Retry-After", 1))
                print(f"Rate limited. Sleeping {retry_after}s...")
                time.sleep(retry_after)
            else:
                raise

genres = sp.recommendation_genre_seeds()
print(f"Available genres: {genres}")