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

def scrape_reptilia():
    # """
    # @input:     ln_names_dict, store_supply, and plants_list, as defined by main.
    # @output:    ln_names_dict, store_supply, updated and filled according to scraped findings. 
    # @func:      Creates a firefox webdriver to scrape tuincentrum.nl. Searches page for every plant. Significant findings are added to the dict.  
    # """
    full_html = ""
    page_nr = 1
    next_page = True
    url_builder = "https://reptilia.nl/terrarium-dieren"
    try:
        while next_page == True:
            
            url = "{}/page/{}/".format(url_builder, str(page_nr))
            print("At part of the site: "+  url)
            page = requests.get(url, timeout=15)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            soup = str(soup)
            soup.strip("\n")
            matches = re.findall("next page-numbers", soup)
            full_html += soup
            if len(matches) == 1:
                print(matches)
                page_nr += 1
            elif len(matches) == 0 and url_builder == "https://reptilia.nl/terrarium-dieren":
                page_nr = 1 
                url_builder = "https://reptilia.nl/planten"
                print("plants!")
            else:
                print("Done.")
                next_page = False
            print(len(soup))

    except TimeoutError:
        print(TimeoutError)
        pass

    return full_html

def check_spec(ln_names_dict, store_supply, full_html):
    counter = 0
    print(len(full_html))
    for i in ln_names_dict.keys():
        print(ln_names_dict[i][0])
        matches = re.findall(ln_names_dict[i][0], full_html)
        if len(matches) > 0 :
            counter += 1
            name = ln_names_dict[i][0].lower()
            name = name.replace(" ", "-")
            url = "https://reptilia.nl" + name
            quote = "Species up for sale: " + url
            ln_names_dict[i].append(quote)
            print(matches)
    if counter < 1:
        print("nothing found.")
    store_supply["Reptilia"][0] = counter


    return ln_names_dict, store_supply


def main_scraper(ln_names_dict, store_supply):
    """
    @input:     Takes ln_names_dict; a dict of all IAS with species_id as on waarnemingen.nl, and store_supply; a dict of all webshops with associated counts of offered species.   
    @output:    Updated ln_names_dict and store_supply with data from tuincentrum.nl
    @func:      Defines plants_list, a list of all invasive alien plants. 
                Then runs scrape_tuin, which returns updated versions of the dicts. 
                Returns these dicts back to main.
    """

    full_html = scrape_reptilia()
    ln_names_dict, store_supply = check_spec(ln_names_dict, store_supply, full_html)
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