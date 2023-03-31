"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from NNSSGB.gov 
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

from time import perf_counter
import time
import re
import bs4 
from bs4 import BeautifulSoup
import requests
import lxml
from lxml import html
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_glansis():
    print("start scraping")
    glansis_spec = ""
    options = webdriver.FirefoxOptions();
    options.add_argument('headless');
    url = "https://www.glerl.noaa.gov/glansis/raT2Explorer.html"

    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(1)

    assert driver.find_element(By.XPATH, '//select[@id="fullSpeciesSelector"]')
    driver.find_element(By.XPATH, '//select[@id="fullSpeciesSelector"]').click()
    time.sleep(2)
    element = driver.find_elements(By.XPATH, "//select[@id='fullSpeciesSelector']//option")
    for value in element:
        glansis_spec = glansis_spec + value.text + ", "
    
    return glansis_spec


def species_ra_check(ln_names_dict, glansis_spec):
    for i in ln_names_dict.keys():
        matches = re.findall(ln_names_dict[i][0], glansis_spec)
        if len(matches) > 0:
            ln_names_dict[i].append("Assessed (to some degree) on Glansis: https://www.glerl.noaa.gov/glansis/raT2Explorer.html")
    return ln_names_dict


def main_scraper(ln_names_dict):
    glansis_spec = scrape_glansis()
    ln_scraping_dict = species_ra_check(ln_names_dict, glansis_spec)
    print(ln_scraping_dict)
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

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)