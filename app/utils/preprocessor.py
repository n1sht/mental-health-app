import pandas as pd
import numpy as np

class MentalHealthPreprocessor:
    def __init__(self):
        self.feature_mappings = {
            'work_interfere': {
                'Never': 0.0, 'Rarely': 0.25, 'Sometimes': 0.5, 'Often': 1.0,
                'never': 0.0, 'rarely': 0.25, 'sometimes': 0.5, 'often': 1.0
            },
            'leave': {
                'Very easy': 0.0, 'Somewhat easy': 0.25, 'Somewhat difficult': 0.5,
                'Very difficult': 0.75, "Don't know": 0.5,
                'very easy': 0.0, 'somewhat easy': 0.25, 'somewhat difficult': 0.5,
                'very difficult': 0.75, "don't know": 0.5
            }
        }
        
        self.binary_features = [
            'self_employed', 'family_history', 'benefits', 'care_options',
            'wellness_program', 'seek_help', 'mental_health_consequence'
        ]
    
    def preprocess_survey_data(self, df):
        """Preprocess the original survey data for training"""
        
        df = df.copy()
        
        
        df = df.replace('NA', np.nan)
        
        
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        
        df = df[(df['Age'] >= 18) & (df['Age'] <= 100)]
        
        
        df['Age'] = (df['Age'] - 18) / (100 - 18)
        
        
        if 'work_interfere' in df.columns:
            
            df['work_interfere'] = df['work_interfere'].fillna('Sometimes')
            
            df['work_interfere'] = df['work_interfere'].apply(
                lambda x: self.feature_mappings['work_interfere'].get(x, 0.5)
            )
        
        
        if 'leave' in df.columns:
            df['leave'] = df['leave'].fillna("Don't know")
            df['leave'] = df['leave'].apply(
                lambda x: self.feature_mappings['leave'].get(x, 0.5)
            )
        
        
        for col in self.binary_features:
            if col in df.columns:
                
                df[col] = df[col].astype(str)

                df[col] = df[col].apply(lambda x: 
                    1 if x.lower() in ['yes', 'y', '1'] else 
                    0 if x.lower() in ['no', 'n', '0'] else 
                    0.5  
                )
        

        if 'treatment' in df.columns:
            df['treatment'] = df['treatment'].astype(str).apply(
                lambda x: 1 if x.lower() in ['yes', 'y', '1'] else 0
            )
        

        features = ['Age', 'self_employed', 'family_history', 'work_interfere',
                   'benefits', 'care_options', 'wellness_program', 'seek_help',
                   'leave', 'mental_health_consequence', 'treatment']
        

        df = df[features].dropna(subset=['treatment'])
        

        df = df.fillna(0.5)
        
        print(f"Processed {len(df)} valid records")
        print(f"Sample processed data:\n{df.head()}")
        
        return df
    
    def preprocess_user_input(self, data):
        """Preprocess user input for prediction"""

        age = float(data['age'])
        data['Age'] = (age - 18) / (100 - 18)
        

        data['work_interfere'] = self.feature_mappings['work_interfere'].get(
            data['work_interfere'], 0.5
        )
        data['leave'] = self.feature_mappings['leave'].get(
            data['leave'], 0.5
        )
        

        for col in self.binary_features:
            if col in data:
                val = data[col].lower()
                data[col] = 1 if val == 'yes' else 0 if val == 'no' else 0.5
        
        # Create feature vector
        features = ['Age', 'self_employed', 'family_history', 'work_interfere',
                   'benefits', 'care_options', 'wellness_program', 'seek_help',
                   'leave', 'mental_health_consequence']
        
        return pd.DataFrame([{f: data[f] for f in features}])