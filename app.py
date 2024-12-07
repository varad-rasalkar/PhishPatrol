import re
import string
import numpy as np
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from flask import Flask, request, jsonify

# Step 1: Preprocessing Functions
def preprocess_email(email_text):
    # Lowercase the text
    email_text = email_text.lower()
    # Remove URLs
    email_text = re.sub(r'http\S+|www\.\S+', '', email_text)
    # Remove punctuation
    email_text = email_text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    email_text = re.sub(r'\d+', '', email_text)
    return email_text

# Step 2: Feature Extraction with TF-IDF
class PhishingDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = RandomForestClassifier(n_estimators=100)  # Reduced for faster training

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
    # Load dataset assuming a CSV with 'email' and 'label' columns
    data = pd.read_csv(file_path)
    emails = data['email'].astype(str).tolist()
    labels = data['label'].tolist()
    return emails, labels

# Flask Backend
app = Flask(__name__)
detector = PhishingDetector()

# Train the model with the dataset
data_file = 'emails_dataset.csv'  # Ensure this file exists in the project directory
if not os.path.exists(data_file):
    print(f"Error: The dataset file '{data_file}' does not exist.")
    exit(1)

emails, labels = load_dataset(data_file)
detector.train(emails, labels)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    email = data.get('email', '')
    if not email:
        return jsonify({'error': 'No email content provided'}), 400

    probabilities = detector.predict(email)
    response = {
        'phishing_likelihood': probabilities[1],
        'legitimate_likelihood': probabilities[0]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
