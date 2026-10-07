from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

FLAG = "FLAG{upl04d_m4lv3ill4nt_r3uss1}"

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Partage de fichiers</title>
<style>
body { font-family: Arial; background: #1a1a2e; color: #eee; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
.box { background: #16213e; padding: 40px; border-radius: 10px; width: 420px; }
h2 { color: #e94560; text-align: center; }
.sub { color: #666; font-size: 12px; text-align: center; margin-bottom: 20px; }
input[type=file] { width: 100%; padding: 10px; margin: 10px 0; background: #0f3460; border: none; color: #eee; border-radius: 5px; box-sizing: border-box; }
button { width: 100%; padding: 10px; background: #e94560; border: none; color: white; border-radius: 5px; cursor: pointer; font-size: 16px; }
.msg { text-align: center; margin-top: 15px; padding: 10px; border-radius: 5px; }
.success { background: #1a4731; color: #2ecc71; }
.error { background: #4a1a1a; color: #e74c3c; }
.files { margin-top: 20px; background: #0f3460; padding: 10px; border-radius: 5px; font-size: 13px; }
.files a { color: #e94560; text-decoration: none; display: block; padding: 3px 0; }
</style></head>
<body>
<!-- verification du type de fichier uniquement cote client - ne pas oublier de valider cote serveur -->
<div class="box">
  <h2>Partage de fichiers</h2>
  <p class="sub">Envoyez vos images ici. Formats acceptes : jpg, png, gif.</p>
  <form method="POST" enctype="multipart/form-data">
    <input type="file" name="file" accept=".jpg,.png,.gif" required>
    <button type="submit">Envoyer</button>
  </form>
  {% if message %}
  <div class="msg {{ css }}">{{ message }}</div>
  {% endif %}
  {% if files %}
  <div class="files">
    <strong>Fichiers envoyes :</strong><br>
    {% for f in files %}
    <a href="/uploads/{{ f }}">{{ f }}</a>
    {% endfor %}
  </div>
  {% endif %}
</div>
</body></html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload():
    message = ''
    css = ''
    files = os.listdir(UPLOAD_FOLDER)
    if request.method == 'POST':
        f = request.files.get('file')
        if f and f.filename:
            filename = f.filename
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            message = f'Fichier {filename} envoye avec succes.'
            css = 'success'
            files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, message=message, css=css, files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return 'Fichier introuvable.', 404
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read()
    if 'FLAG_REQUEST' in content:
        return f'<pre style="background:#1a1a2e;color:#2ecc71;padding:20px;">Execution du fichier...\n\nResultat : {FLAG}</pre>'
    return f'<pre style="background:#1a1a2e;color:#eee;padding:20px;">{content}</pre>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
