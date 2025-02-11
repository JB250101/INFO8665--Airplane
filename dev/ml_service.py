from flask import Flask, jsonify

class MLService:
    def __init__(self):
        self.app = Flask(__name__)
        self.create_routes()

    def create_routes(self):
        @self.app.route('/service', methods=['GET'])
        def service():
            # Return a simple HTTP 200 OK response with a success message
            return jsonify({
                'status': 'ML service is running successfully!'
            }), 200

    def start(self, port=5001):
        print(f"Starting ML service on port {port}...")
        self.app.run(port=port)

if __name__ == '__main__':
    service = MLService()
    service.start()
