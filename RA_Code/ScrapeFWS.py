"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape Risk Assessments of FWS U.S. Fish & Wildlife Service. 
This script functions slightly different from the other risk assessment scripts; it scrapes all risk assessments from the entire website (since it's faster). 
Thus, hopefully, this script will be more robust to future changes and feature alterations, meaning it might require less maintenance. 
Full function of script:
    - Scrapes all risk assessments of FWS with selenium, 10 RA's per batch as is shown on the website (site offers 186 RA's)
    - Saves all risk assessments in a list
    - Compares project IAS list with FWS RA list.
    - Builds a site quote for each IAS that has a RA featured on FWS, and appends it to the ln_names_dict. 
    - ln_names_dict is returned to main, so it can be written to CSV file (see RA_scraping_suite.py and Scraped_RA_info.csv)

You might have to install some requirements using:
pip install undetected-chromedriver
pip install webdriver-manager
python -m pip uninstall undetected-chromedriver
python -m pip install git+https://github.com/ultrafunkamsterdam/undetected-chromedriver@fix-multiple-instance
python -m pip install --upgrade selenium
    
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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_fws():
    options = Options() 
    options.headless = True     # options.add_argument('--headless')
    url = "https://www.fws.gov/library/categories/ecological-risk-screening"
    driver = uc.Chrome(use_subprocess=True, options=options) 
    RA_title_token = "//div//a[contains(text(), 'Ecological Risk Screening Summary')]"
    x = 0
    FWS_RA_list = []
    try:
        driver.get(url)
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, RA_title_token)))
        driver.implicitly_wait(3)

        assert driver.find_element(By.XPATH, "//div[@class='mat-select-value']//span")
        driver.find_element(By.XPATH, "//div[@class='mat-select-value']//span").click()
        driver.implicitly_wait(3)

        assert driver.find_element(By.XPATH, "//span[contains(text(),'High Risk')]")
        driver.find_element(By.XPATH, "//span[contains(text(),'High Risk')]").click()
        driver.implicitly_wait(10)

        assert driver.find_element(By.XPATH, "//span[@class='ng-star-inserted']")
        ra_count_ele_txt = driver.find_element(By.XPATH, "//span[@class='ng-star-inserted']").text
        real_count = ra_count_ele_txt[-3:]
        real_count = round(int(real_count) / 10, 0)
        print("Nr of pages to scrape: ", real_count)        

        while x < real_count:
            print("round: ", x)
            driver.implicitly_wait(3)
            element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, RA_title_token))
                )
            element = driver.find_elements(By.XPATH, RA_title_token)
            for value in element:
                text = value.text
                links = [value.get_attribute('href')]
                full_text = text + "$" + links[0]
                FWS_RA_list.append(full_text)
            x += 1
            element = driver.find_element(By.XPATH, "//div[@class='footer-top']")
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            driver.implicitly_wait(7)
            assert driver.find_element(By.XPATH, "(//li[@class='search-pager-arrow'])[2]")
            driver.find_element(By.XPATH, "(//li[@class='search-pager-arrow'])[2]").click()
            driver.implicitly_wait(3)
        return FWS_RA_list
    except TimeoutError:
        print(TimeoutError)
        pass    

def get_quotes(FWS_RA_list, ln_names_dict):
    for i in ln_names_dict.keys():
        for item in FWS_RA_list:
            matches = re.findall(ln_names_dict[i][0], item)
            matches = list(set(matches))
            if len(matches) > 0:
                print(matches)
                print("https://www.fws.gov/media/" + item)
                item = item.split("$")
                quote = "FWS U.S. Fish & Wildlife Service offers risk screening: " + item[1]
                ln_names_dict[i].append(quote)

    print(ln_names_dict)
    return ln_names_dict


def main_scraper(ln_names_dict):
    FWS_RA_list = scrape_fws()
    ln_scraping_dict = get_quotes(FWS_RA_list, ln_names_dict)

    return ln_scraping_dict

if __name__ == "__main__":
    """
    
    """
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