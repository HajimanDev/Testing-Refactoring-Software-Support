import time
import random
from flask import Flask, request, jsonify
from faker import Faker
import jwt
import datetime

app = Flask(__name__)
fake = Faker()

# Конфигурация аутентификации
SECRET_KEY = "your-secret-key-2026"

# Хранилище пользователей
users = {
    "user1": {"password": "pass123", "role": "reader"},
    "author1": {"password": "pass123", "role": "author"}
}

# Хранилище постов в памяти
posts = [
    {"id": 1, "title": "Первый пост", "content": "Содержимое первого поста"},
    {"id": 2, "title": "Второй пост", "content": "Содержимое второго поста"},
]

@app.route('/')
def index():
    time.sleep(random.uniform(0.01, 0.05))
    return jsonify({"message": "Добро пожаловать в тестовый блог!"})

@app.route('/posts', methods=['GET'])
def get_posts():
    time.sleep(random.uniform(0.05, 0.1))
    return jsonify(posts)

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    time.sleep(random.uniform(0.02, 0.07))
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return jsonify(post)
    return jsonify({"error": "Post not found"}), 404

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    time.sleep(random.uniform(0.1, 0.3))
    new_id = len(posts) + 1
    post = {"id": new_id, "title": data.get("title"), "content": data.get("content")}
    posts.append(post)
    return jsonify(post), 201

# ========== ЭНДПОИНТЫ АУТЕНТИФИКАЦИИ ==========
@app.route('/login', methods=['POST'])
def login():
    """Эндпоинт для аутентификации пользователя"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username]['password'] == password:
        token = jwt.encode({
            'username': username,
            'role': users[username]['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            "token": token,
            "role": users[username]['role']
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
def protected():
    """Защищенный эндпоинт, требующий JWT токен"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({"error": "No token provided"}), 401
    
    try:
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        return jsonify({
            "message": f"Welcome {payload['username']}!",
            "role": payload['role']
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)