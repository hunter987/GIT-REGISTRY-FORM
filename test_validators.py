import pytest
from server import create_app  # Import the function to create the Flask app
import validators
import json
import secrets
@pytest.fixture
def client():
    # Create the app instance using the create_app function
    app = create_app()
    with app.test_client() as client:
        yield client

def test_register_user_success(client):
    # Usar secrets para generar un número aleatorio seguro
    email = f"john.doe{secrets.randbelow(9000) + 1000}@example.com"  # Evita duplicados
    response = client.post('/register',
                           data=json.dumps({
                               'fullname': 'John Doe',
                               'email': email,
                               'password': 'Secure123!'
                           }),
                           content_type='application/json')

    assert response.status_code == 200
    json_response = response.get_json()
    print(json_response)  # para depurar si vuelve a fallar
    assert json_response['status'] == 'success'

# Test to check for missing fields in registration
def test_register_user_missing_fields(client):
    response = client.post('/register',
                           data=json.dumps({
                               'fullname': 'John Doe',
                               'email': ''  # Missing email
                           }),
                           content_type='application/json')

    assert response.status_code == 400
    json_response = response.get_json()
    assert json_response['status'] == 'error'
    assert json_response['message'] == '❌ Missing required fields'

# Test to check invalid JSON format
def test_register_user_invalid_json(client):
    response = client.post('/register',
                           data="invalid_json",  # Not a JSON
                           content_type='application/json')

    assert response.status_code == 400
    json_response = response.get_json()
    assert json_response['status'] == 'error'
    assert json_response['message'] == '❌ Invalid request format'

# Test to check for already registered email
def test_register_user_duplicate_email(client):
    # First, register a user
    client.post('/register',
                data=json.dumps({
                    'fullname': 'John Doe',
                    'email': 'john.doe@example.com',
                    'password': 'Secure123!'
                }),
                content_type='application/json')

    # Try to register with the same email
    response = client.post('/register',
                           data=json.dumps({
                               'fullname': 'Jane Doe',
                               'email': 'john.doe@example.com',
                               'password': 'AnotherPass123!'
                           }),
                           content_type='application/json')

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['status'] == 'error'
    assert json_response['message'] == '❌ Email already registered.'

# Validators Tests
def test_validate_fullname_length():
    assert validators.validate_fullname_length("John")
    assert not validators.validate_fullname_length("Jo")

def test_validate_email_format():
    assert validators.validate_email_format("john@example.com")
    assert not validators.validate_email_format("@example.com")

def test_validate_password_strength():
    assert validators.validate_password_strength("abc123!")
    assert not validators.validate_password_strength("abcdef")

def test_validate_password_match():
    assert validators.validate_password_match("pass123!", "pass123!")
    assert not validators.validate_password_match("pass1", "pass2")

def test_validate_email_case_insensitive():
    assert validators.validate_email_case_insensitive("john@example.com")
    assert not validators.validate_email_case_insensitive("John@Example.com")

def test_validate_long_name():
    assert validators.validate_long_name("John")
    assert not validators.validate_long_name("J" * 51)

def test_validate_long_password():
    assert validators.validate_long_password("a" * 100)
    assert not validators.validate_long_password("a" * 101)

def test_validate_trim():
    assert validators.validate_trim("John", "john@example.com", "pass123!")
    assert not validators.validate_trim(" John ", "john@example.com", "pass123!")

def test_validate_email_plus():
    assert validators.validate_email_plus("john+test@example.com")
    assert not validators.validate_email_plus("john@example.com")

def test_validate_password_common():
    assert validators.validate_password_common("securepass")
    assert not validators.validate_password_common("123456")

def test_validate_no_numbers_in_name():
    assert validators.validate_no_numbers_in_name("Alice")
    assert not validators.validate_no_numbers_in_name("Al1ce")

def test_validate_password_case_sensitive():
    assert validators.validate_password_case_sensitive("Secure123")
    assert not validators.validate_password_case_sensitive("secure")

def test_validate_not_empty():
    assert validators.validate_not_empty("John", "john@example.com", "pass")
    assert not validators.validate_not_empty("", "john@example.com", "pass")

def test_validate_confirm_not_empty():
    assert validators.validate_confirm_not_empty("pass123!")
    assert not validators.validate_confirm_not_empty("")

def test_validate_email_proper():
    assert validators.validate_email_proper("john@example.com")
    assert not validators.validate_email_proper("john@example")
