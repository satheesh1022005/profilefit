from flask import Flask, request, jsonify
from flask_cors import CORS  # to handle requests from React
from model.matching import predict_match

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "✅ AI Profile Matcher API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    resume = data.get('resume')
    opportunity = data.get('opportunity')

    if not resume or not opportunity:
        return jsonify({'error': 'Resume and opportunity fields are required.'}), 400

    match_score = predict_match(resume, opportunity)

    return jsonify({'match_percentage': match_score})

if __name__ == '__main__':
    app.run(debug=True)
