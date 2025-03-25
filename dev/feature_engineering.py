import os
import logging
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from sklearn.preprocessing import LabelEncoder, StandardScaler
from dev_run_v0 import load_data

app = Flask(__name__)

PROCESSED_FILE_PATH = "data/processed_airfare_data.csv"

# ✅ Set up logging
logger = logging.getLogger("FeatureEngineeringService")
logger.setLevel(logging.INFO)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "feature_engineering.log")

file_handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

# Apply label encoding and scaling
def feature_engineer(df):
    try:
        logger.info("Starting feature engineering on DataFrame.")

        # Encode categorical columns
        categorical_cols = ['Airline', 'Source', 'Destination', 'Route', 'Total_Stops', 'Additional_Info']
        encoders = {}

        for col in categorical_cols:
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col])
            encoders[col] = encoder
            joblib.dump(encoder, f"models/encoder/{col}_encoder.pkl")
            logger.info(f"Encoded and saved encoder for column: {col}")

        # Scale numerical columns
        numerical_cols = ['Duration', 'Journey_day', 'Journey_month',
                          'Dep_Time_hour', 'Dep_Time_minute',
                          'Arrival_Time_hour', 'Arrival_Time_minute']
        scaler = StandardScaler()
        df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        joblib.dump(scaler, "models/encoder/scaler.pkl")

        # Save processed data
        df.to_csv(PROCESSED_FILE_PATH, index=False)
        logger.info(f"Feature engineering completed and saved to {PROCESSED_FILE_PATH}")

        return df, categorical_cols, numerical_cols, None

    except Exception as e:
        logger.exception("Exception occurred during feature engineering.")
        return None, [], [], str(e)

# API Endpoint
@app.route("/feature_engineering", methods=["POST"])
def feature_engineering_request():
    try:
        data = request.json
        logger.info("Received request for feature engineering.")
        file_name = data.get("file_name")

        if not file_name:
            logger.warning("Missing file_name in request.")
            return jsonify({"status": "Error", "message": "Missing file_name in request."})

        df = load_data(file_name)
        if df is None or df.empty:
            logger.warning("Failed to load data or file is empty.")
            return jsonify({"status": "Error", "message": "Failed to load data or empty file."})

        processed_df, encoded_cols, scaled_cols, error = feature_engineer(df)
        if error:
            logger.error(f"Feature engineering failed with error: {error}")
            return jsonify({"status": "Error", "message": error})

        logger.info("Returning success response to client.")
        return jsonify({
            "status": "Success",
            "message": "Feature engineering completed successfully!",
            "processed_file": PROCESSED_FILE_PATH,
            "encoded_features": encoded_cols,
            "scaled_features": scaled_cols
        })

    except Exception as e:
        logger.exception("Exception in /feature_engineering route.")
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
