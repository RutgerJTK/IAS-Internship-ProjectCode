from time import perf_counter
import Waarnemingen_attributes
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import csv
sns.set_theme()

def get_names(ias_names):   # gets a dict of latin names coupled to waarnemingen IDs
    ln_names_dict = {}
    with open(ias_names) as f:
        content = f.readlines()
    
    for line in content:
        temp_dict = line.split(": ")
        temp_dict[1] = int(temp_dict[1].strip('\n'))
        ln_names_dict.update({temp_dict[1] : temp_dict[0]})
    return ln_names_dict


def trends_size_check(trends_file_name):
    scraped_trends_path = "D:\\Project_IAS\\Scraped\\Scraped_trends_20y\\"
    # scraped_trends_path = "D:\\Project_IAS\\Scraped\\Scraped_trends_5y\\"
    files = os.listdir(scraped_trends_path)
    if trends_file_name == "Tamias sibiricus":
        trends_file_name = "Eutamias sibiricus"
    for file in files:
        if trends_file_name in file:
            abs_path = scraped_trends_path + file

            if os.path.getsize(abs_path) > 1000:    # Filesize check to perform google trends vs observation analysis only for files which include a 
                return abs_path
            elif os.path.getsize(abs_path) < 100:
                abs_path = "too_small"
                return abs_path
            

def parse_trends(path, obs_dict):     # returns the google trends dict
    trends_dict = {}
    dates = list(obs_dict.keys())
    observations = list(obs_dict.values())
    norm = np.linalg.norm(observations)
    norm_parts_dict = {}
    obs_norm_array = observations/norm    

    with open(path) as f:
        content = f.readlines()[3:-1]
    
    for line in content: 
        line = line.strip("\n")
        line = line.split(",")
        # print(line[0][0:10])
        trends_dict[line[0]] = line[1]
    # print(trends_dict)

    for i in range(len(obs_norm_array)): 
        obs_norm_array[i] = obs_norm_array[i] * 100
        norm_parts_dict[dates[i]] = obs_norm_array[i]
    all_dates = list(set(trends_dict.keys()) | set(obs_dict.keys()))

    obs_plot_dict = {}      # In obs_plot_dict the key is the date, value one is the observation amount on that date, 
    for count, date in enumerate(all_dates):
        if date in obs_dict.keys():
            obs_plot_dict[date] = [int(norm_parts_dict[date])]
        else:
            obs_plot_dict[date] = [int(0)]  

    for count, date in enumerate(all_dates):
        if date in trends_dict.keys():
            trends_val = round(int(trends_dict[date]) / 100 * 40, 0)
            obs_plot_dict[date].append(trends_val)
        else: 
            obs_plot_dict[date].append(0)
    return obs_plot_dict


def plot_dict(obs_plot_dict, trends_file_name, file):
    file = file.split("_")[1]
    save_path = "D:\\Project_IAS\\Plotted_stats\\gt_vs_waarnemingen_plots_20y\\"
    save_plot = "province_obs_counts_{}_20y".format(trends_file_name+"_"+file)

    idx = obs_plot_dict.keys()
    # print(len(obs_plot_dict))
    df = pd.concat([pd.Series(obs_plot_dict[i]) for i in idx], axis =1).T
    df.index=idx
    df = df.reset_index()
    df.columns = ['Date', 'Waarnemingen.nl observations','Trends observations']     # Keys in the dict are all dates going back 20 years, values for column 1 and 2 are the number of waarnemingen.nl and google trends observations respectively.
    df = df.sort_values(by = 'Date')
    df.reset_index(inplace=True)
    
    # df.plot(x=1, y=[2, 3], kind="line", figsize=[15,5])
    # plt.xticks([0, df.shape[0]-1], [df['Date'].iloc[0], df['Date'].iloc[-1]])
    # plt.savefig((save_path + save_plot), dpi='figure', format=None,
    #             bbox_inches=None, pad_inches=0.1,
    #             facecolor='auto', edgecolor='auto',
    #             backend=None)
    # plt.close()

def write_dict(obs_plot_dict, file):
    print("Writing")
    print(len(obs_plot_dict))
    time_obs_list = []
    time_trends_list = []
    path = "D:\\Project_IAS\\Analysis_R\\Time_series\\"

    for key, values in obs_plot_dict.items():
        time_obs_list.append(values[0])
        time_trends_list.append(values[1])
    print(len(time_obs_list), len(time_trends_list))

    with open((path + "Time_series_" + file + ".csv"), mode="w", newline="") as f:
        writer = csv.writer(f)

        # Write the headers (optional)
        writer.writerow(["Waarnemingen.nl observations", "Trends data"])

        # Write the data from the lists
        for value1, value2 in zip(time_obs_list, time_trends_list):
            writer.writerow([value1, value2])

def main_plotter():
    filespath  = "D:\\Project_IAS\\Scraped\\Scraped_daily\\"
    files = os.listdir(filespath)
    path_to_names = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = get_names(path_to_names)
    for file in files:
        if not file.endswith(".txt") and not file.startswith("soup_940586"):
        # if file.endswith("soup_1490"):
            print("File: ", file)
            abs_path = (filespath + file) 
            element_list = Waarnemingen_attributes.xml_parse_elements(abs_path)
            if len(element_list) > 0: # These files have observations, for these observations we desire a comparison with google trends data. 
                id_file = int(file.split("_")[1])
                obs_dict = Waarnemingen_attributes.fill_obs_dict(element_list)  # Thus this function uses the soup ID call

                trends_file_name = ln_names_dict[id_file]
                trends_data_file = trends_size_check(trends_file_name) 
                if trends_data_file != "too_small":
                    obs_plot_dict = parse_trends(trends_data_file, obs_dict)
                    plot_dict(obs_plot_dict, trends_file_name, file)
                    write_dict(obs_plot_dict, file)   # This is only to write data away for the lagged time analysis. 

if __name__ == "__main__":
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    
    main_plotter()

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)