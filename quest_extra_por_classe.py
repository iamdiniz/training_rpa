from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from fpdf import FPDF
import sys
import PyPDF2
import time
import os


meu_diretorio_download = "C:\\Users\\0180035\\Downloads"
url = "https://demo.automationtesting.in/FileDownload.html"


class MainBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = url


    def open_site(self):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(20)
            self.driver.maximize_window()

        except Exception as e:
            print("Erro inesperado: ", e)


    def download_pdf_file(self):
        try:
            # Aguardar até que o campo de usuário esteja presente
            download_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//a[contains(@class, 'btn btn-primary')]"
                ))
            )

            download_button.click()
        except Exception as e:
            print("Erro inesperado: ", e)


    def identify_pdf_file(self, arquivos_antes):
        try:
            start_time = time.time()
            timeout = 30

            while True:
                # Comparar arquivos atuais com os anteriores
                arquivos_atuais = set(os.listdir(meu_diretorio_download))
                novos_arquivos = arquivos_atuais - arquivos_antes

                if novos_arquivos:
                    # Um novo arquivo foi detectado
                    arquivo_baixado = novos_arquivos.pop()
                    print(f"Arquivo baixado: {arquivo_baixado}")
                    break

                elif time.time() - start_time > timeout:
                    print("Tempo limite excedido para o download.")
                    break

                print("Nenhum novo arquivo detectado ainda. Continuando...")
                time.sleep(1)

            if arquivo_baixado: # SE FOR BAIXADO...
                return os.path.join(meu_diretorio_download, arquivo_baixado)  # Retorna o caminho completo
            else: # SE NÃO FOR BAIXADO...
                return None
        except Exception as e:
            print("Erro inesperado: ", e)


    def read_pdf_file(self, pdf_path):
        try:
            # Abre o arquivo PDF
            with open(pdf_path, 'rb') as arquivo_pdf:
                # Cria um objeto PDF Reader
                leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
                
                # Armazena o conteúdo das páginas
                texto_total = ''
                
                # Itera sobre todas as páginas do PDF
                for pagina_num in range(len(leitor_pdf.pages)):
                    pagina = leitor_pdf.pages[pagina_num]
                    texto_total += pagina.extract_text()
                
                return texto_total
        except Exception as e:
            print("Erro inesperado: ", e)


    def send_text_to_field_text(self, text):
        try:
            campo_de_texto = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//textarea[contains(@id, 'textbox') and contains(@class, 'form-control')]"
                ))
            )

            campo_de_texto.send_keys(text[:1000])
        except Exception as e:
            print("Erro inesperado: ", e)


    def click_on_generate_file_button(self):
        try:
            generate_file_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//button[contains(@id, 'createTxt') and contains(@class, 'btn btn-default')]"
                ))
            )

            generate_file_button.click()
        except Exception as e:
            print("Erro inesperado: ", e)


    def click_on_download_button(self):
        try:
            download_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//a[contains(@id, 'link-to-download')]"
                ))
            )

            download_button.click()
        except Exception as e:
            print("Erro inesperado: ", e)


    def convert_txt_to_pdf(self, txt_path, pdf_path):
        try:
            # Cria um objeto PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Define a fonte do texto no PDF
            pdf.set_font("Arial", size=12)

            # Abre o arquivo de texto com uma codificação diferente
            with open(txt_path, 'r', encoding='ISO-8859-1') as arquivo_txt:  # Tenta com ISO-8859-1
                # Lê linha por linha e adiciona ao PDF
                for linha in arquivo_txt:
                    pdf.multi_cell(0, 10, linha)  # Adiciona o texto ao PDF com quebras automáticas de linha

            # Salva o arquivo PDF no caminho especificado
            pdf.output(pdf_path)  # Isso cria o arquivo PDF
            print(f"Arquivo PDF gerado com sucesso: {pdf_path}")
        except Exception as e:
            print("Erro inesperado: ", e)


if __name__ == "__main__":
    try:
        bot = MainBot()
        bot.open_site()
        meu_diretorio_antes_de_baixar_o_pdf = set(os.listdir(meu_diretorio_download))
        bot.download_pdf_file()
        time.sleep(5)

        arquivo_pdf_baixado = None
        arquivo_pdf_baixado = bot.identify_pdf_file(meu_diretorio_antes_de_baixar_o_pdf)

        if arquivo_pdf_baixado:
            texto_pdf = bot.read_pdf_file(arquivo_pdf_baixado)
        else:
            print("Nenhum arquivo baixado.")
            sys.exit(1)

        bot.send_text_to_field_text(texto_pdf)
        bot.click_on_generate_file_button()
        bot.click_on_download_button()

        meu_diretorio_antes_de_baixar_o_txt = set(os.listdir(meu_diretorio_download))

        arquivo_txt_baixado = None
        arquivo_txt_baixado = bot.identify_pdf_file(meu_diretorio_antes_de_baixar_o_pdf)

        if arquivo_txt_baixado:
            bot.convert_txt_to_pdf(arquivo_txt_baixado, arquivo_pdf_baixado)
        else:
            print("Nenhum arquivo baixado.")
            sys.exit(1)

        time.sleep(5)
    except Exception as e:
        print("Erro inesperado: ", e)