# 🎤 Voice-Based Concept Understanding Analyser

An AI-powered web application that evaluates how effectively users understand and explain conceptual topics through spoken communication. The platform combines **speech-to-text transcription**, **semantic similarity analysis**, **audio feature extraction**, and an **intelligent multi-factor scoring engine** to deliver a comprehensive understanding assessment.

## 🚀 Live Demo

- 🎥 **Demo Video:** https://drive.google.com/file/d/1P0eMJKoa6WT9HWGJKanaKMGO4tmNKhZH/view?usp=drivesdk
[![Demo Video](https://img.shields.io/badge/Demo-Video-blue?logo=google-drive)](https://drive.google.com/file/d/1P0eMJKoa6WT9HWGJKanaKMGO4tmNKhZH/view?usp=drivesdk)

> watch the demo video to see the complete workflow and features in action.


## Features

- **Speech-to-Text** — OpenAI Whisper (base model) converts audio to text with automatic format normalization (16 kHz mono WAV).
- **Semantic Similarity** — Sentence-BERT (`all-MiniLM-L6-v2`) computes cosine similarity between the student's explanation and a reference concept.
- **Audio Feature Extraction** — Librosa extracts duration, RMS energy, spectral centroid, zero-crossing rate, and pause ratio.
- **Filler Word Detection** — Regex-based detection of common fillers (uh, um, like, basically, etc.) with ratio computation.
- **Multi-Factor Scoring Engine** — Combines similarity (50 pts), filler discipline (20 pts), pause ratio (15 pts), and RMS energy (15 pts) into a 100-point composite score.
- **Qualitative Classification** — Strong (≥80), Moderate (≥50), or Poor (<50) understanding level with color-coded display.
- **PDF Report Generation** — Downloadable report with reference concept, transcription, waveform visualization, and metric tables.
- **Performance Instrumentation** — Built-in timing for every pipeline stage with an expandable performance panel.

---

## Architecture

```
Audio File (.wav/.mp3)
       │
       ▼
┌─────────────────┐     ┌───────────────────────┐
│  Speech-to-Text │     │   Reference Concept    │
│  (Whisper base)  │     │   (User-provided text) │
└────────┬────────┘     └───────────┬───────────┘
         │                          │
         ▼                          ▼
   Transcript Text ──────► Semantic Similarity
         │                  (Sentence-BERT)
         │                          │
         ▼                          ▼
  Filler Word Analysis     Similarity Score (0–1)
         │                          │
         ▼                          │
  Audio Feature Extraction ◄────────┘
  (RMS, Pause Ratio, etc.)         │
         │                          │
         ▼                          ▼
   ┌────────────────────────────────────┐
   │     Multi-Factor Scoring Engine    │
   │   Similarity + Filler + Audio     │
   │        → Score / 100              │
   │   Strong | Moderate | Poor        │
   └───────────────┬────────────────────┘
                   │
                   ▼
         UI Display + PDF Report
```

---

## Prerequisites

- **Python** 3.9 or higher
- **FFmpeg** — Required by OpenAI Whisper for audio processing
  - **Windows**: `winget install Gyan.FFmpeg` (auto-detected by the app)
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg`

---

## Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/voice-based-concept-understanding-analyser.git
cd voice-based-concept-understanding-analyser/"VBCUA project"

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Streamlit Cloud Deployment

1. Push the repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **"New app"** → select the repository → set `VBCUA project/app.py` as the main file path.
4. Ensure `VBCUA project/packages.txt` exists with:
   ```
   ffmpeg
   ```
5. Deploy. Streamlit Cloud will install dependencies from `VBCUA project/requirements.txt` automatically.

> **Note:** Since the app now lives inside `VBCUA project/`, make sure the Streamlit Cloud app settings point the "Main file path" there — otherwise it won't find `requirements.txt`/`packages.txt`.

> **Note:** Large models (Whisper, Sentence-BERT) will be downloaded on first run and cached by `@st.cache_resource`.

---

## Project Structure

```
voice-based-concept-understanding-analyser/
├── Documentation/               # SmartBridge internship phase docs (1-8)
├── VBCUA project/               # All application code and assets
│   ├── audio/
│   │   └── sample.mp3            # Sample audio for testing
│   ├── reports/
│   │   ├── report.pdf             # Generated PDF report
│   │   └── waveform.png           # Generated waveform image
│   ├── legacy/
│   │   └── modules/               # Earlier (unused) module implementations, kept for reference
│   ├── tests/
│   │   ├── test_epic2.py           # Unit tests (exercises legacy/modules/)
│   │   ├── test_transcription_manual.py
│   │   ├── test_audio_features_manual.py
│   │   └── test_similarity_manual.py
│   ├── .streamlit/
│   │   └── config.toml            # Streamlit configuration
│   ├── app.py                     # Main Streamlit application
│   ├── config.py                  # Central config: model names, paths, scoring weights
│   ├── speech_to_text.py          # Whisper transcription + normalization
│   ├── semantic_eval.py           # Sentence-BERT similarity computation
│   ├── audio_utils.py             # Audio loading, feature extraction, waveform
│   ├── scoring_engine.py          # Filler word analysis + multi-factor scoring
│   ├── report_generator.py        # PDF report generation (ReportLab)
│   ├── requirements.txt           # Python dependencies
│   ├── packages.txt               # System packages for Streamlit Cloud (ffmpeg)
│   └── er diagram.png
├── Video Demo/
│   └── README.md                 # Links to the demo video and live app
├── README.md
└── requirements_extracted.txt    # Copy of dependencies for quick reference
```

---

## Requirements

See [requirements.txt](VBCUA%20project/requirements.txt) for the full list. Key dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.39.0 | Web UI framework |
| openai-whisper | 20240930 | Speech-to-text transcription |
| sentence-transformers | 3.0.1 | Semantic similarity embeddings |
| librosa | 0.10.2 | Audio feature extraction |
| reportlab | 4.2.2 | PDF report generation |
| soundfile | 0.12.1 | Audio I/O |
| matplotlib | 3.9.2 | Waveform visualization |

---

## License

This project is for academic and educational purposes.
