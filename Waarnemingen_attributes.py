"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Get all necessary 
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
import re
import time
import os
from functools import reduce

def xml_parse_attribs(file):
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

    tot_observed_indivs  = sum(indiv_nrs_list)      # Note: as a rule, tot_observed_indivs is ALWAYS equal to or higher than nr_of_observations (one cannot observe negative counts of observed individuals).
    return attrib_list, tot_observed_indivs, indiv_nrs_list

def xml_parse_elements(file):
    tree = ET.parse(file)
    element_list = []
    observed_indivs_nr_token = re.compile("([0-9]{1,6})")
    indiv_nrs_list = []
    # unique_obs_id = []
    # obs_date_full = []


    for elem in tree.iter():
        attribs_string = ""
        nr_observed_full = elem.findall("td")
        if len(nr_observed_full) > 1:
            unique_obs_id = list(nr_observed_full[0][0].attrib.values())[0]
            obs_date_full = nr_observed_full[0][0].text[0:10]
            if nr_observed_full[1].text != None:
                obs_number = nr_observed_full[1].text
                nr = re.findall(r"\d{1,10}", obs_number)[0]
            # if(nr_observed_full[2].text) != None:
            #     location_full = nr_observed_full[2].text
            # elif (nr_observed_full[2].text) == None:
            #     location_full = nr_observed_full[2][0].text
            
            attribs_string = (unique_obs_id + "," +obs_date_full+ ","+ nr)

            element_list.append(attribs_string), indiv_nrs_list.append(int(nr))
    tot_observed_indivs  = sum(indiv_nrs_list)      # Note: as a rule, tot_observed_indivs is ALWAYS equal to or higher than nr_of_observations (one cannot observe negative counts of observed individuals).
    
    return element_list

# ToDo: find out how to create tables with vscode. 
def find_unique_ias_attribs(attrib_list):    # To find regex patterns for each unique observation belonging to a single IAS. Each unique IAS requires a personal table.
    # print(len(attrib_list))
    loc_token_crude = re.compile(".*locations.*[0-9].*")
    locations = list(filter(loc_token_crude.match, attrib_list))
    loc_token_full = re.compile("\\\G(.*').*")
    loc_token_province = re.compile("[href].*(\(.*?\)){1}$")

    obs_id_token_crude = re.compile(".*observation.*")
    obs_ids = list(filter(obs_id_token_crude.match, attrib_list))
    obs_id_token = re.compile("(?<=observation\/).*")
    timestamp_token_crude = re.compile("(?=\/').*")
    datestamp_token = re.compile("^[0-9-]{10}")

    obs_daily_count_token = re.compile("^[0-9]{1,4}")
    obs_daily_counts = list(filter(obs_daily_count_token.match, attrib_list))
    ### Obs_id = date/timestamp of observations (not unique),
    ### obs_daily_counts = count of observations for each timestamp - not for each unique date.

    unique_observation_ids = [] 
    timestamps = []
    date_observations = {'date' : 'obs_day_sum'}
    datestamp = int()
    datestamps = []
    for count, value in enumerate(obs_ids):
        obs_id = re.findall(obs_id_token, obs_ids[count])
        obs_id = obs_id[0][2:]
        unique_observation_ids.append(obs_id)
        
        timestamp = re.findall(timestamp_token_crude, obs_ids[count])
        timestamp = timestamp[0][2:]
        datestamp = re.findall(datestamp_token, timestamp)[0]
        # print(timestamp, " and ", datestamp)
        datestamps.append(datestamp)
        timestamps.append(timestamp)
    # print(unique_observation_ids)
    provinces = []
    for count, value in enumerate(locations):
        obs_province = re.findall(loc_token_province, locations[count])
        obs_province = obs_province[0][1:-1]    # Remove brackets from province name --> (Zeeland) -> Zeeland = cleaner db storage. 
        provinces.append(obs_province)
    nr_of_observations = len(provinces)
    # print("list lengths: ", len(timestamps), len(unique_observation_ids), nr_of_observations)   # length of timestamps, unique_observation_ids, and nr_of_observations lists has to be identical. 
    nr_of_observations = 0
    dates_set = reduce(lambda re, x: re+[x] if x not in re else re, datestamps, []) # Shows order of which each species was discovered/observed chronologically in the Netherlands. 
    # print(len(dates_set),  len(obs_daily_counts))  
    return nr_of_observations, timestamps, provinces


def find_general_table_attribs(filespath, file, nr_of_observations, tot_observed_indivs):   # To find regex patterns for all elements that will be used to fill the general species table on the homepage.
    # filespath = "D:\\Project_IAS\\Stage_Ru\\Scraped_files\\"
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
    return gen_data

def fill_obs_dict(element_list):
    print(len(element_list))
    obs_dict = {}
    datestamp = ""
    datestamp_nr = 0

    for observation in element_list:
        observation = observation.split(",")
        if observation[1] not in obs_dict:
            obs_dict[observation[1]] = int(observation[2])
        else:
            obs_dict[observation[1]] += int(observation[2])
    print(sum(obs_dict.values()))
    return obs_dict

def gen_info_db_push(gen_data):
    """
    Input: gets a list with general species data
    Function: connects to db, writes list data to corresponding 
    """
    # print(gen_data)
    # print("-+"*40)
    pass


def master_extractor():
    filespath  = "D:\\Project_IAS\\Scraped\\Scraped_files\\"
    files = os.listdir(filespath)
    
    for file in files:
        if not file.endswith(".txt"):
            # print("+"*80)
            print(file)
            abs_path = (filespath + file) 
            attrib_list, tot_observed_indivs, indiv_nrs_list = xml_parse_attribs(abs_path)
            nr_of_observations, timestamps, provinces = find_unique_ias_attribs(attrib_list)   # File and attrib_list are corresponding equals here. 
            general_file = (file + "_general_spec_info.txt")
            find_general_table_attribs(filespath, general_file, nr_of_observations, tot_observed_indivs)

            element_list = xml_parse_elements(abs_path)
            if len(element_list) > 0:
                obs_dict = fill_obs_dict(element_list)
    return indiv_nrs_list, timestamps, obs_dict


if __name__ == "__main__":  # in case you would want to run this file on it's own, which will become an artefact function. 
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    
    master_extractor()

    t1_stop = perf_counter()
    print("Elapsed time during the whole program in seconds:",t1_stop-t1_start)
