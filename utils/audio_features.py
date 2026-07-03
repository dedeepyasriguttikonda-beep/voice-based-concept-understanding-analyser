import librosa
import numpy as np

def extract_audio_features(audio_path):
    """
    Extracts basic audio features.
    """

    # Load audio
    y, sr = librosa.load(audio_path)

    # Duration
    duration = librosa.get_duration(y=y, sr=sr)

    # Root Mean Square Energy
    rms = librosa.feature.rms(y=y)
    energy = float(np.mean(rms))

    # Pitch using Spectral Centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    pitch = float(np.mean(spectral_centroid))

    return {
        "Duration (seconds)": round(duration, 2),
        "Average Energy": round(energy, 4),
        "Average Pitch": round(pitch, 2)
    }