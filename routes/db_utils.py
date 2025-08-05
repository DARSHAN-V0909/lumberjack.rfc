import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="rmms1",
        password="rmms1!",
        database="inventory_db"
    )
