import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

auth_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
)

sp = spotipy.Spotify(auth_manager=auth_manager)

# Test that Spotipy setup works
results = sp.search(q='Radiohead', type='track', limit=1)
print(results)