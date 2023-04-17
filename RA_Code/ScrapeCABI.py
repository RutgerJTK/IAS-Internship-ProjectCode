"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
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
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.chrome.options import Options 
import time 
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def scrape_cabi(ln_names_dict):
    options = Options() 
    options.headless = True     # options.add_argument('--headless')
    url = "https://www.cabidigitallibrary.org/"
    # driver = webdriver.Chrome(options=options, service=ChromeService(
        # ChromeDriverManager().install())) 
    driver = uc.Chrome(use_subprocess=True, options=options) 
    driver.get(url)
    driver.maximize_window() 
    try:
        driver.get(url)
        time.sleep(1)
        searchbartoken = "//input[@aria-label='Search CABI Digital Library']"
        cookies_button = "//button[@id='onetrust-accept-btn-handler']"
        assert driver.find_element(By.XPATH, cookies_button)
        driver.find_element(By.XPATH, cookies_button).click()
        time.sleep(1)
        assert driver.find_element(By.XPATH, searchbartoken)
        driver.find_element(By.XPATH, searchbartoken).send_keys("Alopochen aegyptiaca")
        driver.find_element(By.XPATH, searchbartoken).send_keys(Keys.ENTER)
        assert driver.find_element(By.XPATH, "(//div[@class='issue-item__header']//span)[3]")
        for i in ln_names_dict.keys():
            print(ln_names_dict[i][0])
            name = ln_names_dict[i][0]
            driver.find_element(By.XPATH, "//textarea[@class='autocomplete ui-autocomplete-input']").click()
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
            driver.find_element(By.XPATH, "//textarea[@class='autocomplete ui-autocomplete-input']").send_keys(name)
            driver.find_element(By.XPATH, "//div[@class='searchButton']//button[@class='btn quick-search__button']").click()
            driver.implicitly_wait(3)
            name = name.split(" ")
            namebuilder = str(name[0]+ "+" + name[1])
            assert driver.find_element(By.XPATH, "//span[@class='result__count']")
            result_count = driver.find_element(By.XPATH, "//span[@class='result__count']").text
            if int(result_count) > 0:
                quote1 = "CABI yielded {} results: https://www.cabidigitallibrary.org/action/doSearch?AllField={}".format(result_count, namebuilder)
                ln_names_dict[i].append(quote1)
                if name[0] == driver.find_element(By.XPATH, "(//h5//span)[2]").text and name[1] == driver.find_element(By.XPATH, "(//h5//span)[3]").text:
                    driver.find_element(By.XPATH, "(//h5//span)[2]").click()
                    driver.implicitly_wait(5)
                    quote2_url = driver.current_url
                    print("here")
                    quote2 = "Datasheet by CABI: {}".format(quote2_url)
                    print("here2")
                    ln_names_dict[i].append(quote2)
                    driver.back()
                    driver.implicitly_wait(3)

    except TimeoutError:
        print(TimeoutError)
    driver.close()
    return ln_names_dict



def main_scraper(ln_names_dict):
    ln_scraping_dict = scrape_cabi(ln_names_dict)
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