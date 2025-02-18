from flask import Flask, request, jsonify
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import os

app = Flask(__name__)

# Ensure the models directory exists
os.makedirs("models", exist_ok=True)

# Load data function
def load_data():
    df = pd.read_excel("data/Data_Train.xlsx")
    df = df.dropna()  # Remove missing values
    
    # Feature Engineering
    df['Journey_day'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.day
    df['Journey_month'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.month
    df.drop(columns=['Date_of_Journey', 'Route', 'Dep_Time', 'Arrival_Time'], inplace=True, errors='ignore')
    
    # Load Encoders
    encoder_airline = joblib.load("models/encoder_airline.pkl")
    encoder_source = joblib.load("models/encoder_source.pkl")
    encoder_destination = joblib.load("models/encoder_destination.pkl")
    scaler = joblib.load("models/scaler.pkl")
    
    # Encode categorical variables
    df['Airline'] = df['Airline'].map(lambda x: encoder_airline.transform([x])[0] if x in encoder_airline.classes_ else encoder_airline.transform(["Unknown"])[0])
    df['Source'] = df['Source'].map(lambda x: encoder_source.transform([x])[0] if x in encoder_source.classes_ else encoder_source.transform(["Unknown"])[0])
    df['Destination'] = df['Destination'].map(lambda x: encoder_destination.transform([x])[0] if x in encoder_destination.classes_ else encoder_destination.transform(["Unknown"])[0])
    
    # Scaling
    scaled_features = scaler.transform(df[['Airline', 'Source', 'Destination']])
    df[['Airline', 'Source', 'Destination']] = scaled_features
    
    # Define target variable
    X = df[['Airline', 'Source', 'Destination', 'Journey_day', 'Journey_month']]
    y = df['Price']
    return X, y

@app.route("/train", methods=["POST"])
def train_model():
    try:
        X, y = load_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        
        # Save the trained model
        model_path = "models/flight_fare_model.pkl"
        joblib.dump(model, model_path)
        
        return jsonify({"status": "Success", "message": "Model trained successfully!", "MAE": mae})
    
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(port=5003, debug=True)
