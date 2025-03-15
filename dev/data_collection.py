from flask import Flask, request, jsonify
import pandas as pd
import os
from dev_run_v0 import load_data  # Use existing load_data function

app = Flask(__name__)

# **Preprocessing Function**
def preprocess_data(df):
    try:
        # ✅ Convert dictionary to DataFrame if necessary
        if isinstance(df, dict):
            df = pd.DataFrame.from_dict(df)

        # ✅ Ensure we got a valid DataFrame
        if not isinstance(df, pd.DataFrame):
            return None, "❌ Expected a Pandas DataFrame but got a different type."

        # **Drop missing values**
        df = df.dropna().reset_index(drop=True)

        # **Extract Date Features**
        if 'Date_of_Journey' in df.columns:
            df['Journey_day'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.day
            df['Journey_month'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.month
            df.drop(columns=['Date_of_Journey'], inplace=True)

        return df, None
    except Exception as e:
        return None, str(e)

# **Flask API Endpoint**
@app.route("/preprocess", methods=["POST"])
def preprocess_request():
    try:
        request_data = request.get_json()
        file_name = request_data.get("file_name")  # Get filename from request

        if not file_name:
            return jsonify({"status": "Error", "message": "Missing 'file_name' in request."})

        # ✅ Load Data
        df = load_data(file_name)

        # ✅ Convert dictionary to DataFrame if necessary
        if isinstance(df, dict):
            df = pd.DataFrame.from_dict(df)

        # ✅ Ensure it's a DataFrame
        if not isinstance(df, pd.DataFrame):
            return jsonify({"status": "Error", "message": f"Expected a DataFrame, but got {type(df)} instead."})

        # ✅ Preprocess Data
        preprocessed_df, error = preprocess_data(df)
        if error:
            return jsonify({"status": "Error", "message": error})

        return jsonify({
            "status": "Success",
            "message": "Data preprocessed successfully!",
            "data_preview": preprocessed_df.head(5).to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
