import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import sys
sys.path.append('app')
from utils.preprocessor import MentalHealthPreprocessor


preprocessor = MentalHealthPreprocessor()


print("Loading data...")
df = pd.read_csv('data/mental_health_survey.csv')
df = preprocessor.preprocess_survey_data(df)

print(f"Processed {len(df)} records")
print(f"Class distribution:\n{df['treatment'].value_counts()}")


X = df.drop('treatment', axis=1)
y = df['treatment']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


print("\nTraining model...")
model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    subsample=0.8,
    random_state=42
)

model.fit(X_train, y_train)


print("\nEvaluating model...")
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")


cv_scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
print(f"\nCross-validation ROC-AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")


print("\nTesting extreme cases...")


worst_case = pd.DataFrame({
    'Age': [(35-18)/(100-18)],
    'self_employed': [1],
    'family_history': [1],
    'work_interfere': [1.0],
    'benefits': [0],
    'care_options': [0],
    'wellness_program': [0],
    'seek_help': [0],
    'leave': [0.75],
    'mental_health_consequence': [1]
})

worst_pred = model.predict_proba(worst_case)[0][1]
print(f"Worst case confidence: {worst_pred:.1%}")


best_case = pd.DataFrame({
    'Age': [(25-18)/(100-18)],
    'self_employed': [0],
    'family_history': [0],
    'work_interfere': [0.0],
    'benefits': [1],
    'care_options': [1],
    'wellness_program': [1],
    'seek_help': [1],
    'leave': [0.0],
    'mental_health_consequence': [0]
})

best_pred = model.predict_proba(best_case)[0][1]
print(f"Best case confidence: {best_pred:.1%}")


print("\nSaving model...")
joblib.dump(model, 'app/models/mental_health_model.pkl')
joblib.dump(preprocessor, 'app/models/preprocessor.pkl')


X.head(1).to_csv('app/models/features.csv', index=False)

print("\nModel training complete!")