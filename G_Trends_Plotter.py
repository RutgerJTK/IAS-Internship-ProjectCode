"""
Author: Rutger Kemperman
Goal of script: Plot the scraped data to check the correct data was scraped. (This checks out)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 

Ideas corner:
- piechart for prominence in every province.
- ranked list showing the order of first observations (duplicates in list yes/no tbd) in each province.
- Late future goal of script: date of first observation (have database filled for past 50 years or so).

"""

import pandas as pd
import matplotlib.pyplot as plt
import Waarnemingen_attributes
import numpy as np
from time import perf_counter
from functools import reduce

def parse_trends():
    trends_df = pd.read_csv("GTrendsTest1.csv")

    return trends_df

def plot_trends(trends_df):
    trends_df.plot(kind='line', x='date', y=['Blockchain', 'Cardano', 'Ethereum'])
    plt.title('Trends data for ' + trends_df.columns[1] + ", " + trends_df.columns[2] + " and " + trends_df.columns[3] + " over the past 5 years" )
    plt.ylabel('Relative popularity of search trend')
    plt.show()
    pass

def get_observations_stats(provinces, timestamps):
    # fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    provinces_set = reduce(lambda re, x: re+[x] if x not in re else re, provinces, []) # Shows order of which each species was discovered/observed chronologically in the Netherlands. 
    # print(ans[0:5])
    print(provinces_set)
    count_provinces = pd.Series(provinces).value_counts()    
    list_prov_counts = count_provinces.tolist()
    print(list_prov_counts)

    
    pie = plt.pie(list_prov_counts, startangle=90,
                  wedgeprops = {"edgecolor" : "black",
                    'linewidth': 0.5,
                    'antialiased': True})
    plt.axis('equal')
    labels = provinces_set
    labels = [f'{l}: {s}' for l, s in zip(labels, list_prov_counts)]
    plt.legend(bbox_to_anchor=(0.85, 1), loc='upper left', labels=labels, title="Counts per province")
    plt.title("Frequency of species observations per each province since {}".format(timestamps[-1]),  bbox={'facecolor':'1', 'pad':5})
    plt.show()
    print(pie)
    return 


def main_trends_plotter(): # Stats to do: google trends vs 
    
    file = "D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\Scraped_files\\soup_260"
    attrib_list, tot_observed_indivs, indiv_nrs_list = Waarnemingen_attributes.xml_parse(file)   # Actual main enabling it to be used in modules. 
    nr_of_observations, timestamps, provinces = Waarnemingen_attributes.find_unique_ias_attribs(attrib_list)
    # print(indiv_nrs_list, timestamps)
    trends_df = parse_trends()
    # plot_trends(trends_df)
    get_observations_stats(provinces, timestamps)
    # print(timestamps[-1])



if __name__ == "__main__":
    main_trends_plotter()
