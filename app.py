from flask import Flask, request, jsonify, render_template
import os
import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Preprocessing function
def preprocess_email(email_text):
    email_text = email_text.lower()
    email_text = re.sub(r'http\S+|www\.\S+', '', email_text)
    email_text = email_text.translate(str.maketrans('', '', string.punctuation))
    email_text = re.sub(r'\d+', '', email_text)
    return email_text

# PhishingDetector class
class PhishingDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def train(self, emails, labels):
        emails = [preprocess_email(email) for email in emails]
        X = self.vectorizer.fit_transform(emails)
        self.model.fit(X, labels)
        print("Model training completed.")
    
    def predict(self, email):
        email = preprocess_email(email)
        X = self.vectorizer.transform([email])
        return self.model.predict_proba(X)[0]

# Load Dataset
def load_dataset(file_path):
    data = pd.read_csv(file_path)
    emails = data['email'].astype(str).tolist()
    labels = data['label'].tolist()
    return emails, labels

# Initialize Flask app and detector
app = Flask(__name__)
detector = PhishingDetector()

# Train the model with the dataset
data_file = 'emails_dataset.csv'
if not os.path.exists(data_file):
    print(f"Error: The dataset file '{data_file}' does not exist.")
    exit(1)

emails, labels = load_dataset(data_file)
detector.train(emails, labels)

# Define Home route to render index.html
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Define /predict route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    email = data.get('email', '').strip()
    if not email:
        return jsonify({'error': 'No email content provided.'}), 400

    probabilities = detector.predict(email)
    response = {
        'phishing_likelihood': float(probabilities[1]),
        'legitimate_likelihood': float(probabilities[0])
    }
    return jsonify(response)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
