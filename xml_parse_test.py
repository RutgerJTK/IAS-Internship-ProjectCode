import W_ScraperTest
import pandas as pd

from bs4 import BeautifulSoup as bs
from lxml import etree
from selenium.webdriver.common.by import By
from time import perf_counter
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser
import re
import time

def xml_parse(file_path):
    tree = ET.parse(file_path)
    attrib_list = []

    for elem in tree.iter():
        if 'href' in elem.attrib:
            attrib_list.append((str(elem.attrib)[2:-1]) + elem.text)

    return attrib_list

def find_general_table_attribs(attrib_list):   # To find regex patterns for all elements that will be used to fill the general species table on the homepage.
    print(attrib_list)
    pass

# ToDo: find out how to create tables with vscode. 
def find_unique_ias_attribs(attrib_list):    # To find regex patterns for each unique observation belonging to a single IAS. Each unique IAS requires a personal table.
    loc_token_crude = re.compile(".*locations.*[0-9].*")
    locations = list(filter(loc_token_crude.match, attrib_list))
    loc_token_full = re.compile("\\\G(.*').*")
    loc_token_province = re.compile("[href].*(\(.*?\)){1}$")
    print("These match:")
    print(locations)
    print("-"*80)
    provinces = []
    for count, value in enumerate(locations):
        obs_province = re.findall(loc_token_province, locations[count])
        provinces.append(obs_province)


if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    file_path  = "D:\School - all things school related\HAN Bio-informatica\Stage_Ru\Scraped_files\soup_8807"
    attrib_list = xml_parse(file_path)
    find_general_table_attribs(attrib_list)
    # find_unique_ias_attribs(attrib_list)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)
