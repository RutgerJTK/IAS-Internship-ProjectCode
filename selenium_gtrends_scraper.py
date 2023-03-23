"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from google trends (and maybe store it in a database) for assorted species. 
Future goal of script: store data in database so it can be updated later. 
"""

import time
import datetime
import pandas as pd
import os
from time import perf_counter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_name(abs_path):
    """
    @Input: abs_path = path to file to be opened.
    @params: gets latin and dutch species name from file. 
    @Output: returns latin and dutch species names.
    """
    with open(abs_path) as f:
        info =  f.readlines()[0:2][0:2]
        name_latin = info[0].strip("\n")
        name_dutch = info[1].strip("\n")
    return name_latin, name_dutch    


def sel_scrape_trends(name_dutch):
    print("start scraping")
    options = webdriver.FirefoxOptions();
    options.add_argument('headless');
    
    url = "https://trends.google.com/home"

    driver = webdriver.Firefox()
    driver.get(url)
    # time.sleep(2)

    assert "Google" in driver.title
    assert driver.find_element(By.XPATH, "//input")

    driver.find_element(By.XPATH, '(//span[@class="VfPpkd-vQzf8d"])[4]').click()
    time.sleep(2)
    assert driver.find_element(By.XPATH, '(//input[@class="ng-pristine ng-untouched ng-valid ng-not-empty ng-valid-required flex"])')
    driver.find_element(By.XPATH, '(//input[@class="ng-pristine ng-untouched ng-valid ng-not-empty ng-valid-required flex"])').click()
    webElement = driver.find_element(By.XPATH, '(//input[@class="ng-pristine ng-untouched ng-valid ng-not-empty ng-valid-required flex"])').send_keys(name_dutch, Keys.RETURN)

    # time.sleep(3)
    driver.find_element(By.XPATH, "(//div[@class='_md-text' and contains(text(), 'Afgelopen dag')])[1]").click()
    # driver.find_element(By.XPATH, "(//div[@class='_md-text' and contains(text(), '2004 - heden')])[1]").click()
    driver.find_element(By.XPATH, "(//div[@class='_md-text' and contains(text(), 'Afgelopen vijf jaar')])[1]").click()
    time.sleep(2)
    if driver.find_element(By.XPATH, "(//div[@class='cookieBarInner'])"):
        driver.find_element(By.XPATH, "//a[@class='cookieBarButton cookieBarConsentButton']").click()
    driver.find_element(By.XPATH, "(//i[@class='material-icons-extended gray' and contains(text(),'file_download')])[1]").click()
    driver.close()
    return 
    
def rename_file(downloads_path, name_latin):
    # trends_dir = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Scraped_trends\\"
    trends_dir_5y = "D:\\Project_IAS\\Scraped\\Scraped_trends_5y\\"

    files = os.listdir(downloads_path)
    for file in files:
        abs_path = str(downloads_path + file)
        if file == ("multiTimeline.csv"):
            os.rename(abs_path, (trends_dir_5y + "multiTimeline_{}.csv".format(name_latin)))
            print(file)


def GT_master_class(): # points to all other scraping classes, runs through each of them.
    filespath  = "D:\\Project_IAS\\Scraped\\Scraped_files\\"
    downloads_path = "D:\\DATA\\Downloads\\"
    files = os.listdir(filespath)
    for file in files:
        if file.endswith("_general_spec_info.txt"):    
            abs_path = str(filespath + file)      
            name_latin, name_dutch = get_name(abs_path)
            if name_dutch != "Heeft geen Nederlandse naam": # Sommige species kennen geen nederlandse naam. 
                sel_scrape_trends(name_dutch) 
                rename_file(downloads_path, name_latin)
            else: 
                sel_scrape_trends(name_latin) 
                rename_file(downloads_path, name_latin)
    pass


if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    
    GT_master_class()
    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)