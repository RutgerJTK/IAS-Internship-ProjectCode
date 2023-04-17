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


def scrape_cabi(ln_names_dict):
    options = uc.ChromeOptions() 
    # options.headless = True 
    driver = uc.Chrome(use_subprocess=True, options=options) 
    driver.get("https://www.datacamp.com/users/sign_in") 
    driver.maximize_window() 
    time.sleep(20) 
    driver.save_screenshot("datacamp.png") 
    driver.close()

    def main_scraper(ln_names_dict):
        ln_scraping_dict = scrape_cabi(ln_names_dict)
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
        
        
def main_scraper(ln_names_dict):
    ln_scraping_dict = scrape_cabi(ln_names_dict)
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