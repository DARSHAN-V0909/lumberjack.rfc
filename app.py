from flask import Flask, request, jsonify, session,render_template
import mysql.connector
from mysql.connector import IntegrityError
import hashlib
import secrets
import os
## to install mysql.connector and flask have to install inside venv not globally
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)##creates secret key toencrypt the current session  and sign session cookies securely so client cant tamper

# DB connection function
#put your username pswrd here
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="rmms1",
        password="rmms1!",
        database="inventory_db"
    )
@app.route('/')##this is default landing page of the app
@app.route('/login', methods=['GET'])
def home():
    return render_template('login.html')

@app.route('/register')## directs to register.html
def registerPage():
    return render_template('register.html')
@app.route('/register', methods=['POST'])
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

        db_path = os.path.join(os.path.dirname(__file__), 'db', 'init.sql')
        with open(db_path, 'a') as f:
            escaped_username = username.replace("'", "''")
            f.write(
                f"INSERT INTO users (username, password_hash) VALUES ('{escaped_username}', '{password}');\n"
            )
        
        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError:
        return jsonify({"error": "Username already exists"}), 409

    except Exception as e:
        # Catch-all for any other DB errors
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()

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
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

# ---------- MATERIAL ROUTES ----------

@app.route('/materials', methods=['GET', 'POST'])
def materials():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM raw_materials WHERE user_id = %s", (session['user_id'],))
        materials = cursor.fetchall()
        conn.close()
        return jsonify(materials)

    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        unit = data['unit']
        current_stock = data['current_stock']
        threshold = data['threshold']
        user_id = session['user_id']

        cursor.execute(
            "INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) VALUES (%s, %s, %s, %s, %s)",
            (name, unit, current_stock, threshold, user_id)
        )
        conn.commit()
        conn.close()

        db_path = os.path.join(os.path.dirname(__file__), 'db', 'init.sql')
        with open(db_path, 'a') as f:
            ename = name.replace("'", "''")
            eunit = unit.replace("'", "''")
            f.write(
                f"INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) "
                f"VALUES ('{ename}', '{eunit}', {current_stock}, {threshold}, {user_id});\n"
            )

        return jsonify({"message": "Material added"}), 201

# More routes like /transactions and /stock/status can follow...

@app.errorhandler(404)##flask default page for error 404
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)