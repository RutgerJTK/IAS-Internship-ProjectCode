"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""
import Waarnemingen_scraper
import pandas as pd

from bs4 import BeautifulSoup as bs
from lxml import etree
from selenium.webdriver.common.by import By
from time import perf_counter
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser

def soup(paths_list):
    for path in paths_list:
        with open(path, 'rb') as f:
            page = f.read()
            f.close()
        print(type(page))
        dom = etree.HTML(str(page))     # This is an issue for large files. 
        print("am here")

        find_xpaths(dom, page)
    return dom

def find_xpaths(dom, page):
    """
    Defines 11 xpaths and gets those from the dom - the issue is that this might become deprecated as the site changes later. 
    input: dom from website/
    params: 11 xpaths for the tables/schema/csv, saved as 1 dict (each key containing 10 vars, vars can and will in multiple cases be lists).
    output: dict, or csv, anything usable as input to fill the database. 
    """
    pd_table = pd.read_html(page)
    t_frame = pd_table[0]
    print(t_frame)


if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    paths_list = ["D:\School - all things school related\HAN Bio-informatica\Stage_Ru\Scraped_files\soup_260",
    "D:\School - all things school related\HAN Bio-informatica\Stage_Ru\Scraped_files\soup_261",
    "D:\School - all things school related\HAN Bio-informatica\Stage_Ru\Scraped_files\soup_2252", "D:\School - all things school related\HAN Bio-informatica\Stage_Ru\Scraped_files\soup_152"]
    soup(paths_list)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)