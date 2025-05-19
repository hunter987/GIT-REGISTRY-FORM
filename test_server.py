import pytest
import json
from server import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DEBUG": False,
    })

    # Limpiar base de datos antes de cada test
    import sqlite3
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_success(client):
    data = {
        "fullname": "Juan Perez",
        "email": "juanperez@example.com",
        "password": "P@ssword1"
    }
    response = client.post('/register', json=data)
    assert response.status_code == 200
    resp_json = response.get_json()
    assert resp_json["status"] == "success"
    assert "successful" in resp_json["message"]

def test_register_duplicate_email(client):
    data = {
        "fullname": "Juan Diaz",
        "email": "juanperez@example.com",
        "password": "P@ssword1"
    }
    # Registro inicial
    client.post('/register', json=data)
    # Intento duplicado
    response = client.post('/register', json=data)
    assert response.status_code == 200
    resp_json = response.get_json()
    assert resp_json["status"] == "error"
    assert "already registered" in resp_json["message"]

def test_register_invalid_email_format(client):
    data = {
        "fullname": "Juan Perez",
        "email": "juanperez-at-example.com",  # email inválido
        "password": "P@ssword1"
    }
    response = client.post('/register', json=data)
    assert response.status_code == 400
    resp_json = response.get_json()
    assert resp_json["status"] == "error"
    assert "Invalid email format" in resp_json["message"]

def test_register_missing_fields(client):
    data = {
        "fullname": "",
        "email": "",
        "password": ""
    }
    response = client.post('/register', json=data)
    assert response.status_code == 400
    resp_json = response.get_json()
    assert resp_json["status"] == "error"
    assert "Missing required fields" in resp_json["message"]

def test_register_bad_json(client):
    # Enviar data que no es JSON válido
    response = client.post('/register', data="not json", content_type="application/json")
    assert response.status_code == 400
    resp_json = response.get_json()
    assert resp_json["status"] == "error"
    assert "Invalid request format" in resp_json["message"]