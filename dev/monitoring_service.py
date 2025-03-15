from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Define file to store logs
LOG_FILE = "data/inference_logs.csv"
os.makedirs("data", exist_ok=True)

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["Airline", "Source", "Destination", "Route", "Duration", "Total_Stops",
                          "Additional_Info", "Journey_day", "Journey_month", "Dep_Time_hour", 
                          "Dep_Time_minute", "Arrival_Time_hour", "Arrival_Time_minute", 
                          "Predicted_Price", "Actual_Price", "User_Feedback"]
                 ).to_csv(LOG_FILE, index=False)

# Store Inference Logs
@app.route("/log_prediction", methods=["POST"])
def log_prediction():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "Error", "message": "No data received!"})

        df = pd.read_csv(LOG_FILE)

        # Append new prediction to log
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(LOG_FILE, index=False)

        return jsonify({"status": "Success", "message": "Prediction logged successfully!"})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

# Submit Feedback for a Prediction
@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    try:
        feedback_data = request.json
        prediction_id = feedback_data.get("id")
        feedback = feedback_data.get("feedback")

        df = pd.read_csv(LOG_FILE)
        if prediction_id >= len(df):
            return jsonify({"status": "Error", "message": "Invalid prediction ID!"})

        # Update feedback
        df.at[prediction_id, "User_Feedback"] = feedback
        df.to_csv(LOG_FILE, index=False)

        return jsonify({"status": "Success", "message": "Feedback submitted successfully!"})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

# Retrieve Logged Predictions
@app.route("/get_logs", methods=["GET"])
def get_logs():
    try:
        df = pd.read_csv(LOG_FILE)
        return jsonify({"status": "Success", "logs": df.to_dict(orient="records")})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
