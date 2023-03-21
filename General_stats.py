"""
Author: Rutger Kemperman
Goal of script: Plot the scraped data to check the correct data was scraped. (This checks out)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 

Ideas corner:
- piechart for prominence in every province.
- ranked list showing the order of first observations (duplicates in list yes/no tbd) in each province.
- Late future goal of script: date of first observation (have database filled for past 50 years or so).

- ideeen 15-3: 
    - lijst maken met alle geobserveerde species, geordend op basis van aantal observaties. 
    - 2 lijsten hebben van alle wel en niet geobserveerde species
    - 
    - This file will be incorporated into G_Trends_scraper.py. Will not have to be run on its own. 
"""

import pandas as pd
import matplotlib.pyplot as plt
import Waarnemingen_attributes
import numpy as np
from time import perf_counter
from functools import reduce
import os 
import json

def get_names(ias_names):   # gets names
    ln_names_dict = {}
    with open(ias_names) as f:
        content = f.readlines()
    
    for line in content:
        temp_dict = line.split(": ")
        temp_dict[1] = temp_dict[1].strip('\n')
        print(temp_dict)
        ln_names_dict.update({temp_dict[1] : temp_dict[0]})
    print(ln_names_dict)

def parse_trends(path):
    trends_df = pd.read_csv(path, skiprows=[0, 1])
    print(trends_df)
    return trends_df

def plot_trends(file, trends_df):
    print(trends_df)
    name = file.split("_")[1]
    name = name.strip(".csv")

    save_path = "D:\\Project_IAS\\Plotted_stats\\gt_vs_waarneming_plots\\"
    save_graph = "obs_counts_{}".format(name)


    y_name = trends_df.columns[1]

    trends_df.plot(kind='line', x='Week', y=y_name)
    plt.title('Trends data for ' + trends_df.columns[1] +"\n" + " over the past 5 years" )
    plt.ylabel('Relative popularity of search trend')
    plt.show()
    plt.legend(trends_df.columns[1] + "from google trends")
    # plt.savefig((save_path + save_graph), dpi='figure', format=None,
    #     bbox_inches=None, pad_inches=0.1,
    #     facecolor='auto', edgecolor='auto',
    #     backend=None)
    # plt.close()
  

def get_stats_master_class(): # Stats to do: google trends vs 
    # ToDo:
    # Make a dict for dutch/latin name : waarnemingen.nl value so they can be coupled.
    # plan out this main better: each file has to run coupled by name, start comparison with waarnemingen_attributes side. 

    filespath_trend = "D:\\Project_IAS\\Scraped\\Scraped_trends_5y\\"
    ias_names = "D:\\Project_IAS\\ProjectCode\\ias_names_file.txt"
    trend_files = os.listdir(filespath_trend)
    get_names(ias_names)

    for file in trend_files:
        abs_path = str(filespath_trend + file)
        if os.path.getsize(abs_path) > 1000:    # Filesize check to perform google trends vs observation analysis only for 
    #         indiv_nrs_list, timestamps, obs_dict, file2 = Waarnemingen_attributes.master_extractor()
    #         print(file, file2)
            trends_df = parse_trends(abs_path)  
            plot_trends(file, plot_trends)

if __name__ == "__main__":
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    
    get_stats_master_class()

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)