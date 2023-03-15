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

def parse_trends(path):
    trends_df = pd.read_csv(path, skiprows=[0, 1])
    return trends_df

def plot_trends(file, trends_df):
    name = file.split("_")[1]
    name = name.strip(".csv")

    save_path = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Plotted_stats\\gt_vs_waarneming_plots\\"
    save_graph = "province_obs_counts_{}".format(name)

    y_name = trends_df.columns[1]

    trends_df.plot(kind='line', x='Week', y=y_name)
    plt.title('Trends data for ' + trends_df.columns[1] +"\n" + " over the past 5 years" )
    plt.ylabel('Relative popularity of search trend')
    # plt.show()
    plt.legend(trends_df.columns[1] + "from google trends")
    plt.savefig((save_path + save_graph), dpi='figure', format=None,
        bbox_inches=None, pad_inches=0.1,
        facecolor='auto', edgecolor='auto',
        backend=None)
    plt.close()
  


def get_stats_master_class(): # Stats to do: google trends vs 
    trends_df =  parse_trends(file)
    plot_trends(trends_df)
    -------------------------------------------
    filespath = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Scraped_trends_5y\\"
    files = os.listdir(filespath)
    for file in files:
        abs_path = str(filespath + file)
        if os.path.getsize(abs_path) > 1000:    # Filesize check to perform google trends vs observation analysis only for 
            trends_df = parse_trends(abs_path)  
            plot_trends(file, trends_df)        

if __name__ == "__main__":
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    
    get_stats_master_class()

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)