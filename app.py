"""
Government Scheme Predictor - Flask Web Application
Main application file for handling model loading, predictions, and routes.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
import joblib
import pandas as pd
import numpy as np
from werkzeug.exceptions import NotFound, InternalServerError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'scheme_model.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR, 'encoders.pkl')
FEATURE_COLUMNS_PATH = os.path.join(BASE_DIR, 'feature_columns.pkl')
TARGET_ENCODER_PATH = os.path.join(BASE_DIR, 'target_encoder.pkl')

# Global variables for model and encoders
model = None
encoders = None
feature_columns = None
target_encoder = None


def load_model_and_encoders():
    """
    Load the trained model, label encoders, and feature columns.
    Returns True if successful, False otherwise.
    """
    global model, encoders, feature_columns, target_encoder
    
    try:
        # Load the trained Random Forest model
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            logger.info("Model loaded successfully")
        else:
            logger.warning(f"Model file not found at {MODEL_PATH}")
            return False
        
        # Load label encoders
        if os.path.exists(ENCODERS_PATH):
            encoders_data = joblib.load(ENCODERS_PATH)
            encoders = encoders_data
            logger.info("Encoders loaded successfully")
        else:
            logger.warning(f"Encoders file not found at {ENCODERS_PATH}")
            return False
        
        # Load feature columns
        if os.path.exists(FEATURE_COLUMNS_PATH):
            feature_columns = joblib.load(FEATURE_COLUMNS_PATH)
            logger.info("Feature columns loaded successfully")
        else:
            logger.warning(f"Feature columns file not found at {FEATURE_COLUMNS_PATH}")
            return False
        
        # Load target encoder for decoding predictions
        if os.path.exists(TARGET_ENCODER_PATH):
            target_encoder = joblib.load(TARGET_ENCODER_PATH)
            logger.info("Target encoder loaded successfully")
        else:
            logger.warning(f"Target encoder file not found at {TARGET_ENCODER_PATH}")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Error loading model and encoders: {str(e)}")
        return False


def encode_input_data(form_data):
    """
    Encode categorical input data using the loaded label encoders.
    
    Args:
        form_data: Dictionary containing form data
        
    Returns:
        Dictionary with encoded values
    """
    encoded_data = {}
    
    for column, value in form_data.items():
        if column in encoders and value is not None and value != '':
            try:
                # Handle categorical encoding
                if column in ['Age', 'Income']:
                    # Keep numerical values as is
                    encoded_data[column] = float(value)
                else:
                    # Encode categorical values
                    encoder = encoders[column]
                    encoded_data[column] = encoder.transform([value])[0]
            except ValueError as e:
                logger.warning(f"Unknown category for {column}: {value}")
                encoded_data[column] = 0  # Default to first category
            except Exception as e:
                logger.error(f"Error encoding {column}: {str(e)}")
                encoded_data[column] = 0
        else:
            # Handle numerical values or missing encoders
            try:
                encoded_data[column] = float(value) if value else 0
            except (ValueError, TypeError):
                encoded_data[column] = 0
    
    return encoded_data


def create_prediction_dataframe(encoded_data):
    """
    Create a DataFrame with the exact feature order used during training.

    Args:
        encoded_data: Dictionary with encoded feature values

    Returns:
        pandas DataFrame with correct feature order
    """
    # Create dictionary with all features, filling missing ones with 0
    prediction_data = {}

    for column in feature_columns:
        if column in encoded_data:
            prediction_data[column] = encoded_data[column]
        else:
            prediction_data[column] = 0

    # Create DataFrame with correct column order
    df = pd.DataFrame([prediction_data], columns=feature_columns)

    return df


def generate_recommendations(form_data):
    """
    Generate rule-based scheme recommendations based on form data.

    Args:
        form_data: Dictionary containing form submission data

    Returns:
        List of recommended scheme dictionaries
    """
    recommendations = []

    # Parse income for low income check
    try:
        income = float(form_data.get('income', 0)) if form_data.get('income') else 0
    except (ValueError, TypeError):
        income = 0

    # Farmer recommendations
    if form_data.get('farmer') == 'Yes':
        recommendations.append({
            'name': 'PM Kisan Samman Nidhi',
            'icon': 'bi-plant',
            'description': 'Income support of ₹6,000 per year for farmers',
            'reason': 'Farmer',
            'eligibility': 'All Farmers'
        })
        recommendations.append({
            'name': 'Kisan Credit Card (KCC)',
            'icon': 'bi-credit-card',
            'description': 'Credit facility for farmers for agricultural needs',
            'reason': 'Farmer',
            'eligibility': 'Farmers with land'
        })

    # Student recommendations
    if form_data.get('student') == 'Yes':
        recommendations.append({
            'name': 'National Scholarship Portal (NSP)',
            'icon': 'bi-mortarboard',
            'description': 'Central and state government scholarships for students',
            'reason': 'Student',
            'eligibility': 'Students based on merit/income'
        })
        recommendations.append({
            'name': 'AICTE Scholarship',
            'icon': 'bi-book',
            'description': 'Technical education scholarships for meritorious students',
            'reason': 'Student',
            'eligibility': 'Technical students'
        })

    # Disability recommendations
    if form_data.get('disability') == 'Yes':
        recommendations.append({
            'name': 'Unique Disability ID (UDID)',
            'icon': 'bi-person-badge',
            'description': 'Universal identity card for persons with disabilities',
            'reason': 'Disability',
            'eligibility': 'Persons with disabilities'
        })
        recommendations.append({
            'name': 'Assistance to Disabled Persons',
            'icon': 'bi-heart',
            'description': 'Financial assistance for aids and appliances',
            'reason': 'Disability',
            'eligibility': 'Persons with disabilities'
        })

    # Pregnancy recommendations
    if form_data.get('pregnant') == '1':
        recommendations.append({
            'name': 'Pradhan Mantri Matru Vandana Yojana (PMMVY)',
            'icon': 'bi-person-heart',
            'description': 'Maternity benefit of ₹5,000 for pregnant women',
            'reason': 'Pregnant',
            'eligibility': 'Pregnant women & lactating mothers'
        })

    # Senior Citizen recommendations
    if form_data.get('senior_citizen') == '1':
        recommendations.append({
            'name': 'Atal Pension Yojana',
            'icon': 'bi-piggy-bank',
            'description': 'Pension scheme for unorganized sector workers',
            'reason': 'Senior Citizen',
            'eligibility': 'Age 18-40 years'
        })
        recommendations.append({
            'name': 'National Social Assistance Programme',
            'icon': 'bi-shield-check',
            'description': 'Pension support for elderly, widows, and disabled',
            'reason': 'Senior Citizen',
            'eligibility': 'BPL families'
        })

    # Woman SHG recommendations
    if form_data.get('woman_shg') == 'Yes':
        recommendations.append({
            'name': 'National Rural Livelihood Mission (NRLM)',
            'icon': 'bi-people',
            'description': 'Poverty alleviation program for rural women SHGs',
            'reason': 'Woman SHG Member',
            'eligibility': 'Rural women SHGs'
        })
        recommendations.append({
            'name': 'Mudra Yojana',
            'icon': 'bi-cash',
            'description': 'Loans for micro enterprises and small businesses',
            'reason': 'Woman SHG Member',
            'eligibility': 'Micro enterprises'
        })

    # Street Vendor recommendations
    if form_data.get('street_vendor') == 'Yes':
        recommendations.append({
            'name': 'PM SVANidhi',
            'icon': 'bi-cart',
            'description': 'Working capital loan for street vendors',
            'reason': 'Street Vendor',
            'eligibility': 'Street vendors'
        })

    # Artisan recommendations
    if form_data.get('artisan') == 'Yes':
        recommendations.append({
            'name': 'PM Vishwakarma',
            'icon': 'bi-tools',
            'description': 'Support for traditional artisans and craftsmen',
            'reason': 'Artisan',
            'eligibility': 'Traditional artisans'
        })

    # Low income recommendations
    if income < 100000:  # Below 1 lakh
        recommendations.append({
            'name': 'Ayushman Bharat',
            'icon': 'bi-hospital',
            'description': 'Health insurance coverage of ₹5 lakh per family',
            'reason': 'Low Income',
            'eligibility': 'BPL/AAY families'
        })
        recommendations.append({
            'name': 'Pradhan Mantri Awas Yojana (PMAY)',
            'icon': 'bi-house',
            'description': 'Housing for all with interest subsidy',
            'reason': 'Low Income',
            'eligibility': 'EWS/LIG/MIG'
        })

    # Rural household recommendations
    if form_data.get('rural_household') == 'Yes':
        recommendations.append({
            'name': 'PMAY Gramin',
            'icon': 'bi-house-heart',
            'description': 'Rural housing scheme with financial assistance',
            'reason': 'Rural Household',
            'eligibility': 'Rural BPL families'
        })
        recommendations.append({
            'name': 'MGNREGA',
            'icon': 'bi-hammer',
            'description': 'Guaranteed wage employment for rural households',
            'reason': 'Rural Household',
            'eligibility': 'Rural households'
        })

    # Limit to 5 recommendations
    return recommendations[:5]


# Load model and encoders on startup
if not load_model_and_encoders():
    logger.warning("Model or encoders could not be loaded. Application may not function correctly.")


# ==================== Routes ====================

@app.route('/')
def index():
    """Render the home page with prediction form."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests.
    Validates form data, encodes it, and returns prediction.
    """
    try:
        # Check if model is loaded
        if model is None:
            return render_template(
                'error.html',
                error_message="Model not loaded. Please ensure the model files are present.",
                error_code="MODEL_NOT_LOADED"
            ), 500
        
        # Get form data (using lowercase keys to match HTML input names and template variables)
        # For prediction, we'll create a separate dict with capitalized keys for encoding
        form_data = {
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'income': request.form.get('income'),
            'farmer': request.form.get('farmer'),
            'student': request.form.get('student'),
            'disability': request.form.get('disability'),
            'bpl': request.form.get('bpl'),
            'occupation': request.form.get('occupation'),
            'district': request.form.get('district'),
            'marital_status': request.form.get('marital_status'),
            'girl_child': request.form.get('girl_child'),
            'street_vendor': request.form.get('street_vendor'),
            'artisan': request.form.get('artisan'),
            'woman_shg': request.form.get('woman_shg'),
            'rural_household': request.form.get('rural_household'),
            'pregnant': request.form.get('pregnant', '0'),  # Default to 0 if not provided
            'senior_citizen': request.form.get('senior_citizen', '0')  # Default to 0 if not provided
        }
        
        # Validate required fields (using lowercase keys to match form_data)
        required_fields = ['age', 'gender', 'income', 'occupation', 'district']
        missing_fields = [field for field in required_fields if not form_data.get(field)]
        
        if missing_fields:
            return render_template(
                'error.html',
                error_message=f"Please fill in all required fields: {', '.join(missing_fields)}",
                error_code="VALIDATION_ERROR"
            ), 400
        
        # Encode input data (convert to capitalized keys for encoding)
        # Create a mapping from lowercase to capitalized keys for model compatibility
        key_mapping = {
            'age': 'Age',
            'gender': 'Gender',
            'income': 'Income',
            'farmer': 'Farmer',
            'student': 'Student',
            'disability': 'Disability',
            'bpl': 'BPL',
            'occupation': 'Occupation',
            'district': 'District',
            'marital_status': 'MaritalStatus',
            'girl_child': 'GirlChild',
            'street_vendor': 'StreetVendor',
            'artisan': 'Artisan',
            'woman_shg': 'WomanSHG',
            'rural_household': 'RuralHousehold'
        }
        
        # Create encoding dict with capitalized keys
        encoding_data = {key_mapping[k]: v for k, v in form_data.items() if k in key_mapping}
        encoded_data = encode_input_data(encoding_data)
        
        # Create prediction DataFrame
        prediction_df = create_prediction_dataframe(encoded_data)
        
        # Make prediction
        prediction_encoded = model.predict(prediction_df)[0]
        
        # Get prediction confidence
        prediction_proba = model.predict_proba(prediction_df)[0]
        confidence = max(prediction_proba) * 100
        
        # Decode the prediction using target encoder
        if target_encoder is not None:
            predicted_scheme = target_encoder.inverse_transform([prediction_encoded])[0]
        else:
            predicted_scheme = str(prediction_encoded)
        
        logger.info(f"Prediction made: {predicted_scheme} with confidence: {confidence:.2f}%")

        # Generate rule-based recommendations
        recommendations = generate_recommendations(form_data)

        return render_template(
            'result.html',
            predicted_scheme=predicted_scheme,
            confidence=confidence,
            form_data=form_data,
            recommendations=recommendations
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return render_template(
            'error.html',
            error_message="An error occurred during prediction. Please try again.",
            error_code="PREDICTION_ERROR"
        ), 500


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('contact.html')


@app.route('/health')
def health():
    """Health check endpoint for deployment monitoring."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'encoders_loaded': encoders is not None,
        'target_encoder_loaded': target_encoder is not None
    })


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('error.html', error_message="Internal server error occurred."), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all uncaught exceptions."""
    logger.error(f"Unhandled exception: {str(error)}")
    return render_template(
        'error.html',
        error_message="An unexpected error occurred. Please try again later."
    ), 500


# ==================== Main ====================

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
