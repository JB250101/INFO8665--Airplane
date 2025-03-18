import streamlit as st
import requests
import pandas as pd

st.write("🔄 Streamlit app started!")  # Debugging Log

# Function to get fare prediction from the inference API
def get_prediction(input_data):
    try:
        st.write("📡 Sending data for prediction...", input_data)  # Debug log
        response = requests.post("http://127.0.0.1:5005/predict", json=input_data)
        st.write(f"🟢 Response Status: {response.status_code}")  # Debug log
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")  # Show error in UI
    return {"status": "Error", "message": "Prediction failed"}

st.title("✈️ Airfare Price Prediction")
st.sidebar.header("Flight Details")

# User Inputs
airline = st.sidebar.text_input("Airline", "IndiGo")
source = st.sidebar.text_input("Source", "Delhi")
destination = st.sidebar.text_input("Destination", "Bangalore")
date_of_journey = st.sidebar.date_input("Date of Journey")
duration = st.sidebar.number_input("Duration (minutes)", min_value=30, max_value=1500, step=10)
total_stops = st.sidebar.selectbox("Total Stops", ["non-stop", "1 stop", "2 stops", "3 stops", "4 stops"])
additional_info = st.sidebar.text_input("Additional Info", "No info")
dep_time_hour = st.sidebar.number_input("Departure Hour", min_value=0, max_value=23, step=1)
dep_time_minute = st.sidebar.number_input("Departure Minute", min_value=0, max_value=59, step=1)
arrival_time_hour = st.sidebar.number_input("Arrival Hour", min_value=0, max_value=23, step=1)
arrival_time_minute = st.sidebar.number_input("Arrival Minute", min_value=0, max_value=59, step=1)

if st.sidebar.button("Predict Fare"):
    input_data = {
        "Airline": airline,
        "Source": source,
        "Destination": destination,
        "Route": f"{source} → {destination}",
        "Total_Stops": total_stops,
        "Additional_Info": additional_info,
        "Duration": duration,
        "Journey_day": date_of_journey.day,
        "Journey_month": date_of_journey.month,
        "Dep_Time_hour": dep_time_hour,
        "Dep_Time_minute": dep_time_minute,
        "Arrival_Time_hour": arrival_time_hour,
        "Arrival_Time_minute": arrival_time_minute
    }
    
    # Step 1: Send input to preprocessing service
    st.write("🔄 Sending input to Preprocessing...")
    preprocess_response = requests.post("http://localhost:5002/preprocess", json={"file_name": "collected_airfare_data.csv"})
    st.write("✅ Preprocessing Done:", preprocess_response.json())

    # Step 2: Send processed data to feature engineering service
    st.write("🔄 Sending data to Feature Engineering...")
    feature_response = requests.post("http://localhost:5003/feature_engineering", json={"file_name": "preprocessed_airfare_data.csv"})
    st.write("✅ Feature Engineering Done:", feature_response.json())

    # Step 3: Train the model (only if necessary)
    st.write("🔄 Training the Model...")
    train_response = requests.post("http://localhost:5004/train")
    st.write("✅ Model Training Done:", train_response.json())

    # Step 4: Send final processed input for prediction
    st.write("📡 Sending data for prediction...")
    predict_response = requests.post("http://localhost:5005/predict", json=input_data)

    if predict_response.status_code == 200:
        result = predict_response.json()
        st.success(f"Predicted Price: ₹{result['predicted_price']}")
    else:
        st.error(f"❌ Prediction Failed: {predict_response.json()}")

st.write("✅ Ready for predictions!")