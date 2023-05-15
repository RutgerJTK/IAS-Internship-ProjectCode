from flask import Flask, render_template, request
import numpy as np
import json
import sys
import time 
import os
import re
import csv
import pandas as pd

def read_ias_file():
    """
    Note: this function might have to be moved to the ScrapingController script later on to make it more dynamic. 
    Opens the names:waarnemingen_codes file, turns it into a dict, returns it to 
    """
    filespath  = "D:\\Project_IAS\\ProjectCode\\"
    names_dict = {}
    with open(filespath + "ias_names_big_unedited") as f:       # "ias_names_big_unedited.txt" is the base text file to scrape for. 
        for line in f:
            line = line.strip("\n")
            line = line.split(": ")
            # print(line)
            (key, val) = line[0], line[1]
            names_dict[str(key)] = val
    print("Ias file read.")
    return names_dict
    

def main_page_table_prep():
    filespath  = "D:\\Project_IAS\\Scraped\\Scraped_files\\"
    files = os.listdir(filespath)
    static_url_path = "/Project_IAS/ProjectCode/static"
    gen_spec_info_dict = {}
    for file in files:
        if file.endswith(".txt"):
            abs_path = (filespath + file) 
            with open(abs_path, encoding="utf-8") as f:
                stripped_content = []
                content = f.readlines()
                for line in content:
                    line = line.strip("\n")
                    stripped_content.append(line)
            gen_spec_info_dict[stripped_content[0]] = stripped_content[1:-1]
            f.close()
    print("Main page table prepared.")
    return static_url_path, gen_spec_info_dict        

def RA_info_prep():
    RA_scraped_file = "D:\\Project_IAS\\Scraped\\Scraped_RA\\Scraped_RA_info.csv"
    RA_dict = {}
    with open(file=RA_scraped_file) as file:
        content = file.readlines()[1:-1]
        for line in content:
            if (len(line) > 2):
                line = line.strip("\n")
                line = line.split(",")
                RA_dict[line[0]] = line[1:]   # line[0] is soup_id as key, line[1] is latin name, line[2:-1] are Risk Assessments.
    file.close()
    print("Risk Assessment dictionary prepared.")
    return RA_dict

def read_MA_store_supply():
    """
    Note: this function might have to be moved to the ScrapingController script later on to make it more dynamic. 
    Opens the names:waarnemingen_codes file, turns it into a dict, returns it to 
    """
    print("Store supply")
    print("-"*80)

    filepath = "D:\\Project_IAS\\Scraped\\Scraped_MA\\Scraped_MA_supply.csv"
    supply_dict = {}
    supply_df = pd.read_csv(filepath)
    print("-"*80)


    # convert the lists in the # of Species Offered and Species column to separate columns
    supply_df = pd.concat([supply_df[['Webstore']], supply_df['# of Species Offered and Species'].apply(pd.Series)], axis=1)

    # rename the columns
    num_cols = len(supply_df.columns) - 1
    # col_names = ['Species ' + str(i) for i in range(num_cols)]
    col_names = ['Number of IAS sold by store, species names' ]
    col_names.insert(0, 'Webstore')
    supply_df.columns = col_names

    # convert NaN values to empty strings
    supply_df = supply_df.fillna('')
    supply_table_html = supply_df.to_html(index=False, classes='ui celled table')
    supply_table_html = supply_table_html.replace('[', '').replace(']', '').replace("'", '')
    # supply_table_html = supply_table_html.replace('[', '')

    # supply_table_html = supply_table_html.replace(']', '')
    # supply_table_html = supply_table_html.replace("'", '')


    print(supply_table_html)
    return supply_table_html
    

def main():
    names_dict = read_ias_file()
    static_url_path, gen_spec_info_dict = main_page_table_prep()
    RA_dict = RA_info_prep()
    supply_table_html = read_MA_store_supply()
    print("Returning all info.")
    return names_dict, static_url_path, gen_spec_info_dict, RA_dict, supply_table_html

if __name__ == "__main__":
    main()