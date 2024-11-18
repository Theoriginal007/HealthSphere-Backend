# model.py for AI module

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Function to train a regression model for predicting health outcomes
def train_model(data, target_column, save_path='trained_model.pkl'):
    """
    Train a linear regression model using provided data.

    Parameters:
    - data: DataFrame containing feature columns and the target column
    - target_column: Name of the column to predict
    - save_path: Path to save the trained model

    Returns:
    - model: Trained model
    - metrics: A dictionary with training metrics
    """
    # Splitting the data into features and target
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initializing the model
    model = LinearRegression()
    
    # Training the model
    model.fit(X_train, y_train)
    
    # Making predictions
    y_pred = model.predict(X_test)
    
    # Calculating metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    metrics = {
        'mean_squared_error': mse,
        'r2_score': r2
    }
    
    # Saving the model
    joblib.dump(model, save_path)
    print(f"Model trained and saved to {save_path}")
    
    return model, metrics

# Function to load the model and make predictions
def predict(input_data, model_path='trained_model.pkl'):
    """
    Load a trained model and make predictions on new data.

    Parameters:
    - input_data: DataFrame or 2D array containing input data for prediction
    - model_path: Path to the trained model file

    Returns:
    - predictions: Array of predicted values
    """
    try:
        model = joblib.load(model_path)
        predictions = model.predict(input_data)
        return predictions
    except FileNotFoundError:
        print("Error: Model file not found.")
        return None
