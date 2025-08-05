from flask import Blueprint, render_template, request, session, jsonify
import os
from routes.db_utils import get_connection
from mysql.connector import Error

material_bp = Blueprint('material', __name__)

@material_bp.route('/materialAdd')
def materialsAddPage():
    return render_template("materialAdd.html")

@material_bp.route("/materialView")
def materialsViewPage():
    return render_template('materialView.html')

@material_bp.route('/materials', methods=['GET'])#handling get requests
def get_materials():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM raw_materials WHERE user_id = %s", (session['user_id'],))
        materials = cursor.fetchall()
        return jsonify(materials)

    except Error as e:
        print(f"SQL Error: {e}")
        return jsonify({"error": "Failed to fetch materials", "details": str(e)}), 400

    finally:
        conn.close()

@material_bp.route('/materials', methods=['POST'])
def add_material():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        name = data['name']
        unit = data['unit']
        current_stock = data['current_stock']
        threshold = data['threshold']
        user_id = session['user_id']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) "
            "VALUES (%s, %s, %s, %s, %s)",
            (name, unit, current_stock, threshold, user_id)
        )
        conn.commit()

        # Log to init.sql for backup
        db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'init.sql')
        with open(db_path, 'a') as f:
            ename = name.replace("'", "''")
            eunit = unit.replace("'", "''")
            f.write(
                f"INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) "
                f"VALUES ('{ename}', '{eunit}', {current_stock}, {threshold}, {user_id});\n"
            )

        return jsonify({"message": "Material added"}), 201

    except Error as e:
        print(f"SQL Error: {e}")
        return jsonify({"error": "Insertion error", "details": str(e)}), 400

    finally:
        conn.close()
@material_bp.route('/materials', methods=['PUT'])
def update_material():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        material_id = data['material_id']
        quantity = int(data['quantity'])

        conn = get_connection()
        cursor = conn.cursor()

        # # Fetch current stock securely
        # cursor.execute("SELECT current_stock FROM raw_materials WHERE material_id = %s AND user_id = %s",
        #                (material_id, session['user_id']))
        # row = cursor.fetchone()

        # if row is None:
        #     return jsonify({"error": "Material not found"}), 404

        new_stock = data['current_stock'] + int(quantity)

        # Ensure stock doesn't go negative
        if new_stock < 0:
            return jsonify({"error": "Insufficient stock"}), 400
        print('reached')
        # Update stock
        cursor.execute("UPDATE raw_materials SET current_stock = %s WHERE material_id = %s AND user_id = %s",
                       (new_stock, material_id, session['user_id']))

        # Determine type of transaction
        tx_type = "add" if quantity >= 0 else "remove"

        # Log transaction
        cursor.execute(
            "INSERT INTO transactions (material_id, quantity, type, user_id) VALUES (%s, %s, %s, %s)",
            (material_id, abs(quantity), tx_type, session['user_id'])
        )

        conn.commit()

        # Save queries to file for auditing
        db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'init.sql')
        with open(db_path, 'a') as f:
            f.write(f"UPDATE raw_materials SET current_stock = {new_stock} WHERE material_id = {material_id} AND user_id = {session['user_id']};\n")
            f.write(f"INSERT INTO transactions (material_id, quantity, type, user_id) VALUES ({material_id}, {abs(quantity)}, '{tx_type}', {session['user_id']});\n")

        return jsonify({"message": "Material updated"}), 200

    except Error as e:
        print(f"SQL Error: {e}")
        return jsonify({"error": "Update error", "details": str(e)}), 400

    finally:
        conn.close()
@material_bp.route('/materials', methods=['DELETE'])
def delete_material():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        name = data['name']
        material_id=data['material_id']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE material_id=%s and user_id=%s", (material_id, session['user_id']))
        cursor.execute("DELETE FROM raw_materials WHERE name = %s AND user_id = %s", (name, session['user_id']))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Material not found "+name}), 404

        # Audit logging
        db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'init.sql')
        with open(db_path, 'a') as f:
            f.write(f"DELETE FROM transactions WHERE material_id={material_id} and user_id={session['user_id']};\n")
            f.write(f"DELETE FROM raw_materials WHERE name = '{name}' AND user_id = {session['user_id']};\n")
            
        return jsonify({"message": "Material deleted"}), 200

    except Error as e:
        print(f"SQL Error: {e}")
        return jsonify({"error": "Deletion error", "details": str(e)}), 400

    finally:
        conn.close()
@material_bp.route('/transactions',methods=['GET'])
def getTransactions():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT transactions.*,raw_materials.name FROM transactions INNER JOIN raw_materials ON  transactions.material_id = raw_materials.material_id WHERE transactions.user_id = %s", (session['user_id'],))
        transactions = cursor.fetchall()
        return jsonify(transactions)

    except Error as e:
        print(f"SQL Error: {e}")
        return jsonify({"error": "Failed to fetch transactions", "details": str(e)}), 400

    finally:
        conn.close()
@material_bp.route('/stockStatus',methods=['GET'])
def stock_status():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT name,unit,current_stock,threshold FROM raw_materials WHERE user_id = %s AND current_stock<=threshold", (session['user_id'],))
        materials = cursor.fetchall()
        return jsonify(materials)

    except Error as e:
        print(f"SQL Error: {e}")
        return jsonify({"error": "Failed to fetch material data", "details": str(e)}), 400

    finally:
        conn.close()
@material_bp.route('/home')
def homeDirect():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return render_template("dashboard.html", username=session['username'])