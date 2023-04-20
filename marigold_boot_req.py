from flask import Flask, render_template, request
import numpy as np
import json
import sys
import time 
import os
import re
import csv

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
                RA_dict[line[0]] = line[1:-1]   # line[0] is soup_id as key, line[1] is latin name, line[2:-1] are Risk Assessments.
    file.close()
    # print("-")
    # print(RA_dict.keys())
    # print(len(RA_dict["152"]))
    # print(RA_dict["152"][1:-1])
    # print(RA_dict["152"][0][3:-1])
    # print("--")
    # print(RA_dict["152"][2])
    # print(RA_dict["152"][3])
    # print(RA_dict["152"][4])
    # print(RA_dict["152"][5])
    print("Risk Assessment dictionary prepared.")
    return RA_dict

def main():
    names_dict = read_ias_file()
    static_url_path, gen_spec_info_dict = main_page_table_prep()
    RA_dict = RA_info_prep()
    print("Returning all info.")
    return names_dict, static_url_path, gen_spec_info_dict, RA_dict

if __name__ == "__main__":
    main()