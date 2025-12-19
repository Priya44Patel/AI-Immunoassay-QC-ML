"""
Purpose

Train ML model to classify PASS / FAIL plates
"""
"""
ml_models.py
------------
Machine learning utilities for QC classification.
"""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


def train_model(X, y):
    """
    Train RandomForest classifier.
    """
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    model.fit(X, y)
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance.
    """
    preds = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
