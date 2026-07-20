"""
Model Training Script for Government Scheme Predictor
This script trains the Random Forest model and saves it along with encoders and feature columns.
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings

warnings.filterwarnings('ignore')

# Load the dataset
print("Loading dataset...")
df = pd.read_csv(r"D:\New folder\Govt_Scheme_Dataset_10L_15_Schemes.csv")
print(f"Dataset loaded with shape: {df.shape}")

# Data Cleaning
print("Cleaning data...")
# Handle missing values in Income
df["Income"] = pd.to_numeric(df["Income"], errors="coerce")
df["Income"] = df["Income"].fillna(df["Income"].mean())

# Remove duplicates
df = df.drop_duplicates()

# Filter invalid ages
df = df[(df["Age"] >= 0) & (df["Age"] <= 100)]

print(f"Data after cleaning: {df.shape}")

# Create individual label encoders for each categorical column
print("Creating label encoders...")
categorical_columns = [
    "Gender",
    "Farmer",
    "Student",
    "Disability",
    "BPL",
    "Occupation",
    "District",
    "MaritalStatus",
    "GirlChild",
    "StreetVendor",
    "Artisan",
    "WomanSHG",
    "RuralHousehold",
    "Scheme"
]

encoders = {}
for col in categorical_columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col].astype(str))
    encoders[col] = encoder
    print(f"Created encoder for {col} with {len(encoder.classes_)} classes")

# Save the target encoder separately for decoding predictions
target_encoder = encoders["Scheme"]
print(f"Target encoder (Scheme) classes: {target_encoder.classes_}")

# Define feature columns (matching the notebook)
feature_columns = [
    "Age",
    "Gender",
    "Income",
    "Farmer",
    "Student",
    "Disability",
    "BPL",
    "Occupation",
    "District",
    "MaritalStatus",
    "GirlChild",
    "StreetVendor",
    "Artisan",
    "WomanSHG",
    "RuralHousehold"
]

# Prepare features and target
X = df[feature_columns]
y = df["Scheme"]

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the model
print("Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.4f}")

# Feature importance
print("\nFeature Importance:")
importance = model.feature_importances_
for feature, score in zip(feature_columns, importance):
    print(f"{feature}: {score:.4f}")

# Save the model and encoders
print("\nSaving model and encoders...")
joblib.dump(model, 'scheme_model.pkl')
print("Model saved as scheme_model.pkl")

joblib.dump(encoders, 'encoders.pkl')
print("Encoders saved as encoders.pkl")

joblib.dump(feature_columns, 'feature_columns.pkl')
print("Feature columns saved as feature_columns.pkl")

joblib.dump(target_encoder, 'target_encoder.pkl')
print("Target encoder saved as target_encoder.pkl")

print("\nTraining complete! All files saved successfully.")
print("You can now run the Flask application.")
