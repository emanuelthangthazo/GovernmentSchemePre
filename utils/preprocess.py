"""
Data Preprocessing Utilities
Contains functions for data cleaning, encoding, and validation.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import logging

logger = logging.getLogger(__name__)


def clean_data(df):
    """
    Clean the dataset by handling missing values and inconsistencies.
    
    Args:
        df: pandas DataFrame to clean
        
    Returns:
        Cleaned pandas DataFrame
    """
    df_cleaned = df.copy()
    
    # Fill missing numerical values with median
    numerical_cols = df_cleaned.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        if df_cleaned[col].isnull().sum() > 0:
            median_val = df_cleaned[col].median()
            df_cleaned[col].fillna(median_val, inplace=True)
    
    # Fill missing categorical values with mode
    categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_cleaned[col].isnull().sum() > 0:
            mode_val = df_cleaned[col].mode()[0] if len(df_cleaned[col].mode()) > 0 else 'Unknown'
            df_cleaned[col].fillna(mode_val, inplace=True)
    
    logger.info("Data cleaning completed")
    return df_cleaned


def create_label_encoders(df, columns_to_encode):
    """
    Create LabelEncoders for specified categorical columns.
    
    Args:
        df: pandas DataFrame
        columns_to_encode: list of column names to encode
        
    Returns:
        Dictionary of column name -> LabelEncoder pairs
    """
    encoders = {}
    
    for column in columns_to_encode:
        if column in df.columns:
            encoder = LabelEncoder()
            # Fit encoder on the column
            encoder.fit(df[column].astype(str))
            encoders[column] = encoder
            logger.info(f"Created encoder for column: {column}")
        else:
            logger.warning(f"Column {column} not found in DataFrame")
    
    return encoders


def encode_dataframe(df, encoders):
    """
    Encode categorical columns using provided LabelEncoders.
    
    Args:
        df: pandas DataFrame to encode
        encoders: Dictionary of column name -> LabelEncoder pairs
        
    Returns:
        Encoded pandas DataFrame
    """
    df_encoded = df.copy()
    
    for column, encoder in encoders.items():
        if column in df_encoded.columns:
            # Handle unknown categories by replacing with most common
            try:
                df_encoded[column] = encoder.transform(df_encoded[column].astype(str))
            except ValueError as e:
                logger.warning(f"Unknown categories in {column}: {str(e)}")
                # Replace unknown categories with the most common category
                most_common = encoder.classes_[0]
                df_encoded[column] = df_encoded[column].apply(
                    lambda x: most_common if str(x) not in encoder.classes_ else x
                )
                df_encoded[column] = encoder.transform(df_encoded[column].astype(str))
    
    logger.info("DataFrame encoding completed")
    return df_encoded


def validate_input_data(data_dict, required_fields):
    """
    Validate input data dictionary for required fields and valid values.
    
    Args:
        data_dict: Dictionary containing input data
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in data_dict or not data_dict[field]]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # Validate numerical fields
    numerical_fields = ['Age', 'Income']
    for field in numerical_fields:
        if field in data_dict:
            try:
                value = float(data_dict[field])
                if value < 0:
                    return False, f"{field} cannot be negative"
            except (ValueError, TypeError):
                return False, f"{field} must be a valid number"
    
    return True, None


def get_feature_importance(model, feature_names):
    """
    Get feature importance from a trained model.
    
    Args:
        model: Trained scikit-learn model with feature_importances_ attribute
        feature_names: List of feature names
        
    Returns:
        DataFrame with feature names and their importance scores
    """
    if hasattr(model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        return importance_df
    else:
        logger.warning("Model does not have feature_importances_ attribute")
        return None


def prepare_prediction_input(form_data, encoders, feature_columns):
    """
    Prepare form data for model prediction by encoding and ordering features.
    
    Args:
        form_data: Dictionary containing form input data
        encoders: Dictionary of LabelEncoders
        feature_columns: List of feature columns in correct order
        
    Returns:
        pandas DataFrame ready for prediction
    """
    encoded_data = {}
    
    # Map form field names to feature column names
    field_mapping = {
        'age': 'Age',
        'gender': 'Gender',
        'income': 'Income',
        'farmer': 'Farmer',
        'student': 'Student',
        'disability': 'Disability',
        'bpl': 'BPL',
        'occupation': 'Occupation',
        'district': 'District',
        'marital_status': 'Marital_Status',
        'girl_child': 'Girl_Child',
        'street_vendor': 'Street_Vendor',
        'artisan': 'Artisan',
        'woman_shg': 'Woman_SHG',
        'rural_household': 'Rural_Household'
    }
    
    # Encode each field
    for form_field, feature_name in field_mapping.items():
        value = form_data.get(form_field)
        
        if value is None or value == '':
            encoded_data[feature_name] = 0
            continue
        
        if feature_name in ['Age', 'Income']:
            # Keep numerical values as is
            try:
                encoded_data[feature_name] = float(value)
            except (ValueError, TypeError):
                encoded_data[feature_name] = 0
        else:
            # Encode categorical values
            if feature_name in encoders:
                try:
                    encoder = encoders[feature_name]
                    encoded_data[feature_name] = encoder.transform([str(value)])[0]
                except ValueError:
                    # Unknown category, use default
                    encoded_data[feature_name] = 0
                except Exception as e:
                    logger.error(f"Error encoding {feature_name}: {str(e)}")
                    encoded_data[feature_name] = 0
            else:
                encoded_data[feature_name] = 0
    
    # Create DataFrame with correct feature order
    prediction_data = {}
    for column in feature_columns:
        prediction_data[column] = encoded_data.get(column, 0)
    
    df = pd.DataFrame([prediction_data], columns=feature_columns)
    
    return df


def get_prediction_confidence(model, prediction_df):
    """
    Get prediction confidence scores using predict_proba.
    
    Args:
        model: Trained scikit-learn classifier
        prediction_df: DataFrame with input features
        
    Returns:
        Tuple of (predicted_class, confidence_percentage)
    """
    if hasattr(model, 'predict_proba'):
        prediction = model.predict(prediction_df)[0]
        probabilities = model.predict_proba(prediction_df)[0]
        confidence = max(probabilities) * 100
        return prediction, confidence
    else:
        logger.warning("Model does not support predict_proba")
        prediction = model.predict(prediction_df)[0]
        return prediction, 0.0
