from flask import Flask, request, jsonify
import pandas as pd
import os
import logging
from dev_run_v0 import load_data  # Use existing load_data function

app = Flask(__name__)

# ✅ Set up logging
logger = logging.getLogger("DataCollectionService")
logger.setLevel(logging.INFO)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "data_collection.log")

file_handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

# ✅ Preprocessing Function
def preprocess_data(df):
    try:
        logger.info("Starting data preprocessing...")

        if isinstance(df, dict):
            df = pd.DataFrame.from_dict(df)
            logger.info("Converted dictionary input to DataFrame.")

        if not isinstance(df, pd.DataFrame):
            logger.warning("Input is not a DataFrame.")
            return None, "Expected a Pandas DataFrame but got a different type."

        df = df.dropna().reset_index(drop=True)
        logger.info("Dropped missing values.")

        if 'Date_of_Journey' in df.columns:
            df['Journey_day'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.day
            df['Journey_month'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.month
            df.drop(columns=['Date_of_Journey'], inplace=True)
            logger.info("Extracted date features from 'Date_of_Journey'.")

        logger.info("Preprocessing completed successfully.")
        return df, None
    except Exception as e:
        logger.exception("Error occurred during preprocessing.")
        return None, str(e)

# ✅ Flask API Endpoint
@app.route("/preprocess", methods=["POST"])
def preprocess_request():
    try:
        logger.info("Received request for preprocessing.")
        request_data = request.get_json()
        file_name = request_data.get("file_name")

        if not file_name:
            logger.warning("Missing 'file_name' in request.")
            return jsonify({"status": "Error", "message": "Missing 'file_name' in request."})

        logger.info(f"Loading data from file: {file_name}")
        df = load_data(file_name)

        if isinstance(df, dict):
            df = pd.DataFrame.from_dict(df)
            logger.info("Converted loaded dictionary to DataFrame.")

        if not isinstance(df, pd.DataFrame):
            logger.warning(f"Invalid data format: {type(df)}")
            return jsonify({"status": "Error", "message": f"Expected a DataFrame, but got {type(df)} instead."})

        preprocessed_df, error = preprocess_data(df)
        if error:
            logger.error(f"Preprocessing failed: {error}")
            return jsonify({"status": "Error", "message": error})

        logger.info("Returning success response with data preview.")
        return jsonify({
            "status": "Success",
            "message": "Data preprocessed successfully!",
            "data_preview": preprocessed_df.head(5).to_dict(orient="records")
        })

    except Exception as e:
        logger.exception("Unexpected exception in /preprocess route.")
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
