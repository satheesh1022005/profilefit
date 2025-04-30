import re
import os
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# Load English stopwords once
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    # Lowercase
    text = text.lower()

    # Remove punctuation & special characters
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize
    tokens = text.split()

    # Remove stopwords and apply stemming
    processed_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]

    # Re-join tokens
    processed_text = ' '.join(processed_tokens)

    return processed_text

def extract_resume_data(resume):
    """
    Enhanced function to accurately extract key information from a resume.
    Improves pattern matching and handles edge cases better.
    """
    # Normalize the text - convert to lowercase for better matching
    resume_lower = resume.lower()

    # Define patterns for different resume sections

    # Skills pattern - comprehensive list of technical skills
    skills_pattern = r"\b(?:python|java|javascript|typescript|html|css|c\+\+|c#|ruby|go|swift|kotlin|php|rust|scala|perl|r|sql|mysql|postgresql|mongodb|oracle|nosql|react|reactjs|vue\.?js|angular|node\.js|express\.js|django|flask|spring|laravel|asp\.net|jquery|bootstrap|tailwind|sass|less|graphql|rest|soap|xml|json|aws|azure|gcp|docker|kubernetes|jenkins|git|github|gitlab|bitbucket|ci/cd|devops|agile|scrum|tdd|machine learning|deep learning|ai|nlp|tensorflow|pytorch|keras|scikit-learn|pandas|numpy|data science|big data|hadoop|spark|kafka|tableau|power bi|excel|vba|linux|unix|windows|macos|networking|security|blockchain|cloud computing)\b"

    # Extract all skills (before doing case-insensitive operations)
    skills_matches = re.findall(skills_pattern, resume_lower)

    # Certifications pattern - improved to capture actual certifications
    # First, look for explicit certification mentions
    cert_explicit_pattern = r"(?:certification(?:s)?|certified|certificate)(?:\sin|\:|\s-\s|\s|\sof\s)\s*([\w\s\-\.\,\&\/\(\)]+?)(?:\.|\,|;|\n|\(|\)|$)"

    # Second pattern to find certifications listed after keywords
    cert_list_pattern = r"(?:certifications?|achievements|qualifications|credentials)(?:\:|\s\:|\s-\s|\s*\n)((?:.*\n?)*?)(?:\n\n|\n[A-Z]|\Z)"

    # Education pattern - improved to capture degrees and institutions
    education_pattern = {
        'degrees': r"\b(?:bachelor(?:'s)?|master(?:'s)?|phd|doctorate|b\.?(?:tech|s|a|e|sc|arch|b\.a|com)|m\.?(?:tech|s|a|e|sc|arch|b\.a|com)|associate(?:'s)?)\b(?:\sin|\sof|\s)?\s*([\w\s\-\.\,\&\/\(\)]+?)(?:\.|\,|;|\n|\(|\)|$)",
        'institutions': r"\b(?:university|college|institute|school)\s(?:of\s)?([\w\s\-\.\,\&\/\(\)]+?)(?:\.|\,|;|\n|\(|\)|$)",
        'graduation': r"(?:graduated|graduate|completed|earned)\s(?:from|with|in)\s*([\w\s\-\.\,\&\/\(\)]+?)(?:\.|\,|;|\n|\(|\)|$)"
    }

    # Experience pattern - improved to capture job titles, companies, and durations
    experience_pattern = {
        'job_titles': r"(?:^|\n|\.\s)(?:(?:senior|junior|lead|principal|staff|chief|head|associate)\s)?([\w\s\-\.\,\&\/\(\)]+?(?:developer|engineer|analyst|specialist|manager|director|coordinator|administrator|designer|architect|consultant|intern))(?:\sat|\sfor|\s-|\s@|\s\(|\.|\,|;|\n)",
        'companies': r"(?:at|for|with)\s(?:the\s)?([\w\s\-\.\,\&\/\(\)]+?)(?:\.|\,|;|\n|\(|\)|$)",
        'duration': r"(?:\()?((?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s\-\.\,\/]*\d{4})\s*(?:-|to|–|—)\s*((?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s\-\.\,\/]*\d{4}|Present|Current|Now)(?:\))?"
    }

    # GPA or Marks pattern - improved to handle different formats
    gpa_pattern = r"\b(?:gpa|cgpa|percentage|grade point average)(?:\s*(?:of|:|is|=|\-)\s*)?((?:\d{1,2}|\d\.\d{1,2})[\/\s]?(?:\/\s?(?:\d{1,2}|\d\.\d{1,2}))?)(?:\/[0-9.]+)?"

    # Contact Information patterns - improved to handle various formats
    email_pattern = r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
    phone_pattern = r"\b(?:\+\d{1,3}[\s\-\.]?)?(?:\(?\d{3}\)?[\s\-\.]?)?\d{3}[\s\-\.]\d{4}\b"
    # Alternative phone pattern for different formats
    alt_phone_pattern = r"\b(?:\+\d{1,3}[\s\-\.]?)?(?:\d{5,6}[\s\-\.]\d{5,6})\b"

    # LinkedIn or social media pattern
    linkedin_pattern = r"(?:linkedin\.com\/in\/|linkedin:)[a-zA-Z0-9\-]+(?:\/)?|(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9\-]+"

    # Extract certifications using the explicit pattern
    explicit_certs = []
    for match in re.finditer(cert_explicit_pattern, resume_lower):
        cert = match.group(1).strip()
        if cert and len(cert) > 2:  # Filter out very short matches
            explicit_certs.append(cert)

    # Extract certifications from lists (if available)
    cert_lists = re.findall(cert_list_pattern, resume, re.IGNORECASE | re.DOTALL)
    list_certs = []
    if cert_lists:
        for cert_list in cert_lists:
            # Split by common list item delimiters
            items = re.split(r'(?:\n\s*[\-\•\*]\s*|\n\s*\d+\.\s*)', cert_list.strip())
            for item in items:
                item = item.strip()
                if item and len(item) > 2 and not any(skill in item.lower() for skill in skills_matches):
                    list_certs.append(item)

    # Clean up and combine certifications, removing any that are likely skills
    all_certs = explicit_certs + list_certs
    all_certs = [cert for cert in all_certs if cert and len(cert) > 2]

    # Process the problem with certifications in "certifications in Python, ReactJS, and Machine Learning"
    special_cert_pattern = r"(?:certification(?:s)?|certified|certificate)(?:\sin|\:|\s-\s|\s)\s*((?:[a-zA-Z]+(?:\s?[,&]\s?)?)+)"
    special_matches = re.findall(special_cert_pattern, resume, re.IGNORECASE)

    additional_certs = []
    for match in special_matches:
        # Split by commas, 'and', or '&'
        cert_items = re.split(r'\s*(?:,|\sand\s|\s&\s)\s*', match)
        for item in cert_items:
            item = item.strip()
            if item and len(item) > 2:
                additional_certs.append(item)

    # Add the special case certifications
    all_certs.extend(additional_certs)

    # Remove duplicates while preserving case from original text
    unique_certs = []
    lowercase_certs = set()
    for cert in all_certs:
        if cert.lower() not in lowercase_certs:
            lowercase_certs.add(cert.lower())
            # Find the original case in the resume
            original_case = find_original_case(resume, cert)
            unique_certs.append(original_case if original_case else cert)

    # Extracting education
    education_data = {}
    for edu_type, pattern in education_pattern.items():
        matches = re.findall(pattern, resume, re.IGNORECASE)
        if matches:
            education_data[edu_type] = [find_original_case(resume, match) for match in matches if match]

    # Extracting experience
    experience_data = {}
    for exp_type, pattern in experience_pattern.items():
        matches = re.findall(pattern, resume, re.IGNORECASE)
        if matches:
            # For durations, matches might be tuples
            if exp_type == 'duration':
                experience_data[exp_type] = [(find_original_case(resume, start), find_original_case(resume, end))
                                            for start, end in matches if start and end]
            else:
                experience_data[exp_type] = [find_original_case(resume, match) for match in matches if match]

    # Extract GPA
    gpa_match = re.search(gpa_pattern, resume, re.IGNORECASE)
    gpa = gpa_match.group(1).strip() if gpa_match else None

    # Extract contact information
    email_match = re.search(email_pattern, resume)
    email = email_match.group(0) if email_match else None

    phone_match = re.search(phone_pattern, resume)
    if not phone_match:
        phone_match = re.search(alt_phone_pattern, resume)
    phone = phone_match.group(0) if phone_match else None

    # Extract LinkedIn
    linkedin_match = re.search(linkedin_pattern, resume, re.IGNORECASE)
    linkedin = linkedin_match.group(0) if linkedin_match else None

    # Extract all skills with original case
    final_skills = []
    for skill in skills_matches:
        original_case = find_original_case(resume, skill)
        final_skills.append(original_case if original_case else skill)

    # Return all extracted information
    return {
        "skills": list(set(final_skills)),
        "certifications": unique_certs,
        "education": education_data,
        "experience": experience_data,
        "gpa": gpa,
        "email": email,
        "phone": phone,
        "linkedin": linkedin
    }

def find_original_case(text, match_text):
    """Find the original case of a matched string in the full text."""
    pattern = re.compile(re.escape(match_text), re.IGNORECASE)
    match = pattern.search(text)
    return match.group(0) if match else match_text




current_dir = os.path.dirname(os.path.abspath(__file__))
skills_path = os.path.join(current_dir, '../data/skills.json')

with open(skills_path, 'r') as file:
    data = json.load(file)
    skills_list = data["skills"]

def extract_keywords(text):
    escaped_skills = [re.escape(skill) for skill in skills_list]
    keywords_pattern = r"\b(?:{})\b".format("|".join(escaped_skills))
    keywords = re.findall(keywords_pattern, text, re.IGNORECASE)
    return list(set([keyword.lower() for keyword in keywords]))
