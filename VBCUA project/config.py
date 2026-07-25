"""
VBCUA - Central Configuration
=============================
All model names, file paths, and scoring thresholds live here so they aren't
scattered/duplicated across modules. Mirrors the config.py pattern used in
the EduGenie project structure.
"""

import os

# ─── Model Names ───────────────────────────────────────────────────────────
WHISPER_MODEL_NAME = "base"
SBERT_MODEL_NAME = "all-MiniLM-L6-v2"

# ─── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SAMPLE_AUDIO_PATH = os.path.join(AUDIO_DIR, "sample.mp3")
TEMP_UPLOAD_PATH = os.path.join(BASE_DIR, "temp_audio.wav")
WAVEFORM_IMAGE_NAME = "waveform.png"
PDF_REPORT_NAME = "report.pdf"

# ─── Upload Validation ──────────────────────────────────────────────────────
MAX_UPLOAD_SIZE_MB = 200
ALLOWED_AUDIO_TYPES = ["wav", "mp3"]

# ─── Filler Word Detection ──────────────────────────────────────────────────
FILLER_WORD_PATTERN = r"\b(uh|um|ah|like|so|basically|actually|literally|you know)\b"

# ─── Scoring Weights & Thresholds ───────────────────────────────────────────
# Similarity (0-1 scale) -> points (max 50)
SIMILARITY_HIGH_THRESHOLD = 0.7
SIMILARITY_MID_THRESHOLD = 0.4
SIMILARITY_HIGH_POINTS = 50
SIMILARITY_MID_POINTS = 30
SIMILARITY_LOW_POINTS = 10

# Filler ratio -> points (max 20)
FILLER_RATIO_THRESHOLD = 0.05
FILLER_GOOD_POINTS = 20
FILLER_POOR_POINTS = 10

# Pause ratio -> points (max 15)
PAUSE_RATIO_THRESHOLD = 0.25
PAUSE_GOOD_POINTS = 15
PAUSE_POOR_POINTS = 5

# RMS energy -> points (max 15)
RMS_ENERGY_THRESHOLD = 0.01
ENERGY_GOOD_POINTS = 15
ENERGY_POOR_POINTS = 5

# Final score -> understanding level classification
STRONG_UNDERSTANDING_THRESHOLD = 80
MODERATE_UNDERSTANDING_THRESHOLD = 50

UNDERSTANDING_LEVELS = {
    "strong": ("Strong Understanding", "#2ecc71"),
    "moderate": ("Moderate Understanding", "#f39c12"),
    "poor": ("Poor Understanding", "#e74c3c"),
}

# ─── Waveform Plot Styling ──────────────────────────────────────────────────
WAVEFORM_COLOR = "#4a9eff"
WAVEFORM_LABEL_COLOR = "#555555"
WAVEFORM_GRID_COLOR = "#cccccc"

# ─── Audio Feature Extraction ────────────────────────────────────────────────
SILENCE_TOP_DB = 30
