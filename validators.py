SPECIAL_CHARS = "!@#$%^&*"

def marcar(valor: bool) -> str:
    return "✅" if valor else "❌"

def validate_not_empty(name: str, email: str, password: str) -> bool:
    return all([name.strip(), email.strip(), password.strip()])

def validate_confirm_not_empty(confirm: str) -> bool:
    return bool(confirm.strip())

def validate_fullname_length(name: str) -> bool:
    return len(name) >= 3

def validate_long_name(name: str) -> bool:
    return len(name) <= 50

def validate_no_numbers_in_name(name: str) -> bool:
    return not any(char.isdigit() for char in name)

def validate_email_format(email: str) -> bool:
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_email_proper(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]

def validate_email_case_insensitive(email: str) -> bool:
    return email == email.lower()

def validate_email_plus(email: str) -> bool:
    return "+" not in email

def validate_password_strength(password: str) -> bool:
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in SPECIAL_CHARS for c in password)
    return all([has_upper, has_lower, has_digit, has_special]) and len(password) >= 8

def validate_password_common(password: str) -> bool:
    common_passwords = {"password", "123456", "qwerty", "abc123"}
    return password.lower() not in common_passwords

def validate_password_case_sensitive(password: str) -> bool:
    return any(c.isupper() for c in password)

def validate_password_match(password: str, confirm: str) -> bool:
    return password == confirm

def validate_long_password(password: str) -> bool:
    return len(password) <= 30

def validate_trim(name: str, email: str, password: str) -> bool:
    return all(
        s == s.strip()
        for s in [name, email, password]
    )

def evaluar_validadores(nombre: str, correo: str, clave: str, confirmacion: str) -> dict:
    return {
        "validate_fullname_length": marcar(validate_fullname_length(nombre)),
        "validate_email_format": marcar(validate_email_format(correo)),
        "validate_password_strength": marcar(validate_password_strength(clave)),
        "validate_password_match": marcar(validate_password_match(clave, confirmacion)),
        "validate_email_case_insensitive": marcar(validate_email_case_insensitive(correo)),
        "validate_long_name": marcar(validate_long_name(nombre)),
        "validate_long_password": marcar(validate_long_password(clave)),
        "validate_trim": marcar(validate_trim(nombre, correo, clave)),
        "validate_email_plus": marcar(validate_email_plus(correo)),
        "validate_password_common": marcar(validate_password_common(clave)),
        "validate_no_numbers_in_name": marcar(validate_no_numbers_in_name(nombre)),
        "validate_password_case_sensitive": marcar(validate_password_case_sensitive(clave)),
        "validate_not_empty": marcar(validate_not_empty(nombre, correo, clave)),
        "validate_confirm_not_empty": marcar(validate_confirm_not_empty(confirmacion)),
        "validate_email_proper": marcar(validate_email_proper(correo))
    }
