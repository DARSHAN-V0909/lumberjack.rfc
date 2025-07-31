from flask import Flask, request, jsonify, session
import mysql.connector
import hashlib
## to install mysql.connector and flask have to install inside venv not globally
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# DB connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="inventory_db"
    )

# ---------- AUTH ROUTES ----------

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = hashlib.sha256(data['password'].encode()).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}, 201

@app.route('/login', methods=['POST'])
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
        return {"message": "Login successful"}
    return {"error": "Invalid credentials"}, 401

@app.route('/logout')
def logout():
    session.clear()
    return {"message": "Logged out"}

# ---------- MATERIAL ROUTES ----------

@app.route('/materials', methods=['GET', 'POST'])
def materials():
    if 'user_id' not in session:
        return {"error": "Unauthorized"}, 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM raw_materials WHERE user_id = %s", (session['user_id'],))
        materials = cursor.fetchall()
        conn.close()
        return jsonify(materials)

    if request.method == 'POST':
        data = request.get_json()
        cursor.execute(
            "INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) VALUES (%s, %s, %s, %s, %s)",
            (data['name'], data['unit'], data['current_stock'], data['threshold'], session['user_id'])
        )
        conn.commit()
        conn.close()
        return {"message": "Material added"}, 201

# More routes like /transactions and /stock/status can follow...

if __name__ == '__main__':
    app.run(debug=True)