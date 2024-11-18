# utils.py for AI module

import pandas as pd
import json

# Function to load data from CSV
def load_data(file_path):
    """
    Load data from a CSV file into a DataFrame.

    Parameters:
    - file_path: Path to the CSV file

    Returns:
    - data: DataFrame containing the loaded data
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("Error: File not found.")
        return None

# Function to save model predictions as JSON
def save_predictions(predictions, output_path='predictions.json'):
    """
    Save model predictions to a JSON file.

    Parameters:
    - predictions: List or array of prediction results
    - output_path: Path to save the JSON file

    Returns:
    - None
    """
    formatted_results = [{'prediction': round(pred, 2)} for pred in predictions]
    with open(output_path, 'w') as f:
        json.dump(formatted_results, f, indent=4)
    print(f"Predictions saved to {output_path}")
