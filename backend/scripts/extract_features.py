import numpy as np
import librosa

NUM_MFCC = 13

def extract_audio_features(filepath):
    # Load audio file, returning time series array and respective sample rate
    y, sample_rate = librosa.load(filepath, sr=22050, mono=True)
    
    # Get estimated global tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sample_rate)
    
    # Get centroid frequencies
    spectral_centroid = np.mean(
        librosa.feature.spectral_centroid(y=y, sr=sample_rate)
    )
    
    zero_crossing_rate = np.mean(
        librosa.feature.zero_crossing_rate(y)
    )
    
    # Generate mel-frequency cepstrual coefficients
    mfcc = librosa.feature.mfcc(y=y, sr=sample_rate, n_mfcc=NUM_MFCC)
    
    features = {
        "tempo": float(tempo),
        "spectral_centroid": float(spectral_centroid),
        "zero_crossing_rate": float(zero_crossing_rate),
    }
    
    for i in range(NUM_MFCC):
        features[f"mfcc_{i+1}"] = float(np.mean(mfcc[i]))
    
    return features