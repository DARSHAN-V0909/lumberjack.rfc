from flask import Blueprint, render_template, request, jsonify, session
import hashlib
import secrets
import os
from routes.db_utils import get_connection
from mysql.connector import IntegrityError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET'])
def home():
    return render_template('login.html')

@auth_bp.route('/register')
def registerPage():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = hashlib.sha256(data['password'].encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()

        db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'init.sql')
        with open(db_path, 'a') as f:
            escaped_username = username.replace("'", "''")
            f.write(
                f"INSERT INTO users (username, password_hash) VALUES ('{escaped_username}', '{data['password']}');\n"
            )

        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError:
        return jsonify({"error": "Username already exists"}), 409

    finally:
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = hashlib.sha256(data['password'].encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['username'] = username
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', logout=True)