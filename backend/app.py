from flask import Flask, request, jsonify
from flask_cors import CORS
from model.matching import predict_match
from utils.preprocess import extract_resume_data,extract_keywords
from logs.logs import logger  # ✅ importing logger
import PyPDF2
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ AI Profile Matcher API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    resume = data.get('resume')
    opportunity = data.get('opportunity')

    if not isinstance(resume, str) or len(resume.strip()) == 0:
        logger.warning("Invalid or empty resume field.")
        return jsonify({'error': 'Invalid or empty resume field.'}), 400

    if not isinstance(opportunity, str) or len(opportunity.strip()) == 0:
        logger.warning("Invalid or empty opportunity field.")
        return jsonify({'error': 'Invalid or empty opportunity field.'}), 400

    match_score = predict_match(resume, opportunity)

    logger.info(f"Resume: {resume} | Opportunity: {opportunity} | Match: {match_score}%")

    return jsonify({'match_percentage': match_score})


@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()

    resume = data.get('resume')

    if not isinstance(resume, str) or len(resume.strip()) == 0:
        return jsonify({'error': 'Invalid or empty resume field.'}), 400

    # Extract data from the resume
    extracted_data = extract_resume_data(resume)

    return jsonify(extracted_data)

@app.route('/missing_keywords', methods=['POST'])
def missing_keywords():
    data = request.get_json()

    resume = data.get('resume')
    opportunity = data.get('opportunity')

    if not isinstance(resume, str) or len(resume.strip()) == 0:
        return jsonify({'error': 'Invalid or empty resume field.'}), 400

    if not isinstance(opportunity, str) or len(opportunity.strip()) == 0:
        return jsonify({'error': 'Invalid or empty opportunity field.'}), 400

    resume_keywords = extract_keywords(resume)
    opportunity_keywords = extract_keywords(opportunity)

    missing = [word for word in opportunity_keywords if word not in resume_keywords]

    logger.info(f"Missing keywords from Resume: {missing}")

    return jsonify({'missing_keywords': missing})

@app.route('/extract_text_from_pdf', methods=['POST'])
def extract_text_from_pdf():
    # Check if file is present in request
    if 'file' not in request.files:
        logger.warning("No file part in the request")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if file was selected
    if file.filename == '':
        logger.warning("No file selected")
        return jsonify({'error': 'No file selected'}), 400

    # Check if file is PDF
    if not file.filename.lower().endswith('.pdf'):
        logger.warning("Uploaded file is not a PDF")
        return jsonify({'error': 'Uploaded file must be a PDF'}), 400

    try:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return jsonify({"text": text})
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        return jsonify({'error': 'Error processing PDF file'}), 500

if __name__ == '__main__':
    app.run(debug=True)
