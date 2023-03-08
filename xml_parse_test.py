"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Get all necessary 
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

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
import os

def xml_parse(file):
    tree = ET.parse(file)
    attrib_list = []
    observed_indivs_nr_token = re.compile("([0-9]{1,6})")
    indiv_nrs_list = []
    
    for elem in tree.iter():
        nr_observed_full = elem.findall("td")
        if len(nr_observed_full) > 1:
            nr_observed_full = (nr_observed_full[1].text)
            nr_observed = observed_indivs_nr_token.findall(nr_observed_full)
            indiv_nrs_list.append(int(nr_observed[0]))
        if 'href' in elem.attrib:
            attrib_list.append((str(elem.attrib)[2:-1]) + elem.text)

    tot_observed_indivs  = sum(indiv_nrs_list)

    return attrib_list, tot_observed_indivs

# ToDo: find out how to create tables with vscode. 
def find_unique_ias_attribs(attrib_list):    # To find regex patterns for each unique observation belonging to a single IAS. Each unique IAS requires a personal table.
    # print(attrib_list[0:10])
    loc_token_crude = re.compile(".*locations.*[0-9].*")
    locations = list(filter(loc_token_crude.match, attrib_list))
    loc_token_full = re.compile("\\\G(.*').*")
    loc_token_province = re.compile("[href].*(\(.*?\)){1}$")

    obs_id_token_crude = re.compile(".*observation.*")
    obs_ids = list(filter(obs_id_token_crude.match, attrib_list))
    obs_id_token = re.compile("(?<=observation\/).*")
    timestamp_token_crude = re.compile("(?=\/').*")
   
    unique_observation_ids = [] 
    timestamps = []
    for count, value in enumerate(obs_ids):
        obs_id = re.findall(obs_id_token, obs_ids[count])
        obs_id = obs_id[0][2:]
        unique_observation_ids.append(obs_id)

        timestamp = re.findall(timestamp_token_crude, obs_ids[count])
        timestamp = timestamp[0][2:]
        timestamps.append(timestamp)
    
    provinces = []
    for count, value in enumerate(locations):
        obs_province = re.findall(loc_token_province, locations[count])
        obs_province = obs_province[0][1:-1]    # Remove brackets from province name --> (Zeeland) -> Zeeland = cleaner db storage. 
        provinces.append(obs_province)
    nr_of_observations = len(provinces)
    print("list lengths: ", len(timestamps), len(unique_observation_ids), nr_of_observations)
    return nr_of_observations


def find_general_table_attribs(filespath, file, nr_of_observations, tot_observed_indivs):   # To find regex patterns for all elements that will be used to fill the general species table on the homepage.
    # filespath = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Scraped_files\\"
    # files = os.listdir(filespath)

    # Loops over files in directory to select general info files, reads them, parses info to list which it returns. List is ready for db insertion. 
    gen_data = []
    abs_path = filespath + file
    content = open(abs_path).readlines()
    for line in content:
        line = line.strip("\n")
        gen_data.append(line)
    gen_data.append(nr_of_observations)     # Appending total number of times species was observed in the Netherlands. 
    gen_data.append(tot_observed_indivs)    # Appending total number of observed individuals in complete timeperiod. 
    gen_info_db_push(gen_data)
    # print(gen_data)

def gen_info_db_push(gen_data):
    """
    Input: gets a list with general species data
    Function: connects to db, writes list data to corresponding 
    """
    print(gen_data)


def master_extractor():
    filespath  = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Scraped_files\\"
    files = os.listdir(filespath)
    
    "------------------------------ Test ------------------------------"
    # temp_path = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Scraped_files\\soup_8807"
    # attrib_list = xml_parse(temp_path)
    # nr_of_observations = find_unique_ias_attribs(attrib_list)
    "------------------------------ Test ------------------------------"
    
    for file in files:
        if not file.endswith(".txt"):
            print("+"*80)
            abs_path = (filespath + file) 
            print(file)
            attrib_list, tot_observed_indivs = xml_parse(abs_path)
            nr_of_observations = find_unique_ias_attribs(attrib_list)   # File and attrib_list are corresponding equals here. 
            general_file = (file + "_general_spec_info.txt")
            find_general_table_attribs(filespath, general_file, nr_of_observations, tot_observed_indivs)


if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    
    master_extractor()

    t1_stop = perf_counter()
    print("Elapsed time during the whole program in seconds:",t1_stop-t1_start)
