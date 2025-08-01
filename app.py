from flask import Flask, request, jsonify, session,render_template
import mysql.connector
from mysql.connector import IntegrityError
import hashlib
import secrets
import os
## to install mysql.connector and flask have to install inside venv not globally
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)##creates secret key toencrypt the current session  and sign session cookies securely so client cant tamper
#=============implement logout and materials pages next=======================
# DB connection function
#put your username pswrd here this is what connects to the database to send queries
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="rmms1",
        password="rmms1!",
        database="inventory_db"
    )
@app.route('/')##this is default landing page of the app
@app.route('/login', methods=['GET'])# this get method has been specified to not confuse with the other POST method, there are 2 links above this function as this is specified to be the default landing page and should be accesible by the link
def home():
    return render_template('login.html')

@app.route('/register')## directs to register.html
def registerPage():
    return render_template('register.html')
@app.route('/register', methods=['POST'])#when someone registers from the HTMl page a POST request is sent here and this function adds that username/password to the database
def register():
    data = request.get_json()#gets the POST json object from the frontend JS 
    username = data['username']#extracts the username field from the json
    password = hashlib.sha256(data['password'].encode()).hexdigest()#extracts and encodes password to sha256 encryption

    conn = get_connection()#establishes connection with the database
    cursor = conn.cursor()#this signals the start of a query being written now we can write queries to the db
    try:#try catch to handle case where user has tried to register with duplicate username
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password)
        )#tries to execute an insertion query with data that we have extracted from the json
        conn.commit()#commits the query and pushes it to the db immediately, waits for db response

        db_path = os.path.join(os.path.dirname(__file__), 'db', 'init.sql')#absolute path has been used to access the inti_sql file
        with open(db_path, 'a') as f:
            escaped_username = username.replace("'", "''")
            f.write(
                f"INSERT INTO users (username, password_hash) VALUES ('{escaped_username}', '{data['password']}');\n"
            )#passing the actual password here so you can use the profiles
        
        return jsonify({"message": "User registered successfully"}), 201#returns a success request to the front end, it can now render a success message

    except IntegrityError:#handles the edge case where registration form duplicate username occurs
        return jsonify({"error": "Username already exists"}), 409

    except Exception as e:
        # Catch-all for any other DB errors
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()#safely closes the connection in all situations the finally block always runs even if program crashes unexpectedly this allows safe DB closure

@app.route('/login', methods=['POST'])#Handles login request from the frontend, handles authentication from the frontend with DB
def login():
    data = request.get_json()#gets json data from the POST request
    username = data['username']#gets the entered username login data from the json object
    password = hashlib.sha256(data['password'].encode()).hexdigest()#gets the password

    conn = get_connection()#establishes connection with the DB
    cursor = conn.cursor(dictionary=True)#enables us to start writing queries, the dictionary field is True and says that we expect a key value pair
    cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, password))#query to check if user present
    user = cursor.fetchone()#fetches the one entry in case available
    conn.close()#connection between this app and DB is closed

    if user:#if user info was retrieved successfully do this user would be None otherwise
        session['user_id'] = user['id']#sets the session userId to the id field we retrieved from the DB
        return jsonify({"message": "Login successful"})#sends a successful response to the frontend
    return jsonify({"error": "Invalid credentials"}), 401#throws error and should redirect to our custom error 303 HTML page
#TO-DO WORK ON THIS LOGIN PAGE
@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

# ---------- MATERIAL ROUTES ----------
#TO-DO Work on this materials page and add a materials html page
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
    return render_template('404.html'), 404#renders our custom html page in case of error
#mandatory to start the application on run
if __name__ == '__main__':
    app.run(debug=True)