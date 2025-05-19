import tempfile
import shutil
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_case(fullname, email, password, confirm_password, expected_message):
    # Crear perfil temporal para Chrome
    profile_dir = tempfile.mkdtemp()
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={profile_dir}")
    # chrome_options.add_argument("--headless")  # Descomenta si no quieres abrir ventana

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        # Carga el archivo local (ajusta la ruta si es necesario)
        html_path = os.path.abspath("static/test_form.html")
        driver.get(f"file://{html_path}")

        # Rellenar formulario
        driver.find_element(By.ID, "fullname").send_keys(fullname)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "confirm_password").send_keys(confirm_password)

        # Enviar formulario
        driver.find_element(By.ID, "submit_button").click()

        # Esperar el mensaje de validación visible
        msg_element = wait.until(EC.visibility_of_element_located((By.ID, "validation_message")))
        actual_message = msg_element.text

        assert expected_message in actual_message, f"Esperado: {expected_message}, Obtenido: {actual_message}"

        print(f"Test passed: {fullname} -> {actual_message}")

    finally:
        driver.quit()
        shutil.rmtree(profile_dir)

if __name__ == "__main__":
    # Prueba de ejemplo: ajusta expected_message según el test_form.html que tengas
    test_case("Juan", "juan@mail.com", "Abc123!", "Abc123!", "Registro exitoso")