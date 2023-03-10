"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

import data_selector

import datetime
import pandas as pd

from bs4 import BeautifulSoup
from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from pytrends.request import TrendReq
import os
from time import perf_counter

def get_name(abs_path):
    """
    @Input: abs_path = path to file to be opened.
    @params: gets latin and dutch species name from file. 
    @Output: returns latin and dutch species names.
    """
    with open(abs_path) as f:
        info =  f.readlines()[0:2][0]
        name_latin = info[0]
        name_dutch = info[1]

    return name_latin, name_dutch

def get_trends(abs_path, name_latin, name_dutch):
    kw_list_ln = [name_latin]
    kw_list_nl = [name_dutch]
    pytrends = TrendReq(hl='du-NL', tz=360)
    # pytrends.build_payloadkw_list = []
    pytrends.build_payload(kw_list_nl, cat=0, timeframe='today 5-y', geo='Nederland', gprop='')
    data_nl = pytrends.interest_over_time()
    print(data_nl)
    # print(pytrends) 


def GT_master_class(): # points to all other scraping classes, runs through each of them.
    filespath  = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Scraped_files\\"
    files = os.listdir(filespath)
    file = "soup_260"
    gen_file_name = "_general_spec_info.txt"
    end_date = datetime.date.today()
    start_date = end_date.replace(year=(end_date.year - 5))
    abs_path = str(filespath + file + gen_file_name)
    name_latin, name_dutch = get_name(abs_path)
    get_trends(abs_path, name_latin, name_dutch)

if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    
    GT_master_class()
    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)
