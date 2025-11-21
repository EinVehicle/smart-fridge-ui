# app.py
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# 数据库连接
db = mysql.connector.connect(
    host="localhost",
    user="fridge_user",
    password="password",
    database="smart_fridge"
)

@app.route("/api/fridge_status")
def fridge_status():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fridge_overview")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
