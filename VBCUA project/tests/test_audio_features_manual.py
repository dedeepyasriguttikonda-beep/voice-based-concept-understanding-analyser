import os
import sys

# Ensure project root is on path (script now lives in tests/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audio_utils import extract_audio_features

audio_path = "audio/sample.mp3"

features = extract_audio_features(audio_path)

print("Audio Features")
print("----------------")

for key, value in features.items():
    print(f"{key}: {value}")