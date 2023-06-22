import re
import seaborn as sns
sns.set_theme()
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import pandas as pd
import numpy as np

def read_RA():
    path = "D:\\Project_IAS\\Scraped\\Scraped_RA\\Scraped_RA_info2.csv" # New and updated on 21-6-2023. 
    with open(path,  "r") as f:
        content = f.read()

    nobanis = re.findall("Features factsheet on Nobanis", content)
    yield_cabi = re.findall("CABI yielded", content)
    datasheets_cabi = re.findall("Datasheet by CABI", content)
    fws_data = re.findall("FWS U.S. ", content)
    isna_no_RA = re.findall("ISNA - no RA", content)
    isna_RA = re.findall("ISNA - has RA", content)
    NNSSGB = re.findall("Has RA on NNSS Great Britain", content)
    Glansis = re.findall("on Glansis", content)
    INPN = re.findall("on INPN", content)
    BDI = re.findall("Registered on BDI", content)
    Michigan = re.findall("On Michigan's watchlist", content)
    GISD = re.findall("iucngisd", content)

    ra_dict = {
        "nobanis" : len(nobanis), 
        "yield_cabi" : len(yield_cabi),
        "datasheets by cabi": len(datasheets_cabi), 
        "datasheets by FWS" : len(fws_data),
        "isna_no_RA" : len(isna_no_RA),
        "isna_RA" : len(isna_RA), 
        "NNSSGB" : len(NNSSGB), 
        "Glansis" : len(Glansis),
        "INPN" : len(INPN), 
        "BDI" : len(BDI), 
        "Michigan" : len(Michigan), 
        "GISD" : len(GISD)
    }

    f.close()
    # print(ra_dict)
    return ra_dict, content


def plot_ra(ra_dict):
    ra_dict = dict(sorted(ra_dict.items(), key=lambda x: x[1]))
    labels = list(ra_dict.keys())
    values = list(ra_dict.values())
    # cm.get_cmap generates a colour map which is nice to distinguish the bars. 
    cmap = cm.get_cmap('YlGnBu')
    colors = [cmap(i / len(labels)) for i in range(len(labels))]
    plt.bar(labels, values, color=colors)
    plt.xlabel('Risk Assessment Database')
    plt.ylabel('Number of links to species info')
    plt.xticks(rotation=90)

    # And to add values above each bar
    for i, value in enumerate(values):
        plt.text(i, value + 1, str(value), ha='center', va='bottom')

    plt.tight_layout()
    # plt.show()

def read_ias():
    """
    Note: this function might have to be moved to the ScrapingController script later on to make it more dynamic. 
    Opens the names:waarnemingen_codes file, turns it into a dict, returns it to main. 
    """
    filespath  = "D:\\Project_IAS\\ProjectCode\\"
    names_dict = {}
    with open(filespath + "ias_names_big_unedited") as f:       # "ias_names_big_unedited.txt" is the base text file to scrape for. 
        for line in f:
            line = line.strip("\n")
            line = line.split(": ")
            # print(line)
            (key, val) = line[1], line[0]   # Turn this around, since I want the ID to be comparative factor. 
            names_dict[str(key)] = val
    print("Ias file read.")
    # print(names_dict)
    f.close()
    return names_dict

def read_gen_info():
    path = "D:\\Project_IAS\\ProjectCode\\ias_gen_info.txt"
    general_info = { }

    with open(path,  "r") as f:
        content = f.read() 
    
    content = content.split("\n")
    # content = content[:-1]
    for i in range(len(content)):
        content[i] = content[i].replace("Ã«", "ë")
        content[i] = content[i].strip("\n")
        content[i] = content[i].split(": ")
        content[i][1] = content[i][1].split(",")
        general_info[content[i][0]] = content[i][1]
    # print(general_info)
    return general_info

def calc_RA_vals(general_info, content, ra_dict):       # Although dirty, I kinda like it. 
    content = content.split("\n")
    content = content[1:]
    clade_count_dict = {
        "Plants" : [0, [], [], 0],
        "Reptiles and Amphibians": [0, [], [], 0],
        "Mammals": [0, [], [], 0],
        "arthropod (etc)" : [0, [], [], 0],
        "Fish": [0, [], [], 0],
        "Birds": [0, [], [], 0],
        "Bees; wasps and ants": [0, [], [], 0],
        "Algaea; kelp; and single-celled organisms": [0, [], [], 0],
        "Other invertebrates": [0, [], [], 0],
    }

    ra_counts_dict = {      # Eww
        "Features factsheet on Nobanis" : [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "CABI yielded" : [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "Datasheet by CABI":[0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "FWS U.S. " : [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "ISNA - no RA" : [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "ISNA - has RA" :[0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "Has RA on NNSS Great Britain" : [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "on Glansis" :[0, 0, 0, 0, 0, 0, 0, 0, 0,], 
        "on INPN" : [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "Registered on BDI" : [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "On Michigan's watchlist" :[0, 0, 0, 0, 0, 0, 0, 0, 0], 
        "iucngisd" : [0, 0, 0, 0, 0, 0, 0, 0, 0], 
    }

    for key, value in general_info.items():
        if general_info[key][2][1:] in clade_count_dict.keys():
            clade_count_dict[general_info[key][2][1:]][0] += 1
            clade_count_dict[general_info[key][2][1:]][1].append(key)

    for item in content:
        if len(item) > 0:
            item = item.split(',"[')
            for i in clade_count_dict.keys():
                if item[0] in clade_count_dict[i][1]:
                    clade_count_dict[i][2].append(str(item[1]))

    ra_code_list = [ "Features factsheet on Nobanis","CABI yielded", "Datasheet by CABI", "FWS U.S. ","ISNA - no RA", "ISNA - has RA", 
                    "Has RA on NNSS Great Britain", "on Glansis", "on INPN", "Registered on BDI", "On Michigan's watchlist", "iucngisd"]

    for item in ra_code_list:       # Triple nested loop, thank god it is all lightweight stuff so I can get away with it but ewwwww.
        for key, value in clade_count_dict.items():
            if len(clade_count_dict[key][2]) > 0:
                for i in clade_count_dict[key][2]:      # Excuse my code here, I am tired and this is very yuckie. 
                    i = i.split(",")# print(key)
                    for j in i: 
                        if item in j:
                            clade_count_dict[key][3] += 1
                            if key == "Plants":
                                ra_counts_dict[item][0] += 1
                            elif key == "Reptiles and Amphibians":
                                ra_counts_dict[item][1] += 1
                            elif key == "Mammals":
                                ra_counts_dict[item][2] += 1
                            elif key == "arthropod (etc)":
                                ra_counts_dict[item][3] += 1
                            elif key == "Fish":
                                ra_counts_dict[item][4] += 1
                            elif key == "Birds":
                                ra_counts_dict[item][5] += 1
                            elif key == "Bees; wasps and ants":
                                ra_counts_dict[item][6] += 1
                            elif key == "Algaea; kelp; and single-celled organisms":
                                ra_counts_dict[item][7] += 1
                            elif key == "Other invertebrates":
                                    ra_counts_dict[item][8] += 1

    print(ra_counts_dict)
    return ra_counts_dict

def plot_ra_counts(ra_counts_dict):
    keys = list(ra_counts_dict.keys())
    values = list(ra_counts_dict.values())

    # Calculate the total sum of each set of values
    total_sums = [sum(v) for v in values]

    # Sort the keys and values based on the total sums
    sorted_keys, sorted_values = zip(*sorted(zip(keys, values), key=lambda x: sum(x[1])))
    sorted_total_sums = [sum(v) for v in sorted_values]

    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Set the bar width
    bar_width = 0.8

    # Set the index for the bars
    index = np.arange(len(keys))

    # Create the bars
    bottom = np.zeros(len(keys))
    for i in range(len(values[0])):
        plt.bar(index, [v[i] for v in sorted_values], bar_width, bottom=bottom, label=f'Value {i+1}')
        bottom += [v[i] for v in sorted_values]

    # Add total value above each stacked bar
    for j, val in enumerate(sorted_total_sums):
        plt.text(j, bottom[j], str(val), ha='center', va='bottom')

    # Add x-axis labels
    plt.xticks(index, sorted_keys, rotation=45)

    # Add labels and title
    plt.xlabel('RA site')
    plt.ylabel('Amount of RA available')

    # Show the plot
    plt.tight_layout()
    plt.show()
    
def main():
    general_info = read_gen_info()
    ra_dict, content = read_RA()
    plot_ra(ra_dict)    
    ra_counts_dict = calc_RA_vals(general_info, content, ra_dict)
    plot_ra_counts(ra_counts_dict)
    names_dict = read_ias()

if __name__ == "__main__":
    main()