import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocess import preprocess_text

# Load corpus
with open('data/sample_corpus.txt', 'r', encoding='utf-8') as f:
    corpus = f.readlines()

# Preprocess corpus
preprocessed_corpus = [preprocess_text(line) for line in corpus]

# Initialize vectorizer
vectorizer = TfidfVectorizer()

# Fit vectorizer on preprocessed corpus
vectorizer.fit(preprocessed_corpus)

# Save vectorizer as pickle
with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("✅ Vectorizer trained and saved successfully!")
