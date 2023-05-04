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
from selenium.webdriver.firefox.options import Options 
import time 
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


def scrape_fws():
    print("Yo")
    options = Options() 
    options.headless = True     # options.add_argument('--headless')
    url = "https://www.marktplaats.nl/"
    driver = webdriver.Firefox(options=options)
    # driver = uc.Chrome(use_subprocess=True, options=options, version_main="112.0.5615.139") 
    input_search_token = "//input[@class='hz-Nav-dropdown-toggle hz-Header-Autocomplete-input']"
    try:
        print("time to get url:")
        driver.get(url)
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, input_search_token)))
        driver.implicitly_wait(5)
        print("found it")
        
        cookie_token = "//button[@class='gdpr-consent-button hz-Button hz-Button--primary hz-Button--lg']"
        assert driver.find_element(By.XPATH, cookie_token)
        driver.find_element(By.XPATH, cookie_token).click()
        driver.implicitly_wait(2)

        for i in ln_names_dict.keys():
            x = False
            print(ln_names_dict[i][0])
            assert driver.find_element(By.XPATH, input_search_token)
            driver.find_element(By.XPATH, input_search_token).click()
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
            driver.find_element(By.XPATH, input_search_token).send_keys(Keys.DELETE)
            time.sleep(1)
            driver.find_element(By.XPATH, input_search_token).click()            
            driver.find_element(By.XPATH, input_search_token).send_keys(ln_names_dict[i][0])        
            driver.find_element(By.XPATH, input_search_token).send_keys(Keys.ENTER)
            driver.implicitly_wait(1)
            time.sleep(2)
            nr_of_res_token = "(//li[@data-testid='breadcrumb-last-item']//span)[1]"
            res_check = "(//li[@data-testid='breadcrumb-last-item']//span)[2]"
            item_title_token = "//h3[@class='hz-Listing-title']"
            item_pricing_token = "//span[@class='hz-Listing-price hz-text-price-label']"
            assert driver.find_element(By.XPATH, nr_of_res_token)
            assert driver.find_element(By.XPATH, res_check)
            check_query = driver.find_element(By.XPATH, res_check).text
            check_query = check_query.lower()
            driver.implicitly_wait(1)
            name = ln_names_dict[i][0]
            name2 = name.lower()
            print("Check1")
            if name2 not in check_query:
                print(name2, check_query)
                assert driver.find_element(By.XPATH, "(//span/..//a)[1]")
                driver.find_element(By.XPATH, "(//span/..//a)[1]").click()
                time.sleep(2)
                driver.implicitly_wait(3)
            results_amount = driver.find_element(By.XPATH, nr_of_res_token).text
            results_amount = results_amount.split(" ")
            if int(results_amount[0]) > 0:
                print("Check2")
                print("Number of results for " +  ln_names_dict[i][0] + ": " +  results_amount[0])
                item_listings = driver.find_elements(By.XPATH, item_title_token)
                item_pricings = driver.find_elements(By.XPATH, item_pricing_token)
                time.sleep(5)
                for listing in range(len(item_listings)):
                    item_title = item_listings[listing].text
                    item_title = item_title.lower()

                    print(name2, item_title)
                    if name2 in item_title:
                        x = True
                        print("Found an item for "+ ln_names_dict[i][0] + item_title)
                if x == True:
                    print(ln_names_dict[i][0] + " has offerings: " + str(len(item_listings)))
                    name = name.replace(" ", "+")
                    quote = "Marktplaats might offer this species: " + url + "q/" + name
                    print(quote)
                    ln_names_dict[i].append(quote)
            time.sleep(1)

    except TimeoutError:
        print(TimeoutError)
        pass    
    except WebDriverException as e:
        print(e)
        pass
    driver.close()

    return ln_names_dict




def main_scraper(ln_names_dict):
    FWS_RA_list = scrape_fws()
    ln_scraping_dict = ln_names_dict
    print(ln_scraping_dict)
    return ln_scraping_dict

if __name__ == "__main__":
    """
    
    """
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    ias_file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = {}

    try: 
        import MA_scraping_suite
    except ModuleNotFoundError:
        from MA_Code import MA_scraping_suite

    ln_names_dict = MA_scraping_suite.read_file(ias_file)
    ln_scraping_dict = main_scraper(ln_names_dict)

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)