"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

import data_selector

import datetime
import pandas as pd

import bs4 
from lxml import etree
import requests
import lxml
from lxml import html
from lxml import etree
import pandas as pd
import os
from time import perf_counter
from selenium import webdriver
from selenium.webdriver.common.by import By

def read_ias_file():
    """
    Note: this function might have to be moved to the ScrapingController script later on to make it more dynamic. 
    Opens the names:waarnemingen_codes file, turns it into a dict, returns it to 
    """
    names_dict = {}
    with open("ias_names_big_unedited") as f:       # "ias_names_big_unedited.txt" is the base text file to scrape for. 
        for line in f:
            line = line.strip("\n")
            line = line.split(": ")
            print(line)
            (key, val) = line[0], line[1]
            names_dict[str(key)] = val
    return names_dict


def write_waarnemingen_table_to_file(species, start_date, end_date, path):  # Scrapes all unique IAS info on observations per page and writes to file. 
    page_nr = 1
    page_end = False
    name = str(species)

    with open(path, 'ab') as f:
        root = "<ROOT> \n"
        f.write(root.encode())

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
    # except KeyboardInterrupt: # Niet handig om aan te hebben staan met testen. 
        #     print("Program was halted by user action, a restart is required.")

    with open(path, 'ab') as f:
        root = "</ROOT> \n"
        f.write(root.encode())

    f.close()

def waarnemingen_gen_info_writer(species, start_date, end_date, path):  # Scrapes general IAS info and writes to file. 
    name = str(species)
    print(">>>>>>> current file: ", name)
    print(name)
    
    with open(path + name + "_general_spec_info.txt", 'ab') as f2:
        try:
            url = "https://waarneming.nl/species/{}/observations/?date_after={}&date_before={}&province=&search=&advanced=on&user=&location=&sex=&is_validated=on&life_stage=&activity=&method=&page={}".format(name, start_date, end_date, 1)
            page = requests.get(url, timeout=15)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            
            dom = etree.HTML(str(soup))
            if dom.xpath("//h1//a//span[@class='species-common-name']"):    # Not all species have a dutch name registered.
                name_nl = dom.xpath("//h1//a//span[@class='species-common-name']")[0].text
                name_ln = dom.xpath("//h1//i[@class='species-scientific-name']")[0].text
            else:
                name_nl = "Heeft geen Nederlandse naam"
                name_ln = dom.xpath("//h1//i[@class='species-scientific-name']")[0].text

            spec_group = dom.xpath("(//a[@class='btn btn-default'])[1]")[0].text
            rarity = dom.xpath("(//span[@class='hidden-sm'])[1]")[0].text
            prevalence_status = dom.xpath("(//span[@class='hidden-sm'])[2]")[0].text
            gen_info = [name_ln, name_nl, spec_group, rarity, prevalence_status]

            for item in gen_info:
                f2.write(("%s\n" % item).encode())

        except TimeoutError:
            print("Site could not be reached. Try again later.")
        except requests.exceptions.HTTPError as err:
            print("There was an error requesting the site HTTP.", err)
        # except KeyboardInterrupt:
        #     print("Program was halted by user action, a restart is required.")
        except IOError as ioerr: 
            print("Error writng to file to file.", ioerr)

    f2.close()
        



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
        path = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Scraped_files\\soup_{}".format(species)
        paths_list.append(path)
        # write_waarnemingen_table_to_file(species_val, start_date, end_date, paths_list)   # Always has to be prioritized
        waarnemingen_gen_info_writer(species_val, start_date, end_date, path)
        # data_selector.soup(paths_list) # runs through all modules in data_selector.py


if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)

    scrape_master_class()   # Actual main enabling it to be used in modules. 

    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)
    print( "-" * 80, "\n", "Controller end, program done running", "\n","-" * 80)
