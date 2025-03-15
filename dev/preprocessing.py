import os
import pandas as pd
from flask import Flask, request, jsonify
from dev_run_v0 import load_data  # Load data function

app = Flask(__name__)

PROCESSED_FILE_PATH = "data/preprocessed_airfare_data.csv"

# Function to preprocess data
def preprocess_data(df):
    try:
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

        return df, None
    except Exception as e:
        return None, str(e)

# Flask API Endpoint
@app.route("/preprocess", methods=["POST"])
def preprocess_request():
    try:
        data = request.json
        file_name = data.get("file_name")

        if not file_name:
            return jsonify({"status": "Error", "message": "Missing file_name in request."})

        df = load_data(file_name)
        if df is None or df.empty:
            return jsonify({"status": "Error", "message": "Failed to load data or empty file."})

        # Preprocess Data
        preprocessed_df, error = preprocess_data(df)
        if error:
            return jsonify({"status": "Error", "message": error})

        return jsonify({
            "status": "Success",
            "message": "Data preprocessed successfully!",
            "processed_file": PROCESSED_FILE_PATH
        })

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
