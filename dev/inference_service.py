from flask import Flask, request, jsonify
import pandas as pd
import joblib
import numpy as np
import os

app = Flask(__name__)

# Define model and encoders directory
MODEL_PATH = "models/flight_fare_model.pkl"
ENCODERS_DIR = "models/encoder/"
SCALER_PATH = os.path.join(ENCODERS_DIR, "scaler.pkl")

# Load the trained model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

# Load scaler
if os.path.exists(SCALER_PATH):
    scaler = joblib.load(SCALER_PATH)
else:
    scaler = None

# Load categorical encoders
def load_encoders():
    encoders = {}
    for col in ['Airline', 'Source', 'Destination', 'Route', 'Total_Stops', 'Additional_Info']:
        encoder_path = os.path.join(ENCODERS_DIR, f"{col}_encoder.pkl")
        if os.path.exists(encoder_path):
            encoders[col] = joblib.load(encoder_path)
    return encoders

encoders = load_encoders()

# Function to preprocess input data
def preprocess_input(data):
    try:
        df = pd.DataFrame([data])  # Convert input JSON to DataFrame

        # Apply categorical encoding
        for col, encoder in encoders.items():
            if col in df:
                df[col] = df[col].map(lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1)

        # Apply scaling
        numerical_cols = ['Duration', 'Journey_day', 'Journey_month', 'Dep_Time_hour', 
                          'Dep_Time_minute', 'Arrival_Time_hour', 'Arrival_Time_minute']
        
        if scaler:
            df[numerical_cols] = scaler.transform(df[numerical_cols])

        return df, None
    except Exception as e:
        return None, str(e)

# API Endpoint for inference
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not model:
            return jsonify({"status": "Error", "message": "Model not found. Train the model first!"})

        # Get input data
        input_data = request.json
        if not input_data:
            return jsonify({"status": "Error", "message": "No input data provided!"})

        # Preprocess input
        processed_input, error = preprocess_input(input_data)
        if error:
            return jsonify({"status": "Error", "message": error})

        # Predict
        prediction = model.predict(processed_input)
        predicted_price = round(prediction[0], 2)

        return jsonify({
            "status": "Success",
            "message": "Prediction successful!",
            "predicted_price": predicted_price
        })

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(port=5005, debug=True)
