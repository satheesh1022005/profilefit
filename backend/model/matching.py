import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import preprocess_text

# Load vectorizer once when this file is imported
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'vectorizer.pkl')

with open(VECTORIZER_PATH, 'rb') as f:
    vectorizer = pickle.load(f)


def predict_match(resume_text, opportunity_text):
    """
    Preprocesses the resume and opportunity text,
    transforms them using the vectorizer, and computes cosine similarity.
    """
    resume_clean = preprocess_text(resume_text)
    opportunity_clean = preprocess_text(opportunity_text)

    resume_vector = vectorizer.transform([resume_clean])
    opportunity_vector = vectorizer.transform([opportunity_clean])

    similarity = cosine_similarity(resume_vector, opportunity_vector)[0][0]

    # Scale similarity to percentage
    match_percentage = round(float(similarity) * 100, 2)

    return match_percentage
