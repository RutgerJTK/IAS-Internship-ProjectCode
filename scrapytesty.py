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

import os

def read_ias_file():
    """
    Note: this function might have to be moved to the ScrapingController script later on to make it more dynamic. 
    Opens the names:waarnemingen_codes file, turns it into a dict, returns it to 
    """
    names_dict = {}
    with open("ias_names_small.txt") as f:
        for line in f:
            line = line.strip("\n")
            line = line.split(": ")
            print(line)
            (key, val) = line[0], line[1]
            names_dict[str(key)] = val
    return names_dict

def write_waarnemingen_to_file(species, start_date, end_date, paths_list):
    name = str(species)
    url = "https://waarneming.nl/species/{}/observations/?date_after={}&date_before={}&province=&search=&advanced=on&user=&location=&sex=&is_validated=on&life_stage=&activity=&method=".format(name, start_date, end_date)
    page = requests.get(url)
    content = page.content
    dom = etree.HTML(str(content))
    a = content.find(By.XPATH("//span[@class='species-common-name']"))
    print(a)


def scrape_master_class(): # points to all other scraping classes, runs through each of them.
    end_date = datetime.date.today()
    start_date = end_date.replace(year=(end_date.year - 5))
    species = ""
    names_dict = read_ias_file()
    paths_list = []
    for species_val in names_dict.values():
        write_waarnemingen_to_file(species_val, start_date, end_date, paths_list)
    data_selector.soup(paths_list) # runs through all modules in data_selector.py
    # remove_files(paths_list)

if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    scrape_master_class()

