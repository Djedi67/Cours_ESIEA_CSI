from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

FLAG = "FLAG{c0mm4nd_1nj3ct10n_r3uss1}"

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Diagnostic reseau</title>
<style>
body { font-family: Arial; background: #1a1a2e; color: #eee; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
.box { background: #16213e; padding: 40px; border-radius: 10px; width: 480px; }
h2 { color: #e94560; text-align: center; }
.sub { color: #666; font-size: 12px; text-align: center; margin-bottom: 20px; }
input[type=text] { width: 100%; padding: 10px; margin: 10px 0; background: #0f3460; border: none; color: #eee; border-radius: 5px; box-sizing: border-box; }
button { width: 100%; padding: 10px; background: #e94560; border: none; color: white; border-radius: 5px; cursor: pointer; font-size: 16px; }
pre { background: #0f3460; padding: 15px; border-radius: 5px; margin-top: 15px; font-size: 12px; white-space: pre-wrap; word-break: break-all; }
</style></head>
<body>
<!-- outil interne de diagnostic - la commande est construite directement depuis le formulaire -->
<div class="box">
  <h2>Diagnostic reseau</h2>
  <p class="sub">Entrez une adresse IP pour effectuer un ping.</p>
  <form method="POST">
    <input type="text" name="host" placeholder="Ex : 8.8.8.8" required>
    <button type="submit">Ping</button>
  </form>
  {% if result %}
  <pre>{{ result }}</pre>
  {% endif %}
</div>
</body></html>
'''

@app.route('/', methods=['GET', 'POST'])
def ping():
    result = ''
    if request.method == 'POST':
        host = request.form.get('host', '')
        try:
            output = subprocess.check_output(
                f"ping -c 1 {host}",
                shell=True,
                stderr=subprocess.STDOUT,
                timeout=5
            ).decode()
            result = output
        except subprocess.TimeoutExpired:
            result = 'Timeout : hote inaccessible.'
        except subprocess.CalledProcessError as e:
            result = e.output.decode()
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
