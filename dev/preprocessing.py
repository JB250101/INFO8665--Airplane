import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import numpy as np

# Load the training dataset
df_train = pd.read_excel("data/Data_Train.xlsx")

# Ensure "Unknown" is included in categories
df_train['Airline'] = df_train['Airline'].astype(str)
df_train['Source'] = df_train['Source'].astype(str)
df_train['Destination'] = df_train['Destination'].astype(str)

# ✅ Fix: Use pd.concat() instead of df.append()
df_train = pd.concat([df_train, pd.DataFrame([{'Airline': "Unknown", 'Source': "Unknown", 'Destination': "Unknown"}])], ignore_index=True)

# Fit Label Encoders
encoder_airline = LabelEncoder()
encoder_source = LabelEncoder()
encoder_destination = LabelEncoder()

encoder_airline.fit(df_train['Airline'])
encoder_source.fit(df_train['Source'])
encoder_destination.fit(df_train['Destination'])

# Save encoders
joblib.dump(encoder_airline, "models/encoder_airline.pkl")
joblib.dump(encoder_source, "models/encoder_source.pkl")
joblib.dump(encoder_destination, "models/encoder_destination.pkl")

# ✅ Fix: Convert encoding results into a DataFrame before assignment
df_encoded = pd.DataFrame({
    'Airline': encoder_airline.transform(df_train['Airline']),
    'Source': encoder_source.transform(df_train['Source']),
    'Destination': encoder_destination.transform(df_train['Destination'])
})

# Fit Scaler
scaler = StandardScaler()
scaler.fit(df_encoded)  # ✅ Train scaler on encoded values

joblib.dump(scaler, "models/scaler.pkl")

def safe_encode(label, encoder):
    """Safely encode labels, replacing unknowns with 'Unknown'."""
    if label in encoder.classes_:
        return encoder.transform([label])[0]
    else:
        return encoder.transform(["Unknown"])[0]  # Now "Unknown" is always present

def preprocess_data(input_data):
    """Preprocess new input data using pre-trained encoders & scalers."""
    try:
        df = pd.DataFrame([input_data])

        # Convert Date
        df['Journey_day'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.day
        df['Journey_month'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True).dt.month

        # Load encoders
        encoder_airline = joblib.load("models/encoder_airline.pkl")
        encoder_source = joblib.load("models/encoder_source.pkl")
        encoder_destination = joblib.load("models/encoder_destination.pkl")

        # Encode safely
        df['Airline'] = safe_encode(df['Airline'][0], encoder_airline)
        df['Source'] = safe_encode(df['Source'][0], encoder_source)
        df['Destination'] = safe_encode(df['Destination'][0], encoder_destination)

        # Load scaler
        scaler = joblib.load("models/scaler.pkl")
        scaled_features = scaler.transform(df[['Airline', 'Source', 'Destination']])
        # ✅ Ensure we return all 5 required features (Encoded + Scaled + Journey_day + Journey_month)
        processed_data = scaled_features.tolist()[0] + [int(df['Journey_day'][0]), int(df['Journey_month'][0])]

        return {
            "status": "Success",
            "processed_data": [processed_data]  # Ensure it's a list inside a list
        }
    
    except Exception as e:
        return {"status": "Error", "message": str(e)}
