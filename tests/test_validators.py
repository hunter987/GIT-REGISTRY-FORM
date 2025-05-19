import pytest
from validators import (
    validate_not_empty,
    validate_confirm_not_empty,
    validate_fullname_length,
    validate_long_name,
    validate_no_numbers_in_name,
    validate_email_format,
    validate_email_proper,
    validate_email_case_insensitive,
    validate_email_plus,
    validate_password_strength,
    validate_password_common,
    validate_password_case_sensitive,
    validate_password_match,
    validate_long_password,
    validate_trim,
    evaluar_validadores
)

# --- Pruebas de validaciones individuales ---

def test_validate_not_empty():
    assert validate_not_empty("Juan", "correo@example.com", "Pass123!") is True
    assert validate_not_empty("", "correo@example.com", "Pass123!") is False

def test_validate_confirm_not_empty():
    assert validate_confirm_not_empty("Pass123!") is True
    assert validate_confirm_not_empty("") is False

def test_validate_fullname_length():
    assert validate_fullname_length("Juan") is True
    assert validate_fullname_length("Jo") is False

def test_validate_long_name():
    assert validate_long_name("Juan Pérez García") is True
    assert validate_long_name("J" * 51) is False  # Excede el límite

def test_validate_no_numbers_in_name():
    assert validate_no_numbers_in_name("Juan") is True
    assert validate_no_numbers_in_name("Juan123") is False

def test_validate_email_format():
    assert validate_email_format("correo@example.com") is True
    assert validate_email_format("correo@com") is False
    assert validate_email_format("correo.com") is False

def test_validate_email_proper():
    # La función solo verifica la existencia de "@" y de un punto en la parte del dominio.
    assert validate_email_proper("correo@example.com") is True
    assert validate_email_proper("correo@com") is False
    # Aunque este input es un intento de inyección SQL, la función lo considera bien formado.
    assert validate_email_proper("correo@example.com' OR 1=1 --") is True

def test_validate_email_case_insensitive():
    assert validate_email_case_insensitive("correo@example.com".lower()) is True
    assert validate_email_case_insensitive("CORREO@EXAMPLE.COM") is False

def test_validate_email_plus():
    # La implementación actual rechaza correos que contienen '+'.
    assert validate_email_plus("john+test@example.com") is False
    assert validate_email_plus("correo@example.com") is True

def test_validate_password_strength():
    # Se asume que el requisito mínimo es 8 caracteres.
    assert validate_password_strength("Pass1A$X") is True         # 8 caracteres, cumple mayúsculas, minúsculas, dígito y símbolo.
    assert validate_password_strength("abc123!") is False         # Falta mayúscula.
    # "Abc123!" tiene 7 caracteres; al requerirse 8, se espera que retorne False.
    assert validate_password_strength("Abc123!") is False         
    assert validate_password_strength("Pass123") is False         # Falta símbolo especial.

def test_validate_password_common():
    assert validate_password_common("password") is False
    assert validate_password_common("SecurePass1!") is True

def test_validate_password_case_sensitive():
    assert validate_password_case_sensitive("Pass123") is True
    assert validate_password_case_sensitive("pass123") is False

def test_validate_password_match():
    assert validate_password_match("clave123", "clave123") is True
    assert validate_password_match("clave123", "clave124") is False

def test_validate_long_password():
    # Se asume que la longitud máxima aceptada es de 30 caracteres.
    assert validate_long_password("Pass123!") is True
    assert validate_long_password("a" * 30) is True
    assert validate_long_password("a" * 31) is False

def test_validate_trim():
    assert validate_trim("Juan", "correo@example.com", "Pass123!") is True
    assert validate_trim(" Juan ", "correo@example.com ", "Pass123! ") is False

def test_evaluar_validadores():
    # Se usa una contraseña válida de 8 caracteres para que la validación de fortaleza (password strength) sea "✅".
    resultado = evaluar_validadores("Juan", "correo@example.com", "Pass1A$X", "Pass1A$X")
    assert resultado["validate_fullname_length"] == "✅"
    assert resultado["validate_email_format"] == "✅"
    assert resultado["validate_password_strength"] == "✅"
    assert resultado["validate_password_match"] == "✅"

def test_validate_sql_injection():
    # El formato de email debe rechazar intentos de inyección a nivel de formato.
    assert validate_email_format("correo@example.com' OR 1=1 --") is False
    # La función validate_email_proper no filtra inyección; se espera True según su implementación.
    assert validate_email_proper("correo@example.com' OR 1=1 --") is True