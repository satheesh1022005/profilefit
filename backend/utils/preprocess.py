import re
import string

def clean_text(text):
    """
    Cleans input text by:
    - Lowercasing
    - Removing numbers
    - Removing punctuation
    - Stripping extra spaces
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = text.strip()
    return text
