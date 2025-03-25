import os
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

MONITOR_LOG_PATH = "logs/model_monitoring.log"

# ✅ Set up logging
logger = logging.getLogger("MonitoringService")
logger.setLevel(logging.INFO)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "monitoring_service.log")

file_handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

# Write feedback or logs to monitoring log file
def log_monitoring_event(content):
    try:
        with open(MONITOR_LOG_PATH, "a") as log_file:
            log_file.write(content + "\n")
        logger.info(f"Logged monitoring event: {content[:50]}...")  # Log first 50 chars
        return True
    except Exception as e:
        logger.error(f"Failed to log monitoring event: {str(e)}")
        return False

@app.route("/monitor", methods=["POST"])
def monitor_model():
    try:
        data = request.json
        logger.info("Received monitoring event.")

        user_feedback = data.get("feedback", "")
        prediction_value = data.get("prediction", "N/A")

        if not user_feedback:
            logger.warning("Missing 'feedback' field in request.")
            return jsonify({"status": "Error", "message": "Missing feedback field."})

        log_line = f"Prediction: {prediction_value} | Feedback: {user_feedback}"
        success = log_monitoring_event(log_line)

        if not success:
            return jsonify({"status": "Error", "message": "Failed to log monitoring event."})

        logger.info("Monitoring event logged successfully.")
        return jsonify({"status": "Success", "message": "Monitoring event logged."})

    except Exception as e:
        logger.exception("Exception in monitoring service.")
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
