from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")
driver.implicitly_wait(20)
driver.maximize_window()

usuario = "standard_user"
password = "secret_sauce"

# Aguardar até que o campo de usuário esteja presente
campo_usuario = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((
        By.XPATH, 
        "//input[@id='user-name' and @placeholder='Username']"
    ))
)

campo_senha = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((
        By.XPATH, 
        "//input[@id='password' and @placeholder='Password']"
    ))
)

login_button = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((
        By.XPATH, 
        "//input[@id='login-button' and @name='login-button']"
    ))
)

# Preencher o campo de usuário com um valor
campo_usuario.send_keys(usuario)
campo_senha.send_keys(password)
login_button.click()

logo = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((
        By.XPATH, 
        "//div[contains(@class, 'app_logo')]"
    ))
)

print(logo.text)

driver.quit()