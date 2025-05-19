from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configurar Chrome para entorno sin interfaz gráfica (CI/CD)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.get("http://127.0.0.1:5000/")

def test_case(fullname, email, pwd, conf, expected_msg):
    driver.find_element(By.ID, "fullname").clear()
    driver.find_element(By.ID, "fullname").send_keys(fullname)
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(pwd)
    driver.find_element(By.ID, "confirm_password").clear()
    driver.find_element(By.ID, "confirm_password").send_keys(conf)
    driver.find_element(By.TAG_NAME, "button").click()

    msg = driver.find_element(By.ID, "msg").text
    assert msg == expected_msg, f"Esperaba '{expected_msg}', pero salió '{msg}'"

# Casos de prueba
test_case("Juan", "juan@mail.com", "Abc123", "Abc123", "Registro exitoso")
test_case("", "juan@mail.com", "Abc123", "Abc123", "Nombre inválido")
test_case("Juan", "juanmail.com", "Abc123", "Abc123", "Email inválido")
test_case("Juan", "juan@mail.com", "abc", "abc", "Contraseña corta")
test_case("Juan", "juan@mail.com", "Abc123", "Xyz123", "Contraseñas no coinciden")

driver.quit()