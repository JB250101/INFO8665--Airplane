import os
import logging
import pandas as pd
import joblib
import numpy as np
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, confusion_matrix, classification_report
from sklearn.utils.class_weight import compute_sample_weight

app = Flask(__name__)

# ✅ Set up logging
logger = logging.getLogger("TrainingService")
logger.setLevel(logging.INFO)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "training_services.log")

file_handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

# Load saved encoders
def load_encoders():
    encoders = {}
    encoder_dir = "models/encoder"
    for col in ['Airline', 'Source', 'Destination', 'Route', 'Total_Stops', 'Additional_Info']:
        encoder_path = os.path.join(encoder_dir, f"{col}_encoder.pkl")
        if os.path.exists(encoder_path):
            encoders[col] = joblib.load(encoder_path)
    return encoders

# Apply encoders to dataset (handling unseen values)
def apply_encoding(df, encoders):
    for col, encoder in encoders.items():
        if col in df:
            df[col] = df[col].apply(lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1)
    return df

# Load preprocessed data & apply encoding/scaling
def load_data():
    processed_data_path = "data/processed_airfare_data.csv"
    if not os.path.exists(processed_data_path):
        return None, "Preprocessed data not found. Run feature_engineering first!"
    df = pd.read_csv(processed_data_path)

    encoders = load_encoders()
    df = apply_encoding(df, encoders)

    X = df.drop(columns=['Price'])
    y = df['Price']
    return X, y

@app.route("/train", methods=["POST"])
def train_model():
    try:
        logger.info("Training request received.")
        X, y = load_data()
        if X is None:
            logger.warning("Training aborted: preprocessed data not found.")
            return jsonify({"status": "Error", "message": y})

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = joblib.load("models/encoder/scaler.pkl")
        numerical_cols = ['Duration', 'Journey_day', 'Journey_month',
                          'Dep_Time_hour', 'Dep_Time_minute',
                          'Arrival_Time_hour', 'Arrival_Time_minute']

        X_train[numerical_cols] = scaler.transform(X_train[numerical_cols])
        X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

        logger.info("Training RandomForest model with hyperparameter tuning.")

        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        rf_model = RandomForestRegressor(random_state=42)
        rf_search = RandomizedSearchCV(rf_model, param_grid, n_iter=10, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1, random_state=42)
        rf_search.fit(X_train, y_train)

        best_rf_model = rf_search.best_estimator_

        sample_weights = compute_sample_weight("balanced", y_train)
        best_rf_model.fit(X_train, y_train, sample_weight=sample_weights)

        y_pred = best_rf_model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        logger.info(f"Training complete. MAE: {mae:.2f}, R2: {r2:.2f}")

        y_test_labels = np.digitize(y_test, bins=np.histogram(y_test, bins=5)[1])
        y_pred_labels = np.digitize(y_pred, bins=np.histogram(y_pred, bins=5)[1])
        conf_matrix = confusion_matrix(y_test_labels, y_pred_labels).tolist()
        class_report = classification_report(y_test_labels, y_pred_labels, output_dict=True)

        model_path = "models/flight_fare_model.pkl"
        joblib.dump(best_rf_model, model_path)
        logger.info("Trained model saved successfully.")

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
        logger.exception("Exception during model training.")
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
