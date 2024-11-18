# preprocess.py for AI module

import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Function to handle missing data
def clean_data(data, strategy='mean'):
    """
    Handle missing values in the dataset.

    Parameters:
    - data: DataFrame to clean
    - strategy: Strategy for filling missing values ('mean', 'median', or 'mode')

    Returns:
    - data: Cleaned DataFrame
    """
    if strategy == 'mean':
        data = data.fillna(data.mean())
    elif strategy == 'median':
        data = data.fillna(data.median())
    elif strategy == 'mode':
        data = data.fillna(data.mode().iloc[0])
    else:
        raise ValueError("Invalid strategy. Use 'mean', 'median', or 'mode'.")
    return data

# Function to scale data
def normalize_data(data, method='standard'):
    """
    Normalize or scale data to improve model performance.

    Parameters:
    - data: DataFrame to be normalized
    - method: Scaling method ('standard' or 'minmax')

    Returns:
    - scaled_data: Scaled DataFrame
    """
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError("Invalid method. Use 'standard' or 'minmax'.")
    
    scaled_data = scaler.fit_transform(data)
    return pd.DataFrame(scaled_data, columns=data.columns)
