from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import BadRequest
from validators import (
    validate_not_empty,
    validate_fullname_length,
    validate_email_format,
    validate_password_strength,
    validate_password_common,
    validate_email_case_insensitive,
    validate_long_name,
    validate_long_password,
    validate_trim,
    validate_no_numbers_in_name,
)

def create_app():
    app = Flask(__name__)

    def init_db():
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            fullname TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)""")
        conn.commit()
        conn.close()

    init_db()

    @app.route('/form.html')
    def serve_form():
         return app.send_static_file('form.html')
    
    @app.route('/register', methods=['POST'])
    def register_user():
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return jsonify({"status": "error", "message": "❌ Invalid request format"}), 400

        fullname = data.get("fullname", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        # 🔍 Validaciones usando validators.py
        if not validate_not_empty(fullname, email, password):
            return jsonify({"status": "error", "message": "❌ Missing required fields"}), 400
        if not validate_trim(fullname, email, password):
            return jsonify({"status": "error", "message": "❌ Fields should not start or end with spaces"}), 400
        if not validate_fullname_length(fullname):
            return jsonify({"status": "error", "message": "❌ Full Name must be at least 3 characters"}), 400
        if not validate_long_name(fullname):
            return jsonify({"status": "error", "message": "❌ Full Name is too long"}), 400
        if not validate_no_numbers_in_name(fullname):
            return jsonify({"status": "error", "message": "❌ Name should not contain numbers"}), 400
        if not validate_email_format(email):
            return jsonify({"status": "error", "message": "❌ Invalid email format"}), 400
        if not validate_email_case_insensitive(email):
            return jsonify({"status": "error", "message": "❌ Email should be lowercase only"}), 400
        if not validate_password_strength(password):
            return jsonify({"status": "error", "message": "❌ Password must be 6+ characters and include a special symbol"}), 400
        if not validate_password_common(password):
            return jsonify({"status": "error", "message": "❌ Password is too common"}), 400
        if not validate_long_password(password):
            return jsonify({"status": "error", "message": "❌ Password is too long"}), 400

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                           (fullname, email, hashed_password))
            conn.commit()
            response = {"status": "success", "message": "✅ Registration successful!"}
        except sqlite3.IntegrityError:
            response = {"status": "error", "message": "❌ Email already registered."}

        conn.close()
        return jsonify(response)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)