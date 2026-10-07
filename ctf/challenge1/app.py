from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Connexion</title>
<style>
body { font-family: Arial; background: #1a1a2e; color: #eee; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
.box { background: #16213e; padding: 40px; border-radius: 10px; width: 380px; }
h2 { color: #e94560; text-align: center; }
input { width: 100%; padding: 10px; margin: 10px 0; background: #0f3460; border: none; color: #eee; border-radius: 5px; box-sizing: border-box; }
button { width: 100%; padding: 10px; background: #e94560; border: none; color: white; border-radius: 5px; cursor: pointer; font-size: 16px; }
.msg { text-align: center; margin-top: 15px; padding: 10px; border-radius: 5px; }
.success { background: #1a4731; color: #2ecc71; }
.error { background: #4a1a1a; color: #e74c3c; }
</style></head>
<body>
<!-- hint : penser a securiser la requete SQL avant la mise en prod -->
<div class="box">
  <h2>Connexion</h2>
  <form method="POST">
    <input type="text" name="username" placeholder="Nom d utilisateur" required>
    <input type="password" name="password" placeholder="Mot de passe" required>
    <button type="submit">Se connecter</button>
  </form>
  {% if message %}
  <div class="msg {{ css }}">{{ message }}</div>
  {% endif %}
</div>
</body></html>
'''

def get_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'admin', 'motdepasse123')")
    conn.execute("INSERT INTO users VALUES (2, 'user1', 'azerty')")
    conn.execute("CREATE TABLE flags (id INTEGER PRIMARY KEY, flag TEXT)")
    conn.execute("INSERT INTO flags VALUES (1, 'FLAG{SQL_1nj3ct10n_r3uss1e}')")
    conn.commit()
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    css = ''
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        try:
            cursor = db.execute(query)
            user = cursor.fetchone()
            if user:
                secret = db.execute("SELECT flag FROM flags").fetchone()[0]
                message = f'Connexion reussie ! Flag : {secret}'
                css = 'success'
            else:
                message = 'Identifiants incorrects.'
                css = 'error'
        except Exception as e:
            message = f'Erreur : {str(e)}'
            css = 'error'
    return render_template_string(HTML, message=message, css=css)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
