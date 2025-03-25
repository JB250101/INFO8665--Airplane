from flask import Flask, request, jsonify
import pandas as pd
import joblib
import numpy as np
import os
import logging

app = Flask(__name__)

# ✅ Set up logging
logger = logging.getLogger("InferenceService")
logger.setLevel(logging.INFO)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "inference_service.log")

file_handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

# Define model and encoders directory
MODEL_PATH = "models/flight_fare_model.pkl"
ENCODERS_DIR = "models/encoder/"
SCALER_PATH = os.path.join(ENCODERS_DIR, "scaler.pkl")

# Load the trained model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    logger.info("Loaded trained model from disk.")
else:
    model = None
    logger.warning("Trained model not found.")

# Load scaler
if os.path.exists(SCALER_PATH):
    scaler = joblib.load(SCALER_PATH)
    logger.info("Loaded scaler from disk.")
else:
    scaler = None
    logger.warning("Scaler not found.")

# Load categorical encoders
def load_encoders():
    encoders = {}
    for col in ['Airline', 'Source', 'Destination', 'Route', 'Total_Stops', 'Additional_Info']:
        encoder_path = os.path.join(ENCODERS_DIR, f"{col}_encoder.pkl")
        if os.path.exists(encoder_path):
            encoders[col] = joblib.load(encoder_path)
            logger.info(f"Loaded encoder for column: {col}")
        else:
            logger.warning(f"Encoder for column '{col}' not found.")
    return encoders

encoders = load_encoders()

# Preprocess input data
def preprocess_input(data):
    try:
        df = pd.DataFrame([data])
        logger.info("Received input for prediction.")

        for col, encoder in encoders.items():
            if col in df:
                df[col] = df[col].map(lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1)

        numerical_cols = ['Duration', 'Journey_day', 'Journey_month', 'Dep_Time_hour',
                          'Dep_Time_minute', 'Arrival_Time_hour', 'Arrival_Time_minute']

        if scaler:
            df[numerical_cols] = scaler.transform(df[numerical_cols])

        return df, None
    except Exception as e:
        logger.exception("Error during preprocessing input.")
        return None, str(e)

# API Endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        logger.info("Received prediction request.")

        if not model:
            logger.error("Prediction failed: model not loaded.")
            return jsonify({"status": "Error", "message": "Model not found. Train the model first!"})

        input_data = request.json
        if not input_data:
            logger.warning("No input data provided in request.")
            return jsonify({"status": "Error", "message": "No input data provided!"})

        logger.info(f"Input data: {input_data}")

        processed_input, error = preprocess_input(input_data)
        if error:
            logger.error(f"Preprocessing failed: {error}")
            return jsonify({"status": "Error", "message": error})

        expected_order = model.feature_names_in_
        processed_input = processed_input[expected_order]

        prediction = model.predict(processed_input)
        predicted_price = round(prediction[0], 2)

        logger.info(f"Prediction successful: ₹{predicted_price}")

        return jsonify({
            "status": "Success",
            "message": "Prediction successful!",
            "predicted_price": predicted_price
        })

    except Exception as e:
        logger.exception("Exception during prediction.")
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
