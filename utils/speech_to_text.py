import whisper
import streamlit as st

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

def transcribe_audio(audio_path):
    try:
        result = model.transcribe(audio_path)

        text = result.get("text", "").strip()

        if not text:
            return "⚠️ No speech detected in audio."

        return text

    except Exception as e:
        return f"❌ Error: {str(e)}"
    st.write("DEBUG TRANSCRIPT:", transcript)
