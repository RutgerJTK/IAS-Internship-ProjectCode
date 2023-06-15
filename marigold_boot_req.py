from flask import Flask, render_template, request
import numpy as np
import json
import sys
import time 
import os
import re
import csv
import pandas as pd
import base64

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
        if file.endswith("info.txt"):
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
    filepath = "D:\\Project_IAS\\Scraped\\Scraped_MA\\Scraped_MA_supply.csv"
    supply_df = pd.read_csv(filepath)

    # convert the lists in the # of Species Offered and Species column to separate columns - and df editing.
    supply_df = pd.concat([supply_df[['Webstore']], supply_df['# of Species Offered and Species'].apply(pd.Series)], axis=1)
    num_cols = len(supply_df.columns) - 1
    col_names = ['Number of IAS sold by store, species names' ]
    col_names.insert(0, 'Webstore')
    supply_df.columns = col_names
    supply_df = supply_df.fillna('')
    Store_names = {
    'AnimalAttraction: ': 'AnimalAttraction: https://animalattraction.nl',
    'Blue-Lagoon': 'Blue-Lagoon: https://www.blue-lagoon.nl/',
    'Heevis': 'Heevis: https://www.heevis.nl/',
    'Welle Diertotaal': 'Welle Diertotaal: https://www.wellediertotaal.nl/c-5408932/actuele-dierenlijst', 
    'Marktplaats' : 'Marktplaats: https://www.marktplaats.nl',
    'Tuincentrum': 'Tuincentrum: https://tuincentrum.nl/',
    'AquaPlantsOnline.nl': 'AquaPlantsOnline.nl: https://www.aquaplantsonline.nl/aquariumplanten',
    'Reptilia': 'Reptilia: https://reptilia.nl/'
    }
    supply_df['Webstore'] = supply_df['Webstore'].replace(Store_names)
    supply_table_html = supply_df.to_html(index=False, classes='ui celled table')
    supply_table_html = supply_table_html.replace('[', '').replace(']', '').replace("'", '')
    return supply_table_html, supply_df

def get_cummul_plot():
    path = "D:\\Project_IAS\\Plotted_stats\\cummulative_count_plots_20y\\"
    files = os.listdir(path)
    cummul_img_dict = {}
    for file in files:
        with open((path + file), "rb") as cummul_img:
            print(file)
            file_id = re.search(r'\d+', file).group()
            cummul_img_encoded = base64.b64encode(cummul_img.read()).decode('utf-8')
            cummul_img_dict[file_id] = (cummul_img_encoded)

    for key, value in cummul_img_dict.items():
        truncated_value = value[:10] if len(value) > 10 else value
        print(f'{key}: {truncated_value}')
    return cummul_img_dict

def get_Province_counts_plots():
    path = "D:\\Project_IAS\\Plotted_stats\\Province_counts\\"
    files = os.listdir(path)
    Province_counts_dict = {}
    for file in files:
        with open((path + file), "rb") as cummul_img:
            print(file)
            file_id = re.search(r'\d+', file).group()
            Province_counts_dict_encoded = base64.b64encode(cummul_img.read()).decode('utf-8')
            Province_counts_dict[file_id] = (Province_counts_dict_encoded)

    for key, value in Province_counts_dict.items():
        truncated_value = value[:10] if len(value) > 10 else value
        print(f'{key}: {truncated_value}')
    return Province_counts_dict

def get_trends_plots():
    """
    To specify, this gets the plots data for 20 years. 
    """
    path = "D:\\Project_IAS\\Plotted_stats\\gt_vs_waarnemingen_plots_20y\\"
    files = os.listdir(path)
    gt_vs_waarnemingen_plots_dict = {}
    for file in files:
        with open((path + file), "rb") as cummul_img:
            print(file)
            file_id = re.search(r'\d+', file).group()
            gt_vs_waarnemingen_plots_dict_encoded = base64.b64encode(cummul_img.read()).decode('utf-8')
            gt_vs_waarnemingen_plots_dict[file_id] = (gt_vs_waarnemingen_plots_dict_encoded)

    for key, value in gt_vs_waarnemingen_plots_dict.items():
        truncated_value = value[:10] if len(value) > 10 else value
        print(f'{key}: {truncated_value}')
    return gt_vs_waarnemingen_plots_dict

def GT_info_prep():
    cummul_img_dict = get_cummul_plot()
    Province_counts_dict = get_Province_counts_plots()
    gt_vs_waarnemingen_plots_dict = get_trends_plots()
    return cummul_img_dict, Province_counts_dict, gt_vs_waarnemingen_plots_dict



def main():
    names_dict = read_ias_file()
    print(names_dict)
    static_url_path, gen_spec_info_dict = main_page_table_prep()
    RA_dict = RA_info_prep()
    supply_table_html, supply_df = read_MA_store_supply()
    cummul_img_dict, Province_counts_dict, gt_vs_waarnemingen_plots_dict = GT_info_prep()
    print("Returning all info.")
    return names_dict, static_url_path, gen_spec_info_dict, RA_dict, supply_table_html, supply_df, cummul_img_dict, Province_counts_dict, gt_vs_waarnemingen_plots_dict # This is what is returned to Marigold.py, which is required for website start-up. 

if __name__ == "__main__":
    main()