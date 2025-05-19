import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_case(fullname, email, password, confirm_password, expected_msg):
    path = os.path.abspath("static/test_form.html")
    driver.get("file://" + path)

    driver.find_element(By.ID, "fullname").clear()
    driver.find_element(By.ID, "fullname").send_keys(fullname)
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "confirm_password").clear()
    driver.find_element(By.ID, "confirm_password").send_keys(confirm_password)
    driver.find_element(By.TAG_NAME, "button").click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "validation_message")))
    msg = driver.find_element(By.ID, "validation_message").text
    print("Mensaje:", msg)
    assert expected_msg in msg, f"Esperado '{expected_msg}', obtenido '{msg}'"

driver = webdriver.Chrome()  # o el driver que uses
try:
    test_case("Juan", "juan@mail.com", "Abc123", "Abc123", "Registro exitoso")
finally:
    driver.quit()
