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
import seaborn as sns
sns.set_theme()

def plot_observations_stats(provinces, timestamps, file):
    save_path = "D:\\Project_IAS\\Plotted_stats\\Province_counts\\"
    save_pie = "province_obs_counts_{}".format(file)
    provinces_set = reduce(lambda re, x: re+[x] if x not in re else re, provinces, []) # Shows order of which each species was discovered/observed chronologically in the Netherlands. 
    cols = ["#4c88bf","#f1d409", "#04a86b", "#f8151c", "#d79004", "#87edc9", "#b62bb6", "#0f9d12", "#7e05fe", "#a06261", "#6c9a1f", "#d79004"]
    if len(provinces_set) > 0:
        count_provinces = pd.Series(provinces).value_counts()    
        list_prov_counts = count_provinces.tolist()
        # plt.figure(figsize = (10,7))
        # plt.title("Frequency of species observations per each province since {}".format(timestamps[-1]),  bbox={'facecolor':'1', 'pad':1})

        # plt.pie(list_prov_counts, startangle=90,
        #             wedgeprops = {"edgecolor" : "black", "linewidth": 4, 'width':1,
        #                 'linewidth': 0.5,
        #                 'antialiased': True},
        #                 autopct= '%1.1f%%',
        #                 colors=cols)
        # plt.axis('equal')
        # labels = provinces_set
        # labels = [f'{l}: {s}' for l, s in zip(labels, list_prov_counts)]
        # plt.legend(bbox_to_anchor=(-0.15, 0.25), loc='lower left', labels=labels, title="Counts per province")
        
        # # plt.show()
        # plt.savefig((save_path + save_pie), dpi='figure', format=None,
        #     bbox_inches=None, pad_inches=0.1,
        #     facecolor='auto', edgecolor='auto',
        #     backend=None)
        plt.close()
        print("here")

def plot_obs_cummulative(timestamps, indiv_nrs_list, file):
    """
    Note for interpretation of the graphs: Due to reading order, the graphs are reversed to some extent. The last datapoint in the graph resembles the total amount of observations counting back to that point. 
    """
    save_path = "D:\\Project_IAS\\Plotted_stats\\cummulative_count_plots_20y\\"
    save_chart = "cummulative_obs_counts_{}".format(file)
    count2 = 0
    cummul_list = []
    print("Counting for: ", file)
    for count, value in enumerate(indiv_nrs_list):
        count2 += count
        cummul_list.append(count2)


    print(cummul_list[-1])
    print("-"*80)
    print(timestamps[0], timestamps[-1])
    # print(cummul_list[-5:])

    print(len(cummul_list), len(timestamps))

    # cummul_list = cummul_list[::-1]
    # timestamps = timestamps[::-1]

    fig, ax = plt.subplots()

    ax.scatter(timestamps, cummul_list, s=1)
    x_ticks = [timestamps[0], (timestamps[-1] + " 00:00")]
    plt.xticks(x_ticks)
    # Assuming you have the last data point coordinates (last_x, last_y) in your plot
    last_x = timestamps[-1]
    last_y = cummul_list[-1]
    # try:
    #     # Calculate the step size for the x-axis ticks
    #     percentiles = np.arange(10, 100, 10)
    #     indices = np.percentile(np.arange(len(timestamps)), percentiles)
    #     x_ticks = [timestamps[int(index)] for index in indices]

    #     # Set the x-axis ticks
    #     plt.xticks(x_ticks, rotation=45)

    # except ZeroDivisionError:
    #     plt.xticks([timestamps[0], timestamps[-1]], rotation=45)
    #     ax = plt.gca()
    #     ax.invert_xaxis()  # Invert the x-axis ticks

    # Annotate the last data point with a number
    plt.annotate(f'{last_y}', (last_x, last_y), xytext=(5, 10),
                textcoords='offset points', ha='center', fontsize=10)
    plt.savefig((save_path + save_chart), dpi=300, bbox_inches='tight')
    plt.close()


def main_trends_plotter(): # Stats to do: google trends vs     
    files_path = "D:\\Project_IAS\\Scraped\\Scraped_daily\\"
    files = os.listdir(files_path)
    for file in files: 
        if not file.endswith(".txt"): 
        # if file.startswith("soup_152") and not file.endswith(".txt"):
            abs_path = (files_path + file)
            print("Busy with:", abs_path)
            attrib_list, tot_observed_indivs, indiv_nrs_list = Waarnemingen_attributes.xml_parse_attribs(abs_path)   # Actual main enabling it to be used in modules. 
            nr_of_observations, timestamps, provinces = Waarnemingen_attributes.find_unique_ias_attribs(attrib_list)
            element_list = Waarnemingen_attributes.xml_parse_elements(abs_path)
            gen_info = Waarnemingen_attributes.get_gen_info(files_path + file + "_general_spec_info.txt")
            print("Name: " + gen_info[0])
            if len(element_list) > 0:
                obs_dict = Waarnemingen_attributes.fill_obs_dict(element_list)
            # plot_observations_stats(provinces, timestamps, file)    # Don't remove this; it won't overwrite the figure if it is already saved under that name. ToDo: fix this. 
            if len(indiv_nrs_list) > 0:
                plot_obs_cummulative(timestamps, indiv_nrs_list, file)
            else:
                print("0")


if __name__ == "__main__":
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)

    main_trends_plotter()

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)