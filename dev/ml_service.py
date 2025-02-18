from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/service', methods=['GET'])
def service():
    return jsonify({'status': 'ML service is running successfully!'}), 200

if __name__ == '__main__':
    print("Starting ML Service Manager...")
    app.run(port=5000, debug=True)  # Use port 5000 as a gateway
