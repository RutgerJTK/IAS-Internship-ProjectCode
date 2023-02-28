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
import lxml
from lxml import html
from lxml import etree
import pandas as pd
import glob
import ssl
import os

def read_ias_file():
    """
    Note: this function might have to be moved to the ScrapingController script later on to make it more dynamic. 
    Opens the names:waarnemingen_codes file, turns it into a dict, returns it to 
    """
    names_dict = {}
    with open("ias_names_sorted_big.txt") as f:
        for line in f:
            line = line.strip("\n")
            line = line.split(": ")
            print(line)
            (key, val) = line[0], line[1]
            names_dict[str(key)] = val
    return names_dict


def write_waarnemingen_to_file(species, start_date, end_date, paths_list):
    page_nr = 1
    page_end = False
    name = str(species)
    path = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Scraped_files\\soup_{}".format(species)
    paths_list.append(path)

    data =  ""
    while page_end == False:
        print(">>>>>>> current file: ", name)
        try:
            url = "https://waarneming.nl/species/{}/observations/?date_after={}&date_before={}&province=&search=&advanced=on&user=&location=&sex=&is_validated=on&life_stage=&activity=&method=&page={}".format(name, start_date, end_date, page_nr)
            page = requests.get(url, timeout=15)
            element_html = html.fromstring(page.content)
            table = element_html.xpath("//table[@class='table table-bordered table-striped']")
            table_tree = lxml.etree.tostring(table[0], method='xml')
            print("Page: ", str(page_nr))
            if element_html.xpath("//li//a[contains(text(), '{}')]".format(page_nr + 1)): 
                page_nr = page_nr + 1
                with open(path, 'ab') as f:
                    f.write(table_tree)
            else:
                page_end = True
                with open(path, 'ab') as f:
                    f.write(table_tree)
        except TimeoutError:
            print("Site could not be reached. Try again later.")
            continue
        except requests.exceptions.HTTPError as err:
            print("There was an error requesting the site HTTP.")
            continue
        except KeyboardInterrupt:
            print("Program was halted by user action, a restart is required.")
    f.close()


def remove_files(paths_list):
    for file in paths_list:
        try:
            if os.path.exists(file):
                os.remove(file)
        except FileNotFoundError:
                print("The file does not exist") 

def scrape_master_class(): # points to all other scraping classes, runs through each of them.
    end_date = datetime.date.today()
    start_date = end_date.replace(year=(end_date.year - 5))
    species = ""
    names_dict = read_ias_file()
    paths_list = []
    for species_val in names_dict.values():
        write_waarnemingen_to_file(species_val, start_date, end_date, paths_list)
    # data_selector.soup(paths_list) # runs through all modules in data_selector.py


if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    scrape_master_class()

