# 🎤 Voice-Based Concept Understanding Analyser

An AI-powered web application that evaluates how effectively users understand and explain conceptual topics through spoken communication. The platform combines **speech-to-text transcription**, **semantic similarity analysis**, **audio feature extraction**, and an **intelligent multi-factor scoring engine** to deliver a comprehensive understanding assessment.

---

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
cd voice-based-concept-understanding-analyser

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
3. Click **"New app"** → select the repository → set `app.py` as the main file.
4. Add a `packages.txt` file in the repo root with:
   ```
   ffmpeg
   ```
5. Deploy. Streamlit Cloud will install dependencies from `requirements.txt` automatically.

> **Note:** Large models (Whisper, Sentence-BERT) will be downloaded on first run and cached by `@st.cache_resource`.

---

## Project Structure

```
voice-based-concept-understanding-analyser/
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── audio/
│   └── sample.mp3           # Sample audio for testing
├── reports/
│   ├── report.pdf            # Generated PDF report
│   └── waveform.png          # Generated waveform image
├── utils/
│   ├── __init__.py
│   ├── audio_utils.py        # Audio loading, feature extraction, waveform
│   ├── report_generator.py   # PDF report generation (ReportLab)
│   ├── scoring_engine.py     # Filler word analysis + multi-factor scoring
│   ├── semantic_eval.py      # Sentence-BERT similarity computation
│   └── speech_to_text.py     # Whisper transcription + normalization
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
└── README.md
```

---

## Requirements

See [requirements.txt](requirements.txt) for the full list. Key dependencies:

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
