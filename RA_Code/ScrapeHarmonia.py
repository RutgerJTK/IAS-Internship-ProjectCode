"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

from time import perf_counter
import time
import re
from bs4 import BeautifulSoup
import requests
import requests_html
import lxml
from lxml import html
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_harmonia(ln_names_dict):
    try:
        url = "https://ias.biodiversity.be/species/risk"

        options = webdriver.FirefoxOptions();
        options.add_argument('headless');
        
        driver = webdriver.Firefox()
        driver.get(url)
        for i in ln_names_dict.keys():
            # driver.find_element(By.XPATH, "//td[contains(text(), '{}')]".format(ln_names_dict[i][0]))
            driver.find_element(By.XPATH, "//td[@class='scientificname']")
            

    except TimeoutError:
        pass
    return(ln_names_dict)

def main_scraper(ln_names_dict):
    ln_scraping_dict = scrape_harmonia(ln_names_dict)
    return ln_scraping_dict

if __name__ == "__main__":
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    ias_file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = {}

    try: 
        import RA_scraping_suite
    except ModuleNotFoundError:
        from RA_Code import RA_scraping_suite
        
    ln_names_dict = RA_scraping_suite.read_file(ias_file)
    ln_scraping_dict = main_scraper(ln_names_dict)
    for i in ln_names_dict.keys():
        if len(ln_names_dict[i])> 1:
            print(len(ln_names_dict[i]))

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)