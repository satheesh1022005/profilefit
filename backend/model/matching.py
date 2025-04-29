from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import clean_text

# Initialize vectorizer (can be made global / pickle later)
vectorizer = TfidfVectorizer()

def predict_match(resume_text, opportunity_text):
    # Clean the texts
    resume_cleaned = clean_text(resume_text)
    opportunity_cleaned = clean_text(opportunity_text)

    # Combine both for fitting vectorizer
    combined_texts = [resume_cleaned, opportunity_cleaned]
    tfidf_matrix = vectorizer.fit_transform(combined_texts)

    # Compute cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return round(similarity[0][0] * 100, 2)  # Convert to percentage
