import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

@pytest.mark.parametrize("fullname,email,password,confirm_password,expected_message", [
    ("Juan", "juan@mail.com", "Abc123!", "Abc123!", "✔️ Registro exitoso"),
    ("An", "invalidemail", "123", "1234", "❌ Full Name must be at least 3 characters. | ❌ Invalid email format. | ❌ Password must be at least 6 characters. | ❌ Passwords do not match."),
    ("Maria", "maria@mail.com", "pass12", "pass12", "✔️ Registro exitoso"),
])
def test_case(fullname, email, password, confirm_password, expected_message):
    chrome_options = Options()
    # Añadimos opciones para evitar error de sesión
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless=new")  # Ejecución sin GUI (opcional)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/unique_selenium_profile")  # Evitar conflicto de sesión
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("file:///home/runner/work/GIT-REGISTRY-FORM/GIT-REGISTRY-FORM/test_form.html")  # Ajusta esta ruta a tu archivo de prueba

        driver.find_element(By.ID, "fullname").clear()
        driver.find_element(By.ID, "fullname").send_keys(fullname)

        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys(email)

        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(password)

        driver.find_element(By.ID, "confirm_password").clear()
        driver.find_element(By.ID, "confirm_password").send_keys(confirm_password)

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Pequeña espera para que se actualice el mensaje
        time.sleep(0.5)

        message = driver.find_element(By.ID, "validation_message").text
        assert message == expected_message

    finally:
        driver.quit()