from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import undetected_chromedriver as uc
import time

driver = uc.Chrome()
driver.get("https://www.google.com")
driver.implicitly_wait(20)
driver.maximize_window()

campo_de_busca = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//textarea[@id='APjFqb']"))
)

campo_de_busca.send_keys("Python Selenium")
campo_de_busca.submit()

h3 = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, 'h3'))
)

titulos_h3 = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3.LC20lb'))
)

tags_links = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'cite'))
)

time.sleep(5)

titulos = [titulo.text.strip() for titulo in titulos_h3 if titulo.text.strip()][:5]

links = [link.text.strip() for link in tags_links if link.text.strip()][:5]

for titulo, link in zip(titulos, links):
    print(f"{titulo} - {link}")

driver.quit()