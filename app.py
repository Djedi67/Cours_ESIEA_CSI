from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# Vulnérabilité 1 : injection SQL volontaire
@app.route("/user")
def get_user():
    username = request.args.get("name", "")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    return str(cursor.fetchall())

# Vulnérabilité 2 : exécution de commande volontaire
@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    result = os.popen("ping -c 1 " + host).read()
    return result

@app.route("/")
def home():
    return "TP DevSecOps - Application de demonstration"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
