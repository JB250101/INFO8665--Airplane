import pandas as pd
import os

def load_data(file_name):
    # Define the path relative to the project directory
    data_path = os.path.join('data', file_name)
    
    # Verify the file exists
    if not os.path.exists(data_path):
        print(f"❌ Error: File {data_path} not found.")
        return None

    # Load the dataset
    print(f"✅ Loading data from {data_path}...")
    df = pd.read_csv(data_path) if file_name.endswith('.csv') else pd.read_excel(data_path)

    # Debugging
    print(f"📊 Loaded data type: {type(df)}")
    print(f"🔍 First 2 rows:\n{df.head(2)}")

    return df  # Ensure this is a DataFrame

if __name__ == "__main__":
    df = load_data('collected_airfare_data.csv')  # Test loading the CSV
    if df is not None:
        print(f"✅ Loaded {len(df)} records.")
