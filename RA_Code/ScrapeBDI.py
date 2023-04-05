"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from https://species.biodiversityireland.ie/?keyword=Catalogue%20of%20Irelands%20Non-native%20Species
Future goal of script: 
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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_INPN(ln_names_dict):
    print("start scraping")
    BDI_spec = ""
    name_ln = 'Baccharis halimifolia'
    options = FirefoxOptions()
    options.add_argument('--headless')
    url = "https://species.biodiversityireland.ie/index.php?"
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    driver.implicitly_wait(5) # Hard waits via time.sleeps are stupid, use implicit and explicit waits from selenium
    # time.sleep(2)
    assert driver.find_element(By.XPATH, "//a[@class='cc-btn cc-dismiss']")
    driver.find_element(By.XPATH, "//a[@class='cc-btn cc-dismiss']").click()
    time.sleep(1)
    counter = 0 

    for i in ln_names_dict.keys():
        counter += 1
        print(counter, " number in dict")
        try:
            name = ln_names_dict[i][0]
            if name == "Alopochen aegyptiaca":  # There are a few latin names which differ from the ones we use. 
                name = "Alopochen aegyptiacus"
            elif name == "Trachemys scripta elegans":
                name = "Trachemys scripta subsp. elegans"
            elif name == "Trachemys scripta troostii":
                name = "Trachemys scripta troosti"
            wait = WebDriverWait(driver, 2)  
            taxonName = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='taxonName']")))
            ActionChains(driver).click(taxonName)
            driver.find_element(By.XPATH, "//input[@id='taxonName']").send_keys("{}".format(name))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            name2 = name.split(" ")
            
            driver.implicitly_wait(3) 
            assert driver.find_element(By.XPATH, "//a[contains(text(), '{}')]".format(name2[0]))
            driver.find_element(By.XPATH, "//a[contains(text(), '{}')]".format(name2[0])).click()
            # assert driver.find_element(By.XPATH, "//td//a[text()='{}']".format(name))
            # driver.find_element(By.XPATH, "//td//a[text()='{}']".format(name)).click()

            driver.implicitly_wait(1) 
            # assert driver.find_element(By.XPATH, "//li//a[text()='Status']".format(name))
            # driver.find_element(By.XPATH, "//li//a[text()='Status']".format(name)).click()

            ######
            ### grab invasiveness status/Risk Assessment info.
            ######

            driver.back(), driver.back() ## go back twice
            
            driver.implicitly_wait(1) 
            assert driver.find_element(By.XPATH, "//input[@id='taxonName']")
            driver.find_element(By.XPATH, "//input[@id='taxonName']").click()
            driver.find_element(By.XPATH, "//input[@id='taxonName']").send_keys(Keys.CONTROL,"a")
        except Exception:
            
            print(ln_names_dict[i][0])
            driver.implicitly_wait(1) 
            assert driver.find_element(By.XPATH, "//input[@id='taxonName']")
            driver.find_element(By.XPATH, "//input[@id='taxonName']").click()
            driver.find_element(By.XPATH, "//input[@id='taxonName']").send_keys(Keys.CONTROL,"a")
            pass
        # driver.find_element(By.XPATH, "//input[@id='taxonName']").send_keys("Brachio") 


    time.sleep(1)
    # element = driver.find_elements(By.XPATH, "//td[@class='exp sorting_1']//i")
    # time.sleep(1)
    # for value in element:
    #     BDI_spec = BDI_spec + value.text + ", "
    # driver.close()
    print(counter)
    BDI_spec = ""
    return BDI_spec


def species_ra_check(ln_names_dict, BDI_spec):
    for i in ln_names_dict.keys():
        matches = re.findall(ln_names_dict[i][0], BDI_spec)
        if len(matches) > 0:
            ln_names_dict[i].append("Assessed (to some degree) on INPN: https://inpn.mnhn.fr/espece/listeEspeces/statut/metropole/J?lg=en")
    return ln_names_dict


def main_scraper(ln_names_dict):
    BDI_spec = scrape_INPN(ln_names_dict)
    ln_scraping_dict = species_ra_check(ln_names_dict, BDI_spec)
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