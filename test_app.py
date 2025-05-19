from flask import Flask, request, jsonify, render_template_string
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'clave-segura-para-csrf'  # Requerida para CSRFProtect
csrf = CSRFProtect(app)

# HTML con formulario que hace fetch POST con JSON (sin cookies de sesión)
form_html = """
<!-- Formulario sin protección CSRF solo para uso con API JSON -->
<form id="form" method="post" action="/submit">
  <input name="fullname" id="fullname" />
  <input name="email" id="email" />
  <input name="password" id="password" />
  <input name="confirm_password" id="confirm_password" />
  <button type="submit">Enviar</button>
</form>
<div id="msg"></div>
<script>
document.getElementById('form').onsubmit = async e => {
  e.preventDefault();
  const data = {
    fullname: fullname.value,
    email: email.value,
    password: password.value,
    confirm_password: confirm_password.value
  };
  const res = await fetch('/submit', {
    method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)
  });
  const json = await res.json();
  document.getElementById('msg').innerText = json.message;
}
</script>
"""

@app.route('/')
def home():
    return render_template_string(form_html)

# ❗ CSRF deshabilitado específicamente en este endpoint JSON solo para desarrollo / API externa sin cookies.
@csrf.exempt
@app.route('/submit', methods=['POST'])
def submit():
    d = request.json
    if not d['fullname'].strip():
        return jsonify(status='Error', message='Nombre inválido')
    if '@' not in d['email']:
        return jsonify(status='Error', message='Email inválido')
    if len(d['password']) < 6:
        return jsonify(status='Error', message='Contraseña corta')
    if d['password'] != d['confirm_password']:
        return jsonify(status='Error', message='Contraseñas no coinciden')
    return jsonify(status='OK', message='Registro exitoso')

if __name__ == '__main__':
    app.run()