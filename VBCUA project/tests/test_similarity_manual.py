import os
import sys

# Ensure project root is on path (script now lives in tests/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic_eval import get_similarity

reference = "Photosynthesis is the process by which plants make food using sunlight."
student = "Plants use sunlight to prepare food through photosynthesis."

score = get_similarity(reference, student)

print("Similarity Score:", score)
