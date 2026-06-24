from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/greet', methods=['GET'])
def greet():
    response = requests.get('http://service_a:5000/hello')
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)