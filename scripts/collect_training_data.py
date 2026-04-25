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

MAIN_GENRES = [
    "rock",
    "pop",
    "electronic",
    "hip-hop",
    "jazz",
    "blues",
    "country",
    "metal",
    "folk",
    "classical",
    "r&b/soul",
    "reggae",
    "latin",
    "world",
    "ambient",
    "soundtrack",
    "children",
    "comedy",
    "other"
]

GENRE_MAP = {
    # ROCK / ALTERNATIVE
    "alternative rock": "rock",
    "indie rock": "rock",
    "shoegaze": "rock",
    "grunge": "rock",
    "punk": "rock",
    "hardcore punk": "rock",
    "post-punk": "rock",
    "new wave": "rock",
    "progressive rock": "rock",
    "psychedelic rock": "rock",
    "art rock": "rock",
    "garage rock": "rock",
    "surf rock": "rock",
    "noise rock": "rock",

    # POP
    "pop": "pop",
    "indie pop": "pop",
    "dream pop": "pop",
    "synthpop": "pop",
    "electropop": "pop",
    "dance pop": "pop",
    "teen pop": "pop",
    "chamber pop": "pop",
    "art pop": "pop",
    "k-pop": "pop",
    "j-pop": "pop",

    # ELECTRONIC
    "house": "electronic",
    "deep house": "electronic",
    "tech house": "electronic",
    "techno": "electronic",
    "minimal techno": "electronic",
    "trance": "electronic",
    "progressive trance": "electronic",
    "dubstep": "electronic",
    "drum and bass": "electronic",
    "jungle": "electronic",
    "garage": "electronic",
    "uk garage": "electronic",
    "grime": "electronic",
    "breakbeat": "electronic",
    "idm": "electronic",
    "glitch": "electronic",
    "electro": "electronic",
    "downtempo": "electronic",
    "trip hop": "electronic",

    # HIP-HOP
    "hip hop": "hip-hop",
    "rap": "hip-hop",
    "trap": "hip-hop",
    "boom bap": "hip-hop",
    "lo-fi hip hop": "hip-hop",
    "jazz rap": "hip-hop",
    "gangsta rap": "hip-hop",
    "conscious hip hop": "hip-hop",

    # JAZZ
    "bebop": "jazz",
    "swing": "jazz",
    "cool jazz": "jazz",
    "smooth jazz": "jazz",
    "free jazz": "jazz",
    "fusion": "jazz",
    "latin jazz": "jazz",

    # BLUES
    "delta blues": "blues",
    "chicago blues": "blues",
    "electric blues": "blues",
    "blues rock": "blues",

    # COUNTRY
    "country": "country",
    "alt-country": "country",
    "country rock": "country",
    "bluegrass": "country",
    "americana": "country",

    # METAL
    "heavy metal": "metal",
    "death metal": "metal",
    "black metal": "metal",
    "metalcore": "metal",
    "doom metal": "metal",
    "progressive metal": "metal",
    "nu metal": "metal",

    # FOLK
    "folk": "folk",
    "indie folk": "folk",
    "folk rock": "folk",
    "traditional folk": "folk",

    # CLASSICAL
    "baroque": "classical",
    "romantic": "classical",
    "modern classical": "classical",
    "opera": "classical",
    "symphony": "classical",

    # R&B / SOUL
    "r&b": "r&b/soul",
    "soul": "r&b/soul",
    "funk": "r&b/soul",
    "neo soul": "r&b/soul",
    "motown": "r&b/soul",

    # REGGAE
    "reggae": "reggae",
    "dub": "reggae",
    "dancehall": "reggae",
    "ska": "reggae",

    # LATIN
    "reggaeton": "latin",
    "salsa": "latin",
    "bachata": "latin",
    "latin pop": "latin",
    "bossa nova": "latin",

    # WORLD
    "afrobeat": "world",
    "highlife": "world",
    "bhangra": "world",
    "flamenco": "world",

    # AMBIENT
    "ambient": "ambient",
    "dark ambient": "ambient",
    "drone": "ambient",
    "soundscape": "ambient",

    # SOUNDTRACK / OTHER
    "film score": "soundtrack",
    "video game music": "soundtrack",

    # CHILDREN / COMEDY
    "lullabies": "children",
    "sing-along": "children",
    "comedy": "comedy",
    "parody": "comedy"
}

SUBGENRE_KEYWORDS = list(GENRE_MAP.keys())

# Collect data based on genre search
sp.search(q="genre:shoegaze", type="artist")  # Do this for all genres in subgenres list
artist["genres"]  # Then get the artist's genres
sp.artist_top_tracks(artist_id)  # And top tracks
sp.audio_features(track_ids)  # And audio features

# Collect data based on broad track search
sp.search(q="a", type="track")  # Could repeat for all letter of alphabet, or dictionary of common words

# Helper function to enforce lowercase and remove extra space from genre text
def normalise_text(g):
    return g.lower().strip()

# Multi-match scoring for genres
def extract_subgenres(spotify_genres):
    matches = []

    for g in spotify_genres:
        g = normalise_text(g)

        for key in SUBGENRE_KEYWORDS:
            if key in g:
                matches.append(key)

    return list(set(matches))
