import os
import logging
import pandas as pd
from flask import Flask, request, jsonify
from dev_run_v0 import load_data  # Load data function

app = Flask(__name__)

# ✅ Set up logging
logger = logging.getLogger("PreprocessingService")
logger.setLevel(logging.INFO)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "preprocessing.log")

file_handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

PROCESSED_FILE_PATH = "data/preprocessed_airfare_data.csv"

# Function to preprocess data
def preprocess_data(df):
    try:
        logger.info("Starting preprocessing on DataFrame")

        # Drop missing values
        df = df.dropna().reset_index(drop=True)

        # Extract Date Features
        df['Journey_day'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.day
        df['Journey_month'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.month
        df.drop(columns=['Date_of_Journey'], inplace=True)

        # Convert Duration to Minutes
        def convert_duration(duration):
            parts = duration.split()
            hours, minutes = 0, 0
            if 'h' in parts[0]:
                hours = int(parts[0].replace('h', ''))
                if len(parts) > 1:
                    minutes = int(parts[1].replace('m', ''))
            else:
                minutes = int(parts[0].replace('m', ''))
            return hours * 60 + minutes

        df['Duration'] = df['Duration'].apply(convert_duration)

        # Convert Total Stops to Numerical
        df['Total_Stops'] = df['Total_Stops'].replace({
            'non-stop': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3, '4 stops': 4
        })

        # Extract Hour and Minute from Departure and Arrival Time
        df['Dep_Time_hour'] = pd.to_datetime(df['Dep_Time']).dt.hour
        df['Dep_Time_minute'] = pd.to_datetime(df['Dep_Time']).dt.minute
        df['Arrival_Time_hour'] = pd.to_datetime(df['Arrival_Time']).dt.hour
        df['Arrival_Time_minute'] = pd.to_datetime(df['Arrival_Time']).dt.minute
        df.drop(columns=['Dep_Time', 'Arrival_Time'], inplace=True)

        # Save the preprocessed data
        df.to_csv(PROCESSED_FILE_PATH, index=False)

        logger.info(f"Preprocessing completed and saved to {PROCESSED_FILE_PATH}")
        return df, None
    except Exception as e:
        logger.exception("Exception occurred during preprocessing.")
        return None, str(e)

# Flask API Endpoint
@app.route("/preprocess", methods=["POST"])
def preprocess_request():
    try:
        data = request.json
        logger.info("Received request for preprocessing.")
        file_name = data.get("file_name")

        if not file_name:
            logger.warning("Missing file_name in request.")
            return jsonify({"status": "Error", "message": "Missing file_name in request."})

        logger.info(f"Attempting to load file: {file_name}")
        df = load_data(file_name)
        if df is None or df.empty:
            logger.warning("Failed to load data or file is empty.")
            return jsonify({"status": "Error", "message": "Failed to load data or empty file."})

        # Preprocess Data
        preprocessed_df, error = preprocess_data(df)
        if error:
            logger.error(f"Preprocessing failed with error: {error}")
            return jsonify({"status": "Error", "message": error})

        logger.info("Returning success response to client.")
        return jsonify({
            "status": "Success",
            "message": "Data preprocessed successfully!",
            "processed_file": PROCESSED_FILE_PATH
        })

    except Exception as e:
        logger.exception("Exception in /preprocess route.")
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
