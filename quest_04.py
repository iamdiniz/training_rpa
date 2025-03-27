from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import undetected_chromedriver as uc
import time

driver = uc.Chrome()
driver.get("https://www.mercadolivre.com.br/")
driver.implicitly_wait(20)
driver.maximize_window()

time.sleep(5)

campo_de_busca = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((
        By.XPATH, 
        "//input[@id='cb1-edit' and @name='as_word' and @class='nav-search-input']"
    ))
)

campo_de_busca.send_keys("notebook")
campo_de_busca.submit()

time.sleep(5)

titulos_h3 = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.XPATH, "//h3[@class='poly-component__title-wrapper']/a"))
)

precos_html = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((
        By.XPATH, 
        "//div[contains(@class, 'poly-price__current')]//span[@class='andes-money-amount__fraction' and @aria-hidden='true']"
    ))
)

time.sleep(5)

titulos = [titulo.text.strip() for titulo in titulos_h3 if titulo.text.strip()][:5]

precos = [link.text.strip() for link in precos_html if link.text.strip()][:5]

for titulo, preco in zip(titulos, precos):
    print(f"{titulo} - R${preco}")

driver.quit()