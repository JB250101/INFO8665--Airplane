from flask import Flask, request, jsonify
import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dev.preprocessing import preprocess_data

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "Data Preprocessing Service is running!"})

@app.route('/preprocess', methods=['POST'])
def preprocess():
    try:
        json_data = request.get_json()
        processed_data = preprocess_data(json_data)
        return jsonify(processed_data)
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
