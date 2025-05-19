from flask import Flask, request, jsonify
import re
import sqlite3

def create_app():
    app = Flask(__name__)

    def init_db():
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    init_db()

    @app.route('/register', methods=['POST'])
    def register():
        if not request.is_json:
            return jsonify(status="error", message="Invalid request format"), 400

        data = request.get_json()

        # Validar estructura mínima (campos obligatorios)
        fullname = data.get('fullname')
        email = data.get('email')
        password = data.get('password')

        # Validar que no sean None ni espacios en blanco
        if not fullname or not fullname.strip() or \
           not email or not email.strip() or \
           not password or not password.strip():
            return jsonify(status="error", message="Missing required fields"), 400

        fullname = fullname.strip()
        email = email.strip()
        password = password.strip()

        # Validar formato email básico
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify(status="error", message="Invalid email format"), 400

        # Validar contraseña:
        # Al menos 6 caracteres, al menos 1 mayúscula, 1 minúscula, 1 número y 1 símbolo especial
        if len(password) < 6 or \
           not re.search(r"[A-Z]", password) or \
           not re.search(r"[a-z]", password) or \
           not re.search(r"[0-9]", password) or \
           not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return jsonify(status="error", message="Invalid password: must be 6+ chars and include uppercase, lowercase, number, and special symbol"), 400

        # Insertar en DB (evitar duplicados por email)
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if cursor.fetchone() is not None:
                return jsonify(status="error", message="Email already registered"), 200

            cursor.execute(
                "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                (fullname, email, password)
            )
            conn.commit()
            return jsonify(status="success", message="Registration successful"), 200

        except Exception as e:
            # Evitar mostrar errores internos al usuario
            return jsonify(status="error", message="Server error"), 500

        finally:
            conn.close()

    return app
