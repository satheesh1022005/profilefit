import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Dummy training data
data = ["Python developer", "Machine learning engineer", "React developer"]

# Fit vectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(data)

# Save it
with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("✅ Vectorizer saved successfully!")
