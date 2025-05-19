import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

@pytest.mark.parametrize("fullname,email,password,confirm_password,expected_message", [
    ("Juan", "juan@mail.com", "Abc123!", "Abc123!", "✔️ Registro exitoso"),
    ("An", "invalidemail", "123", "1234", "❌ Full Name must be at least 3 characters. | ❌ Invalid email format. | ❌ Password must be at least 6 characters. | ❌ Passwords do not match."),
    ("Maria", "maria@mail.com", "pass12", "pass12", "✔️ Registro exitoso"),
])
def test_case(fullname, email, password, confirm_password, expected_message):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless=new")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/unique_selenium_profile")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("file:///home/runner/work/GIT-REGISTRY-FORM/GIT-REGISTRY-FORM/test_form.html")

        wait = WebDriverWait(driver, 5)  # espera hasta 5 segundos

        # Espera y rellena fullname
        fullname_field = wait.until(EC.presence_of_element_located((By.ID, "fullname")))
        fullname_field.clear()
        fullname_field.send_keys(fullname)

        # Email
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.clear()
        email_field.send_keys(email)

        # Password
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys(password)

        # Confirm password
        confirm_field = wait.until(EC.presence_of_element_located((By.ID, "confirm_password")))
        confirm_field.clear()
        confirm_field.send_keys(confirm_password)

        # Botón submit (espera que esté clickable)
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        submit_button.click()

        # Espera que el mensaje de validación aparezca y contenga texto
        message_element = wait.until(lambda d: d.find_element(By.ID, "validation_message").text != "")
        message = driver.find_element(By.ID, "validation_message").text

        assert message == expected_message

    except TimeoutException as e:
        pytest.fail(f"Timeout esperando elemento: {e}")
    except NoSuchElementException as e:
        pytest.fail(f"No se encontró un elemento necesario: {e}")
    finally:
        driver.quit()