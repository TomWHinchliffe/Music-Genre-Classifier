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

SUBGENRE_KEYWORDS = sorted(
    GENRE_MAP.keys(),
    key=lambda x: -len(x)
)

# Idea: Collect data based on genre search
# sp.search(q="genre:shoegaze", type="artist")  # Do this for all genres in subgenres list (after matching)
# artist["genres"]  # Then get the artist's genres
# sp.artist_top_tracks(artist_id)  # And top tracks
# sp.audio_features(track_ids)  # And audio features

# Idea: Collect data based on broad track search
# sp.search(q="a", type="track")  # Could repeat for all letter of alphabet, or dictionary of common words

def process_track(track, artist_genres):
    features = safe_call(sp.audio_features, [track["id"]])[0]
    
    if features is None:
        return None
    
    # debug print
    print(features["danceability"])
    
    subgenres, main_genres = process_genres(artist_genres)
    
    return {
        # Track and artist info
        "track_id": track["id"],
        "name": track["name"],
        "artist": track["artists"][0]["name"],

        # Track audio features
        "danceability": features["danceability"],
        "energy": features["energy"],
        "valence": features["valence"],
        "tempo": features["tempo"],
        "acousticness": features["acousticness"],
        "instrumentalness": features["instrumentalness"],
        "liveness": features["liveness"],
        "speechiness": features["speechiness"],

        # Labels
        "subgenres": subgenres,
        "main_genres": main_genres
    }

# Obtain respective subgenres and main genres from a list of Spotify genres
def process_genres(spotify_genres):
    subgenres = extract_subgenres(spotify_genres)
    main_genres = map_to_main(subgenres)
    
    if not main_genres:
        main_genres = ["other"]
    
    return subgenres, main_genres

# Multi-match scoring for subgenres
def extract_subgenres(spotify_genres):
    matches = []

    for g in spotify_genres:
        g = normalise_text(g)

        for key in SUBGENRE_KEYWORDS:
            if key in g:
                matches.append(key)

    return list(set(matches))

# Returns a list of main genres, mapped from subgenres 
def map_to_main(subgenres):
    return list(set(GENRE_MAP[s] for s in subgenres if s in GENRE_MAP))

# Helper function to enforce lowercase and remove extra space from genre text
def normalise_text(g):
    return g.lower().strip()

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

# Dataset collection loop and saving
def collect_training_data():
    data = []
    seen_tracks = set()

    TARGET_DATASET_SIZE = 10000

    # Collect artist genre data
    for subgenre in list(GENRE_MAP.keys()):
        print(f"Fetching genre seed: {subgenre}")
        
        # Fetch artist genre search results
        results = safe_call(
            sp.search,
            q=f"genre:{subgenre}",
            type="artist",
            limit=10
        )
        
        for artist in results["artists"]["items"]:
            artist_id = artist["id"]
            artist_genres = artist["genres"]
            
            if not artist_genres:
                continue
            
            top_tracks = safe_call(sp.artist_top_tracks, artist_id)["tracks"]
            
            for track in top_tracks:
                # Skip over seen tracks
                if track["id"] in seen_tracks:
                    continue
                
                # Process row data with track info, artist info, and audio features
                track_row = process_track(track, artist_genres)
                
                if track_row:
                    data.append(track_row)
                    seen_tracks.add(track["id"])
                
            time.sleep(0.2)
        
        # Stop collecting data when desired dataset size has been reached        
        if len(data) >= TARGET_DATASET_SIZE:
            break

    # Save dataset
    df = pd.DataFrame(data)

    # Remove empty rows
    df = df[df["main_genres"].map(len) > 0]

    # Save dataset to CSV file
    df.to_csv("data/training_dataset.csv", index=False)

    print(f"Collected {len(df)} tracks")

# Main function to collect and save the genre training dataset
if __name__ == "__main__":
    collect_training_data()
