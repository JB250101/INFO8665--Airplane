import pandas as pd
import os

def load_data(file_name):
    # Define the path relative to the project directory
    data_path = os.path.join('data', file_name)
    
    # Load and return the dataset
    if os.path.exists(data_path):
        print(f"Loading data from {data_path}...")
        return pd.read_excel(data_path)
    else:
        print(f"Error: File {data_path} not found.")
        return None

if __name__ == "__main__":
    # Example of loading the dataset
    df = load_data('Data_Train.xlsx')
    if df is not None:
        print(f"Loaded {len(df)} records from the dataset.")
