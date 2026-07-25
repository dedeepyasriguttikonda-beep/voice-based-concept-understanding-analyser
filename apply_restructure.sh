#!/usr/bin/env bash
# Run this from the ROOT of your local clone of
# voice-based-concept-understanding-analyser.
# It reproduces the restructure with git history preserved (git mv).
set -e

# 1. Move legacy (unused) modules/ folder aside
mkdir -p legacy
git mv modules legacy/modules
touch legacy/__init__.py
git add legacy/__init__.py

# 2. Flatten utils/ to project root
git mv utils/speech_to_text.py speech_to_text.py
git mv utils/semantic_eval.py semantic_eval.py
git mv utils/audio_utils.py audio_utils.py
git mv utils/scoring_engine.py scoring_engine.py
git mv utils/report_generator.py report_generator.py
git rm utils/__init__.py
rmdir utils 2>/dev/null || true

# 3. Move stray root test scripts into tests/
git mv test.py tests/test_transcription_manual.py
git mv test_audio.py tests/test_audio_features_manual.py
git mv test_similarity.py tests/test_similarity_manual.py

# 4. Drop the tracked runtime artifact (already in .gitignore going forward)
git rm --cached temp_audio.wav 2>/dev/null || true
rm -f temp_audio.wav

echo "Structural moves complete."
echo "Now copy over the following NEW/EDITED files from the delivered zip:"
echo "  - config.py                (new)"
echo "  - app.py                   (edited imports + config usage)"
echo "  - speech_to_text.py        (edited: imports WHISPER_MODEL_NAME)"
echo "  - semantic_eval.py         (edited: imports SBERT_MODEL_NAME)"
echo "  - scoring_engine.py        (edited: imports scoring constants)"
echo "  - audio_utils.py           (edited: imports path/waveform constants)"
echo "  - report_generator.py      (edited: imports REPORTS_DIR/PDF_REPORT_NAME)"
echo "  - tests/test_epic2.py      (edited: imports now point to legacy.modules)"
echo "  - tests/test_transcription_manual.py   (edited: import path fixed)"
echo "  - tests/test_audio_features_manual.py  (edited: import path fixed)"
echo "  - tests/test_similarity_manual.py      (edited: import path fixed)"
echo "  - README.md                (edited: Project Structure section)"
echo ""
echo "Then: git add -A && git commit -m 'Restructure: flatten utils/, move modules/ to legacy/, add config.py'"

# ---------------------------------------------------------------------------
# PHASE 2: nest everything into "VBCUA project/", matching the reference
# repo's root layout (Documentation/ + project folder + Video Demo/ + README
# + one requirements file).
# ---------------------------------------------------------------------------
mkdir -p "VBCUA project"
git mv app.py "VBCUA project/app.py"
git mv config.py "VBCUA project/config.py"
git mv speech_to_text.py "VBCUA project/speech_to_text.py"
git mv semantic_eval.py "VBCUA project/semantic_eval.py"
git mv audio_utils.py "VBCUA project/audio_utils.py"
git mv scoring_engine.py "VBCUA project/scoring_engine.py"
git mv report_generator.py "VBCUA project/report_generator.py"
git mv requirements.txt "VBCUA project/requirements.txt"
git mv packages.txt "VBCUA project/packages.txt"
git mv "er diagram.png" "VBCUA project/er diagram.png"
git mv audio "VBCUA project/audio"
git mv reports "VBCUA project/reports"
git mv legacy "VBCUA project/legacy"
git mv tests "VBCUA project/tests"
git mv .streamlit "VBCUA project/.streamlit"

mkdir -p "Video Demo"
# Video Demo/README.md and requirements_extracted.txt: copy these two files
# in from the delivered zip (they're new, not moves).

echo ""
echo "IMPORTANT — files that reference paths and need manual updates:"
echo "  - .devcontainer/devcontainer.json  (postAttachCommand / updateContentCommand"
echo "    need 'cd \"VBCUA project\"' prepended — see zip for the edited version)"
echo "  - README.md  (run instructions + Streamlit Cloud 'Main file path' should be"
echo "    'VBCUA project/app.py', not 'app.py')"
echo "  - Streamlit Cloud app settings (if already deployed): update the main file"
echo "    path in the dashboard to 'VBCUA project/app.py' or the deploy will break."
echo ""
echo "Then: git add -A && git commit -m 'Nest app into VBCUA project/, add Video Demo/, match reference root layout'"
