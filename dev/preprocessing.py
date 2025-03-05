from flask import Flask, request, jsonify
import pandas as pd
import os
from dev_run_v0 import load_data  # Importing the correct function

app = Flask(__name__)

def preprocess_data(df):
    try:
        if not isinstance(df, pd.DataFrame):
            return None, "Error: Expected a Pandas DataFrame but got a different type."

        df = df.dropna().reset_index(drop=True)  # Ensure df is not a dictionary
        
        # Feature Engineering
        df['Journey_day'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.day
        df['Journey_month'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.month
        df.drop(columns=['Date_of_Journey'], inplace=True)

        return df, None  # Return DataFrame and no error
    except Exception as e:
        return None, str(e)

@app.route("/preprocess", methods=["POST"])
def preprocess_request():
    try:
        request_data = request.get_json()
        file_name = request_data.get("file_name", "collected_airfare_data.csv")  # Default file

        # Load Data using `load_data()`
        df = load_data(file_name)
        
        if df is None:
            return jsonify({"status": "Error", "message": "Failed to load data."})

        # Preprocess Data
        preprocessed_df, error = preprocess_data(df)
        if error:
            return jsonify({"status": "Error", "message": error})

        # Save the preprocessed data
        preprocessed_file = os.path.join("data", "preprocessed_airfare_data.csv")
        preprocessed_df.to_csv(preprocessed_file, index=False)

        return jsonify({
            "status": "Success",
            "message": "Data preprocessed successfully!",
            "saved_file": preprocessed_file,
            "data_preview": preprocessed_df.head(5).to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(port=5003, debug=True)
