from utils.semantic_similarity import get_similarity

reference = "Photosynthesis is the process by which plants make food using sunlight."
student = "Plants use sunlight to prepare food through photosynthesis."

score = get_similarity(reference, student)

print("Similarity Score:", score)
