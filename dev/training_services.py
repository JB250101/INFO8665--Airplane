from flask import Flask, request, jsonify
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, confusion_matrix, classification_report
from sklearn.model_selection import RandomizedSearchCV
from sklearn.utils.class_weight import compute_sample_weight
import os
import numpy as np


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

        # Hyperparameter tuning for the best RandomForest model
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        rf_model = RandomForestRegressor(random_state=42)
        rf_search = RandomizedSearchCV(rf_model, param_grid, n_iter=10, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1, random_state=42)
        rf_search.fit(X_train, y_train)

        # Get the best model
        best_rf_model = rf_search.best_estimator_

        # Apply sample weighting
        sample_weights = compute_sample_weight("balanced", y_train)
        best_rf_model.fit(X_train, y_train, sample_weight=sample_weights)
        
        # Evaluate the model
        y_pred = best_rf_model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Convert continuous predictions to categorical labels for classification report & confusion matrix
        y_test_labels = np.digitize(y_test, bins=np.histogram(y_test, bins=5)[1])
        y_pred_labels = np.digitize(y_pred, bins=np.histogram(y_pred, bins=5)[1])
        conf_matrix = confusion_matrix(y_test_labels, y_pred_labels).tolist()
        class_report = classification_report(y_test_labels, y_pred_labels, output_dict=True)
    
        
        # Save the trained model
        model_path = "models/flight_fare_model.pkl"
        joblib.dump(best_rf_model, model_path)
        
        return jsonify({
            "status": "Success",
            "message": "Model trained successfully!",
            "MAE": mae,
            "MSE": mse,
            "R2_Score": r2,
            "Confusion_Matrix": conf_matrix,
            "Classification_Report": class_report
        })
    
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(port=5003, debug=True)
