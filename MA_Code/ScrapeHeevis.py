"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all marketdata from heevis.
Inner workings: All species for sale are scraped, these are compared to the invasive species list. If any invasive species are being sold, the site link will be added to that species profile.

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
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException



def scrape_heevis(ln_names_dict, heevis_list, store_supply):
    print("Yo")
    print(store_supply)
    teller = 0
    teller2 = 0
    options = Options() 
    options.headless = True     # options.add_argument('--headless')
    url = "https://www.heevis.nl/"
    driver = webdriver.Firefox(options=options)
    # driver = uc.Chrome(use_subprocess=True, options=options, version_main="112.0.5615.139") 
    cookie_token = "//label[@class='allow-all-cookies-button']//span[contains(text(), 'Begrepen')]"
    input_search_token = "//div[@class='control']//input[@id='search']"
    try:
        print("time to get url:")
        driver.get(url)
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, cookie_token)))
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, cookie_token).click()
        driver.implicitly_wait(1)
        
        for i in ln_names_dict.keys():
            if ln_names_dict[i][0] in heevis_list:
                print(ln_names_dict[i][0])
                assert driver.find_element(By.XPATH , input_search_token)
                driver.find_element(By.XPATH, input_search_token).click()
                action = ActionChains(driver)
                action.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
                driver.find_element(By.XPATH, input_search_token).send_keys(Keys.DELETE)
                time.sleep(1)
                driver.find_element(By.XPATH , input_search_token).send_keys(ln_names_dict[i][0])
                driver.find_element(By.XPATH , input_search_token).send_keys(Keys.ENTER)
                time.sleep(2)
                driver.implicitly_wait(2)
            
                try:
                    assert driver.find_element(By.XPATH, "//div[@class='message notice']//div")
                    element = driver.find_element(By.XPATH, "//div[@class='message notice']//div").text
                    if element != "Uw zoekopdracht heeft geen resultaten opgeleverd.":
                        print(ln_names_dict[i][0] + " : " + str(element))
                        cur_url = driver.current_url
                        print(cur_url)
                        teller2 +=1
                except NoSuchElementException:  # These are the results which we in fact want; perhaps we should shift this around since this is the prefered output. 
                    print("Got a certain hit for: " + ln_names_dict[i][0])
                    assert driver.find_element(By.XPATH, "//div[@class='message-success success message']")
                    assert driver.find_element(By.XPATH, "//h1//span")
                    item_title = driver.find_element(By.XPATH, "//h1//span").text
                    if ln_names_dict[i][0] in item_title:
                        cur_url = driver.current_url
                        quote = "Heevis sells this species: " + cur_url
                        ln_names_dict[i].append(quote)
                        print(cur_url)
                    
                    teller2 +=1

                print("-+"*  35)
                teller += 1
        print(teller)
        print(teller2)

    except TimeoutError:
        print(TimeoutError)
        pass    
    except WebDriverException as e:
        print(e)
        pass
    driver.close()

    return ln_names_dict, teller2




def main_scraper(ln_names_dict, store_supply):
    # Since heevis mainly offers aquatic and marine life related good and species, the list to search this website with was trimmed down to the following species:
    heevis_list = ["Lampropeltis getula", "Procambarus clarkii", "Celastrus orbiculatus", "Heracleum persicum", "Alternanthera philoxeroides", 
                   "Acacia saligna", "Trachemys scripta elegans", "Humulus scandens", "Hakea sericea", "Cenchrus setaceus", "Heracleum sosnowskyi",
                   "Gunnera tinctoria", "Microstegium vimineum", "Andropogon virginicus", "Faxonius virilis", "Eriocheir sinensis", "Myriophyllum heterophyllum",
                   "Ludwigia grandiflora",  "Ludwigia peploides", "Lithobates catesbeianus", "Asclepias syriaca", "Baccharis halimifolia", "Gambusia holbrooki", 
                   "Lysichiton americanus",  "Eichhornia crassipes", "Fundulus heteroclitus", "Cardiospermum grandiflorum", "Parthenium hysterophorus",
                   "Prosopis juliflora",  "Cabomba caroliniana",  "Pacifastacus leniusculus", "Xenopus laevis", "Ameiurus melas", "Lepomis gibbosus", 
                   "Pseudorasbora parva", "Perccottus glenii",  "Trachemys scripta scripta", "Trachemys scripta troostii", "Gymnocoronis spilanthoides",
                   "Triadica sebifera", "Persicaria perfoliata", "Cortaderia jubata", "Ehrharta calycina", "Pueraria montana", "Lygodium japonicum", 
                   "Procambarus virginalis", "Faxonius rusticus", "Gambusia affinis", "Plotosus lineatus", "Ailanthus altissima", "Elodea nuttallii", 
                   "Heracleum mantegazzianum", "Hydrocotyle ranunculoides", "Impatiens glandulifera", "Myriophyllum aquaticum", "Persicaria wallichii", 
                   "Pistia stratiotes", "Salvinia molesta", "Channa argus", "Morone americana",  "Arthurdendyus triangulatus", "Rugulopteryx okamurae", 
                   "Lagarosiphon major", "Faxonius limosus", "Lespedeza cuneata", "Cipangopaludina chinensis", "Rhinella marina"]

    ln_names_dict, teller2 = scrape_heevis(ln_names_dict, heevis_list, store_supply)
    store_supply['Heevis'] = teller2
    ln_scraping_dict = ln_names_dict
    print(ln_scraping_dict)
    return ln_scraping_dict, store_supply

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
    store_supply = MA_scraping_suite.MA_store_nrs()
    ln_scraping_dict, store_supply = main_scraper(ln_names_dict, store_supply)
    

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)