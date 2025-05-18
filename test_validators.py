import pytest
from server import create_app
import validators
import json
import secrets

# ---------------------- FIXTURE ----------------------

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

# ---------------------- ENDPOINT TESTS ----------------------

def test_register_user_success(client):
    email = f"john.doe{secrets.randbelow(9000) + 1000}@example.com"
    response = client.post('/register',
                           data=json.dumps({
                               'fullname': 'John Doe',
                               'email': email,
                               'password': 'Secure123!',
                               'confirm': 'Secure123!'
                           }),
                           content_type='application/json')

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['status'] == 'success'

def test_register_user_missing_fields(client):
    response = client.post('/register',
                           data=json.dumps({
                               'fullname': 'John Doe',
                               'email': '',
                               'password': 'Secure123!',
                               'confirm': 'Secure123!'
                           }),
                           content_type='application/json')

    assert response.status_code == 400
    json_response = response.get_json()
    assert json_response['status'] == 'error'
    assert json_response['message'] == '❌ Missing required fields'

def test_register_user_invalid_json(client):
    response = client.post('/register',
                           data="invalid_json",
                           content_type='application/json')

    assert response.status_code == 400
    json_response = response.get_json()
    assert json_response['status'] == 'error'
    assert json_response['message'] == '❌ Invalid request format'

def test_register_user_duplicate_email(client):
    client.post('/register',
                data=json.dumps({
                    'fullname': 'John Doe',
                    'email': 'john.doe@example.com',
                    'password': 'Secure123!',
                    'confirm': 'Secure123!'
                }),
                content_type='application/json')

    response = client.post('/register',
                           data=json.dumps({
                               'fullname': 'Jane Doe',
                               'email': 'john.doe@example.com',
                               'password': 'AnotherPass123!',
                               'confirm': 'AnotherPass123!'
                           }),
                           content_type='application/json')

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['status'] == 'error'
    assert json_response['message'] == '❌ Email already registered.'

# ---------------------- VALIDATOR UNIT TESTS ----------------------

def test_validate_not_empty():
    assert validators.validate_not_empty("John", "john@example.com", "pass123!")
    assert not validators.validate_not_empty("", "john@example.com", "pass123!")

def test_validate_confirm_not_empty():
    assert validators.validate_confirm_not_empty("pass123!")
    assert not validators.validate_confirm_not_empty(" ")

def test_validate_fullname_length():
    assert validators.validate_fullname_length("John")
    assert not validators.validate_fullname_length("Jo")

def test_validate_long_name():
    assert validators.validate_long_name("John" * 10)
    assert not validators.validate_long_name("J" * 51)

def test_validate_no_numbers_in_name():
    assert validators.validate_no_numbers_in_name("Alice")
    assert not validators.validate_no_numbers_in_name("Al1ce")

def test_validate_email_format():
    assert validators.validate_email_format("john@example.com")
    assert not validators.validate_email_format("@example.com")

def test_validate_email_proper():
    assert validators.validate_email_proper("john@example.com")
    assert not validators.validate_email_proper("john@example")

def test_validate_email_case_insensitive():
    assert validators.validate_email_case_insensitive("john@example.com")
    assert not validators.validate_email_case_insensitive("John@Example.com")

def test_validate_email_plus():
    assert validators.validate_email_plus("john@example.com")
    assert not validators.validate_email_plus("john+spam@example.com")

def test_validate_password_strength():
    assert validators.validate_password_strength("Secure123!")
    assert not validators.validate_password_strength("weakpass")
    assert not validators.validate_password_strength("NoSpecial123")
    assert not validators.validate_password_strength("noupper123!")
    assert not validators.validate_password_strength("NOLOWER123!")

def test_validate_password_common():
    assert validators.validate_password_common("securepass")
    assert not validators.validate_password_common("123456")

def test_validate_password_case_sensitive():
    assert validators.validate_password_case_sensitive("Secure123")
    assert not validators.validate_password_case_sensitive("secure123")

def test_validate_password_match():
    assert validators.validate_password_match("Password1!", "Password1!")
    assert not validators.validate_password_match("Password1!", "password1!")

def test_validate_long_password():
    assert validators.validate_long_password("a" * 30)
    assert not validators.validate_long_password("a" * 31)

def test_validate_trim():
    assert validators.validate_trim("John", "john@example.com", "Secure123!")
    assert not validators.validate_trim(" John ", "john@example.com", "Secure123!")
