from fastapi import APIRouter, Query
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
import time
import os
from dotenv import load_dotenv  # For loading .env file containing spotify credentials

load_dotenv()

router = APIRouter()

auth_manager = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
)

sp = spotipy.Spotify(auth_manager=auth_manager)

# Search song route
@router.get("/search")
def search_song(query: str = Query(..., description="The name of the song to search")):
    try:
        results = sp.search(q=query, type="track", limit=10)

    except SpotifyException as e:
        if e.http_status == 429:
            retry_after = int(e.headers.get("Retry-After", 1))
            print(f"Rate limited. Retrying after {retry_after}s...")
            time.sleep(retry_after)
            results = sp.search(q=query, type="track", limit=5)
        else:
            raise e
    
    tracks = []
    for item in results["tracks"]["items"]:
        track_info = {
            "name": item["name"],
            "artist": item["artists"][0]["name"] if item.get("artists") else None,
            "album": item["album"]["name"] if item.get("album") else None,
            "image": (
                item["album"]["images"][0]["url"]
                if item["album"] and item["album"].get("images")
                else None
            ),
            "spotify_url": item.get("external_urls", {}).get("spotify"),
            "release_year": item["album"]["release_date"][:4] if item.get("album") else None,
        }
        tracks.append(track_info)
    
    return {"tracks": tracks}
    