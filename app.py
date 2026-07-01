"""
Voice-Based Concept Understanding Analyser — Main Streamlit App
================================================================
Entry point that wires Epic 2 modules into an interactive UI.

Run with:
    streamlit run app.py
"""

import os
import tempfile

import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Voice-Based Concept Analyser",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Epic 2 module imports ─────────────────────────────────────────────────────
from modules.speech_to_text import speech_to_text, save_waveform, validate_transcription
from modules.semantic_engine import semantic_similarity, get_available_concepts
from modules.audio_features import (
    extract_audio_features,
    filler_word_ratio,
    evaluate_understanding,
    get_feedback,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    concept = st.selectbox(
        "Select Concept Topic",
        options=get_available_concepts(),
        index=0,
    )
    custom_ref = st.text_area(
        "Custom Reference (optional)",
        placeholder="Paste your own reference definition here...",
        height=120,
    )
    whisper_model = st.selectbox(
        "Whisper Model Size",
        options=["tiny", "base", "small"],
        index=1,
        help="Larger models are more accurate but slower.",
    )
    st.markdown("---")
    st.caption("Voice-Based Concept Understanding Analyser v1.0")

# ── Main header ───────────────────────────────────────────────────────────────
st.title("🎙️ Voice-Based Concept Understanding Analyser")
st.markdown(
    "Upload an audio explanation of a concept. The system will **transcribe**, "
    "**evaluate semantic understanding**, and **analyse speech fluency** to "
    "generate a comprehensive score."
)
st.divider()

# ── File upload ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload your audio explanation (WAV recommended)",
    type=["wav", "mp3", "m4a", "ogg", "flac"],
    help="Record yourself explaining the selected concept, then upload here.",
)

if uploaded_file is None:
    st.info("👆 Upload an audio file to begin analysis.")
    st.stop()

# Save uploaded bytes to a temp file so modules can read it by path
with tempfile.NamedTemporaryFile(
    suffix=os.path.splitext(uploaded_file.name)[-1], delete=False
) as tmp:
    tmp.write(uploaded_file.read())
    audio_path = tmp.name

st.audio(uploaded_file, format="audio/wav")

# ── Run analysis ──────────────────────────────────────────────────────────────
if st.button("🔍 Analyze Concept Understanding", type="primary"):

    with st.spinner("🎧 Processing and evaluating..."):

        # ── Task 1: Speech-to-Text ────────────────────────────────────────────
        with st.status("📝 Transcribing audio...", expanded=False):
            transcript = speech_to_text(audio_path, model_size=whisper_model)
            validation = validate_transcription(transcript)
            waveform_img = save_waveform(audio_path)

        # ── Task 3 (part A): Audio Feature Extraction ─────────────────────────
        with st.status("🔊 Extracting audio features...", expanded=False):
            audio_features = extract_audio_features(audio_path)
            filler_data    = filler_word_ratio(transcript)

        # ── Task 2: Semantic Similarity ────────────────────────────────────────
        with st.status("🧠 Computing semantic similarity...", expanded=False):
            sim_result = semantic_similarity(
                transcript,
                concept,
                custom_reference=custom_ref.strip() if custom_ref.strip() else None,
            )

        # ── Task 3 (part B): Final Scoring ────────────────────────────────────
        score, level, color = evaluate_understanding(
            sim_result["normalized_score"], filler_data, audio_features
        )
        feedback = get_feedback(
            sim_result["normalized_score"], filler_data, audio_features, level
        )

    # ── Results display ───────────────────────────────────────────────────────
    st.success("✅ Analysis complete!")
    st.divider()

    # Row 1: Score cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Final Score", f"{score * 100:.1f} / 100")
    with col2:
        st.metric("🧠 Semantic Similarity", f"{sim_result['percentage']}%")
    with col3:
        st.metric("🗣️ Filler Word Rate", f"{filler_data['filler_percentage']}%")

    st.markdown(
        f"<h3 style='color:{color}; text-align:center;'>🏷️ {level}</h3>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Row 2: Transcript + Waveform
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("📄 Transcription")
        if validation["quality_flag"] == "empty":
            st.warning("No speech detected. Please check your audio.")
        else:
            st.text_area(
                label="Transcribed text",
                value=transcript,
                height=200,
                disabled=True,
                label_visibility="collapsed",
            )
            st.caption(
                f"Word count: **{validation['word_count']}** | "
                f"Quality: **{validation['quality_flag'].capitalize()}**"
            )

    with col_right:
        st.subheader("🌊 Waveform")
        if os.path.exists(waveform_img):
            st.image(waveform_img, use_column_width=True)

    st.divider()

    # Row 3: Audio metrics
    st.subheader("🔊 Audio Features")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Duration", f"{audio_features['duration_sec']} s")
    m2.metric("Pause Ratio", f"{audio_features['pause_ratio'] * 100:.1f}%")
    m3.metric("Speaking Ratio", f"{audio_features['speaking_ratio'] * 100:.1f}%")
    m4.metric("RMS Energy", f"{audio_features['rms_energy']:.5f}")

    # Row 4: Filler words
    if filler_data["detected_fillers"]:
        st.subheader("💬 Detected Filler Words")
        filler_cols = st.columns(min(len(filler_data["detected_fillers"]), 5))
        for i, (word, count) in enumerate(filler_data["detected_fillers"][:5]):
            filler_cols[i].metric(f'"{word}"', f"{count}×")

    st.divider()

    # Row 5: Feedback
    st.subheader("📋 Feedback")
    for item in feedback:
        st.markdown(f"- {item}")

    # Cleanup temp file
    try:
        os.remove(audio_path)
    except OSError:
        pass