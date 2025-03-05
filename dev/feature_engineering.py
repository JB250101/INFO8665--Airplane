import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from dev_run_v0 import load_data  # Load data from dev_run_v0
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = Flask(__name__)

ENCODERS_DIR = "models/encoder/"
os.makedirs(ENCODERS_DIR, exist_ok=True)  # Ensure encoder directory exists

# Function to apply label encoding and save encoders
# Function to apply label encoding and save encoders
def encode_categorical_features(df, categorical_cols):
    encoders = {}
    for col in categorical_cols:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])  # Ensure categorical values are transformed
        encoders[col] = encoder
        joblib.dump(encoder, os.path.join(ENCODERS_DIR, f"{col}_encoder.pkl"))  # Save encoder
    return df, encoders

@app.route("/feature_engineering", methods=["POST"])
def feature_engineering():
    try:
        data = request.json
        file_name = data.get("file_name")

        if not file_name:
            return jsonify({"status": "Error", "message": "Missing file_name in request."})

        df = load_data(file_name)
        if df is None or df.empty:
            return jsonify({"status": "Error", "message": "Failed to load data or empty file."})

        # Identify categorical columns to encode
        categorical_cols = ['Airline', 'Source', 'Destination','Route', 'Total_Stops', 'Additional_Info']
        df, encoders = encode_categorical_features(df, categorical_cols)

        # Apply Scaling
        scaler = StandardScaler()
        numerical_cols = ['Duration', 'Journey_day', 'Journey_month', 'Dep_Time_hour', 
                          'Dep_Time_minute', 'Arrival_Time_hour', 'Arrival_Time_minute']
        df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

        # Save the scaler
        joblib.dump(scaler, os.path.join(ENCODERS_DIR, "scaler.pkl"))

        # Save the feature-engineered dataset
        processed_file_path = os.path.join("data", "processed_airfare_data.csv")
        df.to_csv(processed_file_path, index=False)

        return jsonify({
            "status": "Success",
            "message": "Feature engineering completed successfully!",
            "encoded_features": list(encoders.keys()),
            "scaled_features": numerical_cols,
            "processed_file": processed_file_path
        })

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(port=5003, debug=True)
