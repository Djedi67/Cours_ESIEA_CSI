from flask import Flask, request
import sqlite3
import subprocess

app = Flask(__name__)

@app.route("/user")
def get_user():
    username = request.args.get("name", "")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = ?"
    cursor.execute(query, (username,))
    return str(cursor.fetchall())

@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True
    ).stdout
    return result

@app.route("/")
def home():
    return "TP DevSecOps - Application de demonstration"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
