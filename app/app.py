from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import json
import os

app = Flask(__name__)

model = joblib.load('app/models/mental_health_model.pkl')
preprocessor = joblib.load('app/models/preprocessor.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:

        data = request.json
        

        X = preprocessor.preprocess_user_input(data)
        

        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]
        

        risk_analysis = analyze_risk_factors(data)
        

        save_submission(data, prediction, probability)
        

        response = {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': get_risk_level(probability),
            'risk_factors': risk_analysis,
            'recommendations': get_recommendations(probability, risk_analysis)
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def analyze_risk_factors(data):
    """Analyze individual risk factors"""
    risk_factors = []
    
    if data['family_history'] == 'yes':
        risk_factors.append({
            'factor': 'Family History',
            'severity': 'high',
            'description': 'Family history of mental health issues increases risk'
        })
    
    if data['work_interfere'] in ['often', 'sometimes']:
        risk_factors.append({
            'factor': 'Work Interference',
            'severity': 'high' if data['work_interfere'] == 'often' else 'medium',
            'description': 'Mental health affecting work performance'
        })
    
    if data['benefits'] == 'no':
        risk_factors.append({
            'factor': 'No Benefits',
            'severity': 'medium',
            'description': 'Lack of mental health benefits at workplace'
        })
    
    if data['seek_help'] == 'no':
        risk_factors.append({
            'factor': 'Help Avoidance',
            'severity': 'high',
            'description': 'Reluctance to seek professional help'
        })
    
    return risk_factors

def get_risk_level(probability):
    """Determine risk level based on probability"""
    if probability >= 0.8:
        return 'critical'
    elif probability >= 0.6:
        return 'high'
    elif probability >= 0.4:
        return 'moderate'
    elif probability >= 0.2:
        return 'low'
    else:
        return 'minimal'

def get_recommendations(probability, risk_factors):
    """Generate personalized recommendations"""
    recommendations = []
    
    if probability >= 0.5:
        recommendations.append({
            'priority': 'high',
            'action': 'Consult a mental health professional',
            'description': 'Consider scheduling an appointment with a therapist or counselor'
        })
    
    if any(rf['factor'] == 'Work Interference' for rf in risk_factors):
        recommendations.append({
            'priority': 'medium',
            'action': 'Talk to HR about mental health resources',
            'description': 'Many workplaces offer Employee Assistance Programs (EAP)'
        })
    
    if probability >= 0.3:
        recommendations.append({
            'priority': 'medium',
            'action': 'Practice self-care',
            'description': 'Regular exercise, meditation, and adequate sleep can help'
        })
    
    recommendations.append({
        'priority': 'low',
        'action': 'Build a support network',
        'description': 'Stay connected with friends and family'
    })
    
    return recommendations

def save_submission(data, prediction, probability):
    """Save submission to JSON file"""
    submission = {
        'timestamp': datetime.now().isoformat(),
        'data': data,
        'prediction': int(prediction),
        'probability': float(probability)
    }
    

    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'data/submissions/submissions_{date_str}.json'
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            submissions = json.load(f)
    else:
        submissions = []
    
    submissions.append(submission)
    
    with open(filename, 'w') as f:
        json.dump(submissions, f, indent=2)

@app.route('/stats')
def stats():
    """Get statistics about submissions"""
    total_submissions = 0
    needs_treatment = 0
    
    submissions_dir = 'data/submissions'
    if os.path.exists(submissions_dir):
        for filename in os.listdir(submissions_dir):
            if filename.endswith('.json'):
                with open(f'{submissions_dir}/{filename}', 'r') as f:
                    submissions = json.load(f)
                    total_submissions += len(submissions)
                    needs_treatment += sum(1 for s in submissions if s['prediction'] == 1)
    
    return jsonify({
        'total_submissions': total_submissions,
        'needs_treatment': needs_treatment,
        'percentage': (needs_treatment / total_submissions * 100) if total_submissions > 0 else 0
    })

if __name__ == '__main__':
    app.run(debug=True)