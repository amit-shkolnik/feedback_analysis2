import os
import io
import config
from config import *

def load_csv(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def load_excel(file_path: str) -> pd.DataFrame:
    """Load data from an Excel file into a DataFrame."""
    return pd.read_excel(file_path)

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the DataFrame to ensure it is in the correct format for analysis.
    
    This may include handling missing values, renaming columns, and converting data types.
    """
    # Example preprocessing steps
    df.dropna(inplace=True)  # Remove missing values
    df.columns = [col.strip().lower() for col in df.columns]  # Clean column names
    return df

def load_file(file_path: str) -> pd.DataFrame:
    """Load data from a file (CSV or Excel) and preprocess it."""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        return df
    elif file_path.endswith('.xlsx'):
        df = load_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
    
    return preprocess_data(df)