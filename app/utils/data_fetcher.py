from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class DataFetcher:
    def fetch_data(self, url, table_xpath):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)

        element = driver.find_element("xpath", table_xpath)
        html_table = element.get_attribute("outerHTML")
        driver.quit()
        
        table = pd.read_html(str(html_table), thousands='.', decimal=',')[0]
        return table