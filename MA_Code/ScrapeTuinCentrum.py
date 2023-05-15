"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all marketdata from tuincentrum.nl.
Inner workings: All species for sale are scraped, these are compared to the invasive species list. 
                If any invasive species are being sold, the site link will be added to that species profile and nr of species counted is added to another dict.
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
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def scrape_tuin(ln_names_dict, store_supply, plants_list):
    """
    @input:     ln_names_dict, store_supply, and plants_list, as defined by main.
    @output:    ln_names_dict, store_supply, updated and filled according to scraped findings. 
    @func:      Creates a firefox webdriver to scrape tuincentrum.nl. Searches page for every plant. Significant findings are added to the dict.  
    """
    options = Options() 
    options.headless = True     # options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    # driver = uc.Chrome(use_subprocess=True, options=options, version_main="112.0.5615.139") 
    input_search_token = "//input[@id='searchquery']"
    counter = 0
    try:
        print("Get url:")
        driver.get("https://www.google.com/")       # Website has me jumping through hoops due to anti botting software so i have to fake a page visit via google.
        element = WebDriverWait(driver, 15).until(  
            EC.presence_of_element_located((By.XPATH, "//button//div[text()='Alles afwijzen']")))
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, "//button//div[text()='Alles afwijzen']").click()
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, "(//textarea)[1]").click()
        driver.find_element(By.XPATH, "(//textarea)[1]").send_keys("tuincentrum.nl")
        driver.find_element(By.XPATH, "(//textarea)[1]").send_keys(Keys.ENTER)
        driver.implicitly_wait(2)
        assert driver.find_element(By.XPATH, "(//h3[contains(text(), 'Tuincentrum.nl')])[1]")
        driver.find_element(By.XPATH, "(//h3[contains(text(), 'Tuincentrum.nl')])[1]").click()
        driver.set_page_load_timeout(15)

        assert driver.find_element(By.XPATH, "(//button//span)[1]") # locate and click cookie button
        driver.find_element(By.XPATH, "(//button//span)[1]").click()
        driver.implicitly_wait(2)
        time.sleep(3)

        # locate searchquery and find organism.
        print("Scraping species.")
        for i in ln_names_dict.keys():
            if ln_names_dict[i][0] in plants_list:
                time.sleep(1)
                name = ln_names_dict[i][0]
                name2 = name.lower()
                name2 = name2.replace(" ", "-")
                
                assert driver.find_element(By.XPATH, "//input[@id='searchquery']")
                driver.find_element(By.XPATH, "//input[@id='searchquery']").click()
                action = ActionChains(driver)
                action.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
                driver.find_element(By.XPATH, input_search_token).send_keys(Keys.DELETE)
                driver.implicitly_wait(2)
                driver.find_element(By.XPATH, "//input[@id='searchquery']").send_keys(name2)
                driver.find_element(By.XPATH, "//input[@id='searchquery']").send_keys(Keys.ENTER)
                species_token = "//a[@class='h-full']//h3[contains(text(), '{}')]".format(ln_names_dict[i][0])

                try:    # This try except functions like an if/else condition; since selenium can't deal with if/else blocks I purposefully throw exceptions to continue the loop.
                    assert driver.find_element(By.XPATH, species_token) # 
                    ln_names_dict[i].append("Tuincentrum offers this species: " + "https://tuincentrum.nl/p/" + name)
                    counter += 1
                except NoSuchElementException:
                    # print("not here. next.")
                    pass

    except TimeoutError:
        print(TimeoutError)
        pass    
    except WebDriverException as e:
        print(e)
        pass
    driver.close()

    store_supply['Tuincentrum'][0] = counter
    if counter > 0:
        print("Found some species")
    else: 
        print("No species sold by Tuincentrum")
    return ln_names_dict, store_supply

def main_scraper(ln_names_dict, store_supply):
    """
    @input:     Takes ln_names_dict; a dict of all IAS with species_id as on waarnemingen.nl, and store_supply; a dict of all webshops with associated counts of offered species.   
    @output:    Updated ln_names_dict and store_supply with data from tuincentrum.nl
    @func:      Defines plants_list, a list of all invasive alien plants. 
                Then runs scrape_tuin, which returns updated versions of the dicts. 
                Returns these dicts back to main.
    """
    # plants_list is a list consisting of only plants, since tuincentrum does not sell any other types of species from the list that we're interested in. 
    plants_list = [ "Lampropeltis getula", "Celastrus orbiculatus", "Heracleum persicum", "Alternanthera philoxeroides", "Acacia saligna",
                   "Humulus scandens", "Hakea sericea", "Cenchrus setaceus", "Heracleum sosnowskyi", "Gunnera tinctoria", "Microstegium vimineum",
                   "Andropogon virginicus",  "Myriophyllum heterophyllum", "Ludwigia grandiflora", "Ludwigia peploides", "Asclepias syriaca", 
                   "Baccharis halimifolia", "Lysichiton americanus", "Eichhornia crassipes", "Cardiospermum grandiflorum", "Parthenium hysterophorus", 
                   "Prosopis juliflora", "Cabomba caroliniana", "Gymnocoronis spilanthoides", "Triadica sebifera", "Persicaria perfoliata", 
                   "Cortaderia jubata", "Ehrharta calycina", "Pueraria montana", "Lygodium japonicum", "Ailanthus altissima", "Elodea nuttallii",
                   "Heracleum mantegazzianum", "Hydrocotyle ranunculoides", "Impatiens glandulifera", "Myriophyllum aquaticum", "Persicaria wallichii",
                   "Pistia stratiotes", "Salvinia molesta", "Rugulopteryx okamurae", "Lagarosiphon major", "Lespedeza cuneata"]
    ln_names_dict, store_supply = scrape_tuin(ln_names_dict, store_supply, plants_list)
    ma_scraping_dict = ln_names_dict
    print(store_supply)
    return ma_scraping_dict, store_supply

if __name__ == "__main__":
    """
    @input:     Imports the MA scraping suite to use the read_file and MA_store_nrs functions.
    @output:    Returns a dict of links for each species found as well as a dict of stores with the associated number of species up for offer in each store. 
                Additionally outputs measured time passed of program. 
    @func:      Measures runtime of script and calls on other functions; controlling function. 
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
    store_supply = MA_scraping_suite.MA_store_nrs()
    ln_scraping_dict, store_supply = main_scraper(ln_names_dict, store_supply)

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)