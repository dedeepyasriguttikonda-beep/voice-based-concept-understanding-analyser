import streamlit as st
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from utils.speech_to_text import transcribe_audio
from utils.semantic_similarity import calculate_similarity
from utils.audio_features import extract_audio_features


def generate_pdf(transcript, similarity_score, final_score, features):
    os.makedirs("reports", exist_ok=True)

    pdf_path = "reports/report.pdf"

    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<font size=20><b>Voice Based Concept Understanding Report</b></font>",
            styles["Title"],
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Transcript</b>", styles["Heading2"]))
    elements.append(Paragraph(transcript, styles["BodyText"]))

    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Semantic Similarity Score</b>", styles["Heading2"]))
    elements.append(
        Paragraph(f"{similarity_score:.2f}", styles["BodyText"])
    )

    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Final Understanding Score</b>", styles["Heading2"]))
    elements.append(
        Paragraph(f"{final_score:.2f}%", styles["BodyText"])
    )

    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Audio Features</b>", styles["Heading2"]))

    if isinstance(features, dict):
        for key, value in features.items():
            elements.append(
                Paragraph(f"<b>{key}</b>: {value}", styles["BodyText"])
            )
    else:
        elements.append(
            Paragraph(str(features), styles["BodyText"])
        )

    doc.build(elements)

    return pdf_path

st.set_page_config(
    page_title="Voice Based Concept Understanding Analyser",
    page_icon="🎤",
    layout="wide",
)

st.title("🎤 Voice Based Concept Understanding Analyser")

uploaded_file = st.file_uploader(
    "Upload Audio File",
    type=["wav", "mp3", "m4a"],
)

reference_answer = st.text_area(
    "Enter Reference Answer "
)

if uploaded_file is not None:

    file_path = "temp_audio.wav"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.audio(uploaded_file)

    if st.button("Analyze Audio"):

        with st.spinner("Analyzing audio..."):

            # Speech-to-text
            transcript = transcribe_audio(file_path)

            # Semantic similarity
            if reference_answer.strip() != "":
                similarity_score = calculate_similarity(
                    reference_answer,
                    transcript,
                )
            else:
                similarity_score = 0

            # Audio features
            features = extract_audio_features(file_path)

            # Final score
            final_score = round(
                (similarity_score + 100) / 2,
                2,
            )

        st.subheader("📝 Transcript")
        st.write(transcript)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🧠 Semantic Similarity")
            st.metric(
                "Similarity Score",
                f"{similarity_score:.2f}",
            )

        with col2:
            st.subheader("🎧 Audio Features")
            st.write(features)

        st.subheader("🏆 Final Understanding Score")

        st.metric(
            "Overall Score",
            f"{final_score}%",
        )

        pdf_path = generate_pdf(
            transcript,
            similarity_score,
            final_score,
            features,
        )

        st.success("✅ PDF Report Generated Successfully!")

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_file,
                file_name="Voice_Report.pdf",
                mime="application/pdf",
            )