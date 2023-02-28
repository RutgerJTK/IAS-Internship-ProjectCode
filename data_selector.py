"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""
import W_ScraperTest
import pandas as pd

from bs4 import BeautifulSoup as bs
from lxml import etree
from selenium.webdriver.common.by import By

def find_xpaths(dom, page):
    """
    Defines 11 xpaths and gets those from the dom - the issue is that this might become deprecated as the site changes later. 
    input: dom from website/
    params: 11 xpaths for the tables/schema/csv, saved as 1 dict (each key containing 10 vars, vars can and will in multiple cases be lists).
    output: dict, or csv, anything usable as input to fill the database. 
    """
    print(page)
    species_name = driver.find_element(By.XPATH, "//span[@class='species-common-name']", dom)
    print(spec_name_dutch)

def soup(paths_list):
    for path in paths_list:
        with open(path, 'rb') as f:
            page = f.read()
            f.close()
        dom = etree.HTML(str(page))
        find_xpaths(dom, page)
    return dom

if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    paths_list = ["D:\School - all things school related\HAN Bio-informatica\Stage_Ru\ProjectCode\soup_260",
    "D:\School - all things school related\HAN Bio-informatica\Stage_Ru\ProjectCode\soup_261",
    "D:\School - all things school related\HAN Bio-informatica\Stage_Ru\ProjectCode\soup_2252"]
    soup(paths_list)