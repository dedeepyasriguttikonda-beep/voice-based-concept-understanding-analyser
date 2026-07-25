import re
import logging

from config import (
    FILLER_WORD_PATTERN,
    SIMILARITY_HIGH_THRESHOLD,
    SIMILARITY_MID_THRESHOLD,
    SIMILARITY_HIGH_POINTS,
    SIMILARITY_MID_POINTS,
    SIMILARITY_LOW_POINTS,
    FILLER_RATIO_THRESHOLD,
    FILLER_GOOD_POINTS,
    FILLER_POOR_POINTS,
    PAUSE_RATIO_THRESHOLD,
    PAUSE_GOOD_POINTS,
    PAUSE_POOR_POINTS,
    RMS_ENERGY_THRESHOLD,
    ENERGY_GOOD_POINTS,
    ENERGY_POOR_POINTS,
    STRONG_UNDERSTANDING_THRESHOLD,
    MODERATE_UNDERSTANDING_THRESHOLD,
    UNDERSTANDING_LEVELS,
)

logger = logging.getLogger(__name__)

def calculate_filler_word_stats(text):
    """
    Analyzes user transcript text to count filler words/phrases,
    and returns a stats dictionary.
    """
    if not text or not text.strip():
        return {
            "filler_word_count": 0,
            "total_words": 0,
            "filler_ratio": 0.0
        }

    # Clean punctuation for total word count calculation
    cleaned_text = re.sub(r'[^\w\s\']', '', text.lower())
    words = cleaned_text.split()
    total_words = len(words)

    # Common English filler words and short phrases
    fillers_found = re.findall(FILLER_WORD_PATTERN, text.lower())
    filler_word_count = len(fillers_found)

    if total_words > 0:
        filler_ratio = round(filler_word_count / total_words, 4)
    else:
        filler_ratio = 0.0

    return {
        "filler_word_count": filler_word_count,
        "total_words": total_words,
        "filler_ratio": filler_ratio
    }

def evaluate_understanding(similarity, filler_ratio, audio):
    """
    Computes a composite understanding score (0-100) by combining:
      - Semantic similarity (0-1 scale): up to 50 points
      - Filler word ratio: up to 20 points
      - Pause ratio: up to 15 points
      - RMS energy: up to 15 points

    Returns:
        tuple: (score, label, color_hex)
    """
    logger.info("Evaluating understanding — similarity=%.4f, filler_ratio=%.4f, audio=%s",
                similarity, filler_ratio, audio)
    score = 0
    score += (
        SIMILARITY_HIGH_POINTS if similarity > SIMILARITY_HIGH_THRESHOLD
        else SIMILARITY_MID_POINTS if similarity > SIMILARITY_MID_THRESHOLD
        else SIMILARITY_LOW_POINTS
    )
    score += FILLER_GOOD_POINTS if filler_ratio < FILLER_RATIO_THRESHOLD else FILLER_POOR_POINTS
    score += PAUSE_GOOD_POINTS if audio["pause_ratio"] < PAUSE_RATIO_THRESHOLD else PAUSE_POOR_POINTS
    score += ENERGY_GOOD_POINTS if audio["rms_energy"] > RMS_ENERGY_THRESHOLD else ENERGY_POOR_POINTS

    if score >= STRONG_UNDERSTANDING_THRESHOLD:
        label, color = UNDERSTANDING_LEVELS["strong"]
    elif score >= MODERATE_UNDERSTANDING_THRESHOLD:
        label, color = UNDERSTANDING_LEVELS["moderate"]
    else:
        label, color = UNDERSTANDING_LEVELS["poor"]

    logger.info("Result: score=%d, level=%s", score, label)
    return score, label, color
