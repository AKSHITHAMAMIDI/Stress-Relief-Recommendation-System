"""
train_model.py
---------------
Generates a synthetic-but-realistic lifestyle dataset and trains a
RandomForestClassifier to predict a person's stress level (Low/Medium/High)
from their daily habits. Saves the trained model + feature scaler to disk
so the Streamlit app can load them instantly without retraining.

Run once:  python train_model.py
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

FEATURES = [
    "sleep_hours",
    "work_hours",
    "screen_time_hours",
    "physical_activity_hours",
    "social_interaction_score",   # 1 (isolated) - 10 (very social)
    "mood_score",                 # 1 (very low mood) - 10 (great mood)
    "caffeine_cups",
    "meditation_minutes",
]


def generate_synthetic_dataset(n=6000):
    """Create a synthetic dataset where the stress label is derived from a
    weighted, noisy combination of lifestyle features -- mimicking real
    survey-style stress research (e.g., PSS-style predictors)."""
    sleep_hours = np.clip(np.random.normal(6.5, 1.5, n), 2, 11)
    work_hours = np.clip(np.random.normal(8, 2.5, n), 0, 16)
    screen_time_hours = np.clip(np.random.normal(6, 2.5, n), 0, 16)
    physical_activity_hours = np.clip(np.random.exponential(0.6, n), 0, 3)
    social_interaction_score = np.clip(np.random.normal(5.5, 2, n), 1, 10)
    mood_score = np.clip(np.random.normal(5.5, 2, n), 1, 10)
    caffeine_cups = np.clip(np.random.poisson(2, n), 0, 8)
    meditation_minutes = np.clip(np.random.exponential(5, n), 0, 60)

    # Weighted "true" stress score (higher = more stressed)
    raw_score = (
        -1.4 * (sleep_hours - 7)
        + 0.55 * (work_hours - 8)
        + 0.45 * (screen_time_hours - 6)
        - 0.9 * physical_activity_hours
        - 0.5 * (social_interaction_score - 5.5)
        - 0.8 * (mood_score - 5.5)
        + 0.35 * caffeine_cups
        - 0.12 * meditation_minutes
        + np.random.normal(0, 2.2, n)  # noise
    )

    # Convert to 3 classes using quantile-based thresholds for balance
    low_thresh, high_thresh = np.percentile(raw_score, [33, 66])
    labels = np.where(
        raw_score <= low_thresh, "Low",
        np.where(raw_score <= high_thresh, "Medium", "High")
    )

    df = pd.DataFrame({
        "sleep_hours": sleep_hours,
        "work_hours": work_hours,
        "screen_time_hours": screen_time_hours,
        "physical_activity_hours": physical_activity_hours,
        "social_interaction_score": social_interaction_score,
        "mood_score": mood_score,
        "caffeine_cups": caffeine_cups,
        "meditation_minutes": meditation_minutes,
        "stress_level": labels,
    })
    return df


def train_and_save():
    df = generate_synthetic_dataset()
    X = df[FEATURES]
    y = df["stress_level"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=5,
        random_state=RANDOM_SEED,
        class_weight="balanced",
    )
    model.fit(X_train_scaled, y_train)

    preds = model.predict(X_test_scaled)
    print("=== Model evaluation on held-out test set ===")
    print(classification_report(y_test, preds))

    joblib.dump(model, "stress_model.pkl")
    joblib.dump(scaler, "stress_scaler.pkl")
    df.to_csv("synthetic_stress_data.csv", index=False)
    print("Saved: stress_model.pkl, stress_scaler.pkl, synthetic_stress_data.csv")


if __name__ == "__main__":
    train_and_save()
