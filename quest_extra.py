from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from fpdf import FPDF
import sys
import PyPDF2
import time
import os

driver = webdriver.Chrome()
meu_diretorio_download = "C:\\Users\\0180035\\Downloads"
url = "https://demo.automationtesting.in/FileDownload.html"


def identificar_arquivo(arquivos_antes, arquivo_baixado):
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


def ler_pdf(caminho_pdf):
    try:
        # Abre o arquivo PDF
        with open(caminho_pdf, 'rb') as arquivo_pdf:
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
        print(f"Erro ao ler o PDF: {e}")
        return None


def txt_para_pdf(caminho_txt, caminho_pdf):
    try:
        # Cria um objeto PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Define a fonte do texto no PDF
        pdf.set_font("Arial", size=12)

        # Abre o arquivo de texto com uma codificação diferente
        with open(caminho_txt, 'r', encoding='ISO-8859-1') as arquivo_txt:  # Tenta com ISO-8859-1
            # Lê linha por linha e adiciona ao PDF
            for linha in arquivo_txt:
                pdf.multi_cell(0, 10, linha)  # Adiciona o texto ao PDF com quebras automáticas de linha

        # Salva o arquivo PDF no caminho especificado
        pdf.output(caminho_pdf)  # Isso cria o arquivo PDF
        print(f"Arquivo PDF gerado com sucesso: {caminho_pdf}")

    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")


def main():
    try:
        driver.get(url)
        driver.implicitly_wait(20)
        driver.maximize_window()

        arquivos_antes = set(os.listdir(meu_diretorio_download))
        arquivo_pdf_baixado = None
        arquivo_txt_baixado = None

        time.sleep(1)

        # Aguardar até que o campo de usuário esteja presente
        download_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//a[contains(@class, 'btn btn-primary')]"
            ))
        )

        download_button.click()

        time.sleep(5)

        arquivo_pdf_baixado = identificar_arquivo(arquivos_antes, arquivo_pdf_baixado)

        if arquivo_pdf_baixado:
            texto_pdf = ler_pdf(arquivo_pdf_baixado)
        else:
            print("Nenhum arquivo baixado.")
            sys.exit(1)

        campo_de_texto = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//textarea[contains(@id, 'textbox') and contains(@class, 'form-control')]"
            ))
        )

        campo_de_texto.send_keys(texto_pdf[:1000])

        generate_file_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[contains(@id, 'createTxt') and contains(@class, 'btn btn-default')]"
            ))
        )

        generate_file_button.click()

        download_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//a[contains(@id, 'link-to-download')]"
            ))
        )

        arquivos_antes2 = set(os.listdir(meu_diretorio_download))

        download_button.click()

        arquivo_txt_baixado = identificar_arquivo(arquivos_antes2, arquivo_txt_baixado)

        if arquivo_txt_baixado:
            txt_para_pdf(arquivo_txt_baixado, arquivo_pdf_baixado)
        else:
            print("Nenhum arquivo baixado.")
            sys.exit(1)

        driver.quit()

    except Exception as e:
        print("Erro inesperado: ", e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Erro inesperado: ", e)