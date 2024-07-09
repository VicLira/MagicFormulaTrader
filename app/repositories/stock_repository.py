from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import os
import yfinance as yf

class StockRepository:
    def __init__(self):
        self.url = "https://www.fundamentus.com.br"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def download_data(self):
        try:
            self.driver.get(f"{self.url}/resultado.php")
            local_tabela = "/html/body/div[1]/div[2]/table"
            elemento = self.driver.find_element("xpath", local_tabela)
            html_tabela = elemento.get_attribute("outerHTML")
            tabela = pd.read_html(html_tabela, thousands=".", decimal=",")[0]
            
            data_dir = "../../app/data"
            os.makedirs(data_dir, exist_ok=True)

            file_path = os.path.join(data_dir, "dados_empresas_fundamentus.csv")
            tabela.to_csv(file_path, index=False)
            return tabela
        except Exception as e:
            print(f"Erro ao baixar dados: {e}")
        return None
    
    def get_sector(self, ticker):
        try:
            url = f"{self.url}/detalhes.php?papel={ticker}"
            self.driver.get(url)
            local_sector = "/html/body/div[1]/div[2]/table[1]/tbody/tr[4]/td[2]/span/a"
            if self.driver.find_elements("xpath", local_sector):
                elemento = self.driver.find_element("xpath", local_sector)
                sector_text = elemento.text
                return sector_text
            else:
                return "N/A"
        except Exception as e:
            print(f"Erro ao obter setor para {ticker}: {e}")
            return "N/A"

    def get_return(self, ticker):
        try:
            url = f"{self.url}/detalhes.php?papel={ticker}"
            self.driver.get(url)
            min_52_weeks = "/html/body/div[1]/div[2]/table[1]/tbody/tr[3]/td[4]/span"
            max_52_weeks = "/html/body/div[1]/div[2]/table[1]/tbody/tr[4]/td[4]/span"
            min_price = self.driver.find_element("xpath", min_52_weeks).text.replace(",", ".")
            max_price = self.driver.find_element("xpath", max_52_weeks).text.replace(",", ".")
            if min_price and max_price:
                return (float(max_price) - float(min_price)) / float(min_price) * 100
            else:
                return None
        except Exception as e:
            print(f"Erro ao obter retorno para {ticker}: {e}")
            return None

    def load_data(self, file_path):
        try:
            selected_columns = ["Papel", "Cotação", "P/L", "P/VP", "EV/EBIT", "ROIC", "Liq.2meses"]
            data = pd.read_csv(file_path, usecols=selected_columns)
            data = self.treat_data(data)
            return data
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado em {file_path}")
            return None

    def treat_data(self, data):
        try:
            data["ROIC"] = data["ROIC"].str.replace("%", "")
            data["ROIC"] = data["ROIC"].str.replace(".", "")
            data["ROIC"] = data["ROIC"].str.replace(",", ".")
            data["ROIC"] = data["ROIC"].astype(float)

            return data
        except ValueError as e:
            print(f"Erro ao converter ROIC para float: {e}")
            return None

    def get_ibovespa_returns(self):
        try:
            ibovespa = yf.Ticker("^BVSP")
            hist = ibovespa.history(period="1y")
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            total_return = (end_price - start_price) / start_price
            return total_return
        except yf.DownloadError as e:
            print(f"Erro ao obter dados do Ibovespa: {e}")
            return None