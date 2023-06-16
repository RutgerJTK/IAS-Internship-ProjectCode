import re
import seaborn as sns
sns.set_theme()
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random

def read_RA():
    path = "D:\\Project_IAS\\Scraped\\Scraped_RA\\Scraped_RA_info.csv"
    with open(path,  "r") as f:
        content = f.read()

    nobanis = re.findall("Features factsheet on Nobanis", content)
    yield_cabi = re.findall("CABI yielded", content)
    datasheets_cabi = re.findall("Datasheet by CABI", content)
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
        "isna_no_RA" : len(isna_no_RA),
        "isna_RA" : len(isna_RA), 
        "NNSSGB" : len(NNSSGB), 
        "Glansis" : len(Glansis),
        "INPN" : len(INPN), 
        "BDI" : len(BDI), 
        "Michigan" : len(Michigan), 
        "GISD" : len(GISD)
    }
    # print(ra_dict)
    f.close()
    return ra_dict


def plot_ra(ra_dict):
    print(ra_dict)
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
    Opens the names:waarnemingen_codes file, turns it into a dict, returns it to 
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
    with open(path,  "r") as f:
        content = f.read() 
    
    content = content.split(":")
    content = content[:-1]
    for i in range(len(content)):
        content[i] = content[i].replace("Ã«", "ë")
    
        content[i] = content[i].strip("\n")
        content[i] = content[i].split(",")
    print(content)

    for i in range(len(content)):
        if len(content[i]) > 4:

            print(len(content[i]), content[i])
    # split_list = [content[i:i+4] for i in range(0, len(content), 4)]

    # print(split_list[-2])


def build_ra_dict(names_dict):
    for id in names_dict.keys():
        name_ln = (names_dict[id])


def main():
    ra_dict = read_RA()
    plot_ra(ra_dict)    
    names_dict = read_ias()
    read_gen_info()
    build_ra_dict(names_dict)

if __name__ == "__main__":
    main()