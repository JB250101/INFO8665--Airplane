from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load models
model_path = "models/flight_fare_model.pkl"
encoder_airline_path = "models/encoder_airline.pkl"
encoder_source_path = "models/encoder_source.pkl"
encoder_destination_path = "models/encoder_destination.pkl"
scaler_path = "models/scaler.pkl"

# Ensure model exists
if not os.path.exists(model_path):
    raise FileNotFoundError("Trained model not found. Please train the model first.")

# Load the trained model and encoders
model = joblib.load(model_path)
encoder_airline = joblib.load(encoder_airline_path)
encoder_source = joblib.load(encoder_source_path)
encoder_destination = joblib.load(encoder_destination_path)
scaler = joblib.load(scaler_path)

def safe_encode(label, encoder):
    """Safely encode labels, replacing unknowns with 'Unknown'."""
    if label in encoder.classes_:
        return encoder.transform([label])[0]
    else:
        return encoder.transform(["Unknown"])[0]  # Ensure "Unknown" is in training

@app.route("/predict", methods=["POST"])
def predict():
    try:
        json_data = request.get_json()
        processed_data = json_data["processed_data"]  # Use already preprocessed data
        df = pd.DataFrame(processed_data, columns=['Airline', 'Source', 'Destination', 'Journey_day', 'Journey_month'])


        # Select model features
        X = df[['Airline', 'Source', 'Destination', 'Journey_day', 'Journey_month']]
        prediction = model.predict(X)

        return jsonify({"status": "Success", "predicted_price": prediction.tolist()})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(port=5004, debug=True)
