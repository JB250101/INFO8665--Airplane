import os
import logging
import streamlit as st
import requests
import pandas as pd

# ✅ Set up logging
logger = logging.getLogger("StreamlitDashboard")
logger.setLevel(logging.INFO)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "streamlit_dashboard.log")

file_handler = logging.FileHandler(log_path, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

# ✅ Streamlit GUI
st.set_page_config(page_title="Airfare Price Prediction", layout="centered")
st.title("✈️ Airfare Price Prediction")

# Input form
st.sidebar.header("Flight Details")
airline = st.sidebar.selectbox("Airline", ["IndiGo", "Air India", "SpiceJet"])
source = st.sidebar.selectbox("Source", ["Delhi", "Mumbai", "Bangalore", "Cochin"])
destination = st.sidebar.selectbox("Destination", ["Delhi", "Mumbai", "Bangalore", "Cochin"])
date_of_journey = st.sidebar.date_input("Date of Journey")
duration = st.sidebar.number_input("Duration (minutes)", min_value=0)

total_stops = st.sidebar.selectbox("Total Stops", ["non-stop", "1 stop", "2 stops"])
additional_info = st.sidebar.selectbox("Additional Info", ["No info", "In-flight meal included"])

dep_time_hour = st.sidebar.number_input("Departure Hour", min_value=0, max_value=23)
dep_time_minute = st.sidebar.number_input("Departure Minute", min_value=0, max_value=59)
arrival_time_hour = st.sidebar.number_input("Arrival Hour", min_value=0, max_value=23)
arrival_time_minute = st.sidebar.number_input("Arrival Minute", min_value=0, max_value=59)

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

    try:
        st.write("🔄 Sending input to Preprocessing...")
        logger.info("Calling preprocessing service...")
        pre_res = requests.post("http://localhost:5002/preprocess", json={"file_name": "collected_airfare_data.csv"})
        st.success(pre_res.json())

        st.write("🔄 Sending data to Feature Engineering...")
        logger.info("Calling feature engineering service...")
        fe_res = requests.post("http://localhost:5003/feature_engineering", json={"file_name": "preprocessed_airfare_data.csv"})
        st.success(fe_res.json())

        st.write("🔄 Training the Model...")
        logger.info("Calling training service...")
        train_res = requests.post("http://localhost:5004/train")
        st.success(train_res.json())

        st.write("📡 Sending data for prediction...")
        logger.info(f"Sending input to prediction service: {input_data}")
        pred_res = requests.post("http://localhost:5005/predict", json=input_data)

        if pred_res.status_code == 200:
            result = pred_res.json()
            logger.info(f"Prediction successful: ₹{result['predicted_price']}")
            st.success(f"Predicted Price: ₹{result['predicted_price']}")
        else:
            logger.warning("Prediction request failed.")
            st.error("Prediction failed. Please check inputs or backend services.")

    except Exception as e:
        logger.exception("Error during prediction process.")
        st.error(f"❌ Error: {str(e)}")
