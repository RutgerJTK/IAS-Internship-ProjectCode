"""
Author: Rutger Kemperman
Goal of script: Plot the scraped data to check the correct data was scraped. (This checks out)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 

Note: probably add this to the daily mining suite, so this data is updated on the daily. 

Ideas corner:
- piechart for prominence in every province.
- ranked list showing the order of first observations (duplicates in list yes/no tbd) in each province.
- Late future goal of script: date of first observation (have database filled for past 50 years or so).


"""

import pandas as pd
import matplotlib.pyplot as plt
import Waarnemingen_attributes
import General_stats
import numpy as np
from time import perf_counter
from functools import reduce
import os
import time
import random

# def get_observation_stats():
#     files_path = "D:\\Project_IAS\\Scraped\\Scraped_files\\"
#     files = os.listdir(files_path)
#     for file in files: 
#         if not file.endswith(".txt"):
#             abs_path = (files_path + file)
#             attrib_list, tot_observed_indivs, indiv_nrs_list = Waarnemingen_attributes.xml_parse(abs_path)   # Actual main enabling it to be used in modules. 
#             nr_of_observations, timestamps, provinces = Waarnemingen_attributes.find_unique_ias_attribs(attrib_list)

#             plot_observations_stats(provinces, timestamps, file)
#             print(timestamps)
#             # time.sleep(1)

def plot_observations_stats(provinces, timestamps, file):
    save_path = "D:\\Project_IAS\\Plotted_stats\\Province_counts\\"
    save_pie = "province_obs_counts_{}".format(file)
    provinces_set = reduce(lambda re, x: re+[x] if x not in re else re, provinces, []) # Shows order of which each species was discovered/observed chronologically in the Netherlands. 
    cols = ["#4c88bf","#f1d409", "#04a86b", "#f8151c", "#d79004", "#87edc9", "#b62bb6", "#0f9d12", "#7e05fe", "#a06261", "#6c9a1f", "#d79004"]
    if len(provinces_set) > 0:
        count_provinces = pd.Series(provinces).value_counts()    
        list_prov_counts = count_provinces.tolist()
        plt.figure(figsize = (10,7))
        plt.title("Frequency of species observations per each province since {}".format(timestamps[-1]),  bbox={'facecolor':'1', 'pad':1})

        plt.pie(list_prov_counts, startangle=90,
                    wedgeprops = {"edgecolor" : "black", "linewidth": 4, 'width':1,
                        'linewidth': 0.5,
                        'antialiased': True},
                        autopct= '%1.1f%%',
                        colors=cols)
        plt.axis('equal')
        labels = provinces_set
        labels = [f'{l}: {s}' for l, s in zip(labels, list_prov_counts)]
        plt.legend(bbox_to_anchor=(-0.15, 0.25), loc='lower left', labels=labels, title="Counts per province")
        
        # plt.show()
        plt.savefig((save_path + save_pie), dpi='figure', format=None,
            bbox_inches=None, pad_inches=0.1,
            facecolor='auto', edgecolor='auto',
            backend=None)
        plt.close()


def main_trends_plotter(): # Stats to do: google trends vs     
    files_path = "D:\\Project_IAS\\Scraped\\Scraped_files\\"
    files = os.listdir(files_path)
    for file in files: 
        if not file.endswith(".txt"):
            abs_path = (files_path + file)
            attrib_list, tot_observed_indivs, indiv_nrs_list = Waarnemingen_attributes.xml_parse_attribs(abs_path)   # Actual main enabling it to be used in modules. 
            nr_of_observations, timestamps, provinces = Waarnemingen_attributes.find_unique_ias_attribs(attrib_list)
            element_list = Waarnemingen_attributes.xml_parse_elements(abs_path)
            if len(element_list) > 0:
                obs_dict = Waarnemingen_attributes.fill_obs_dict(element_list)

    print(obs_dict)


if __name__ == "__main__":
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)

    main_trends_plotter()

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)