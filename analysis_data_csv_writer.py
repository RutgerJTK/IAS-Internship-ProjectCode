import csv
import Waarnemingen_attributes
import pandas as pd
import os
import re
from time import perf_counter


data = """Species_name_latin	Species_name_dutch	Species_type	Rarity	Overall impact	Biodiversity impact	Environmental (ecosystem services) impact	Economic impact	Social impact	Other impacts	Risk assessment structure	Year_of_CIRCABC RA_Revision	Year_of_EU_List_inclusion	Nr of references on marigold	Total nr of observed individuals
Acacia saligna	Wilgacacia	Plants	null	3,8	4	4	4	4	3	Old 	2018	2019	6	0
Acridotheres tristis	Treurmaina	Birds	2	3,2	4	3	4	3	2	Modern	2017	2019	5	3486	83
Ailanthus altissima	Hemelboom	Plants	2	2,8	4	4	3	1	2	Modern	2018	2019	9	977901	1706
Alopochen aegyptiaca	Nijlgans	Birds	1	2,8	3	3	3	3	2	Modern	2016	2017	5	10529689521
Alternanthera philoxeroides	Alligatorkruid	Plants	3	3,6	4	4	4	4	2	Old 	2015	2017	6	0
Ameiurus melas	Zwarte dwergmeerval	Fish	4	3,2	4	4	3	3	2	Odd	2021	2022	6	153	14
Andropogon virginicus	Amerikaans bezemgras	Plants	null	3,6	4	3	4	4	3	Old 	2018	2019	5	0
Arthurdendyus triangulatus	Nieuw-Zeelandse landplatworm	Other invertebrates	null	3,2	4	4	4	2	2	Modern	2017	2019	5	0
Asclepias syriaca	Zijdeplant	Plants	3	2,6	2	4	3	2	2	Modern	2015	2017	3	11781	349
Axis axis	Axishert	Mammals	null	2,8	3	3	3	2	3	Modern	2021	2022	5	0
Baccharis halimifolia	Struikaster	Plants	3	3,4	4	4	4	1	4	Odd	2014	2016	5	0	0
Cabomba caroliniana	Waterwaaier	Plants	3	3	3	3	3	4	2	Odd	2015	2016	9	12246	351
Callosciurus erythraeus	Pallas' Eekhoorn	Mammals	2	3,6	4	4	4	3	3	Modern	2014	2016	5	1	3
Callosciurus finlaysonii	Thaise Eekhoorn	Mammals	1	2,6	3	3	4	1	2	Modern	2018	2022	4	0
Cardiospermum grandiflorum	Ballonrank	Plants	null	3	3	3	3	3	3	Old 	2017	2019	5	0
Celastrus orbiculatus	Heeft geen Nederlandse naam	Plants	3	2	2	2	3	1	2	Odd	2021	2022	7	3	0
Cenchrus setaceus (Pennisetum setaceum)	Fraai lampenpoetsergras	Plants	3	3,4	4	4	4	2	3	Modern	2016	2017	2	0
Channa argus	Heeft geen Nederlandse naam	Fish	null	3,2	4	3	3	2	4	Modern	2020	2022	7	0
Cortaderia jubata	Hoog pampagras	Plants	null	2,8	3	3	3	3	2	Old 	2018	2019	5	0
Corvus splendens	Huiskraai	Birds	3	3,6	4	4	3	4	3	Modern	2011	2016	6	0	0
Ehrharta calycina	Roze rimpelgras	Plants	null	2,6	4	4	2	2	1	Old 	2018	2019	4	0
Eichhornia crassipes	Waterhyacint	Plants	3	3,4	4	4	4	3	2	Odd	2015	2016	8	10	82
Elodea nuttallii	Smalle waterpest	Plants	1	3,2	4	4	4	3	1	Modern	2016	2017	9	1680861	2554
Eriocheir sinensis	Chinese wolhandkrab	Arthropods (etc.)	2	3,2	4	4	2	3	3	Modern	2011	2016	9	831405	2009
Eutamias sibiricus	Siberische Grondeekhoorn	Mammals	2	2,6	3	3	4	2	1	Modern	2011	2016	6	429201	2057
Faxonius limosus	Gevlekte Amerikaanse rivierkreeft	Arthropods (etc.)	1	2,4	2	3	3	2	2	Modern	2015	2016	5	606651	1904
Faxonius rusticus	Roestbruine Amerikaanse Rivierkreeft	Arthropods (etc.)	null	3,4	4	3	4	2	4	Modern	2019	2022	4	0
Faxonius virilis	Geknobbelde Amerikaanse rivierkreeft	Arthropods (etc.)	2	2,2	2	4	2	2	1	Old 	2015	2016	2	76245	642
Fundulus heteroclitus	Heeft geen Nederlandse naam	Fish	null	2,6	4	2	3	1	3	Modern	2019	2022	5	0
Gambusia affinis	Muskietenvisje	Fish	null	3,4	4	4	4	2	3	Modern	2020	2022	6	0	0
Gambusia holbrooki	Oostelijk Muskietenvisje	Fish	null	3,2	4	4	4	2	2	Modern	2020	2022	6	0
Gunnera tinctoria	Reuzenrabarber	Plants	3	3,2	4	4	4	2	2	Modern	2016	2017	6	21	8
Gymnocoronis spilanthoides	Smalle theeplant	Plants	3	3	4	3	3	3	2	Old 	2017	2019	6	55	15
Hakea sericea	Hakea	Plants	null	3,4	5	3	3	3	3	Old 	2018	2022	5	0
Heracleum mantegazzianum	Reuzenberenklauw	Plants	1	3,6	4	4	5	4	1	Modern	2016	2017	9	60549510	20226
Heracleum persicum	Perzische berenklauw	Plants	3	2,4	2	2	2	4	2	Modern	2015	2016	4	0
Heracleum sosnowskyi	Sosnowsky's berenklauw	Plants	3	2,6	3	1	4	3	2	Odd	2015	2016	5	0
Herpestes javanicus	Indische Mangoeste (javanicus)	Mammals	null	3,8	4	5	4	4	2	Modern	2015	2016	4	0
Humulus scandens	Japanse hop	Plants	3	3	4	3	3	3	2	Old 	2018	2019	4	0
Hydrocotyle ranunculoides	Grote waternavel	Plants	2	3,6	3	5	4	4	2	Modern	2011	2016	8	5000703	6344
Impatiens glandulifera	Reuzenbalsemien	Plants	1	3	3	3	3	1	1	Modern	2015	2017	9	65981328	16634
Lagarosiphon major	Verspreidbladige waterpest	Plants	3	3,2	3	4	3	3	3	Modern	2011	2016	9	435	58
Lampropeltis getula	Koningsslang	Reptiles and amphibians	null	2,6	4	2	4	1	2	Modern	2017	2022	4	0
Lepomis gibbosus	Zonnebaars	Fish	2	2,6	4	3	3	2	1	Modern	2018	2019	7	336610	1529
Lespedeza cuneata	Chinese struikklaver	Plants	null	3	4	4	3	3	1	Old 	2018	2019	5	0
Lithobates catesbeianus	Amerikaanse stierkikker	Reptiles and amphibians	4	2,2	3	4	1	1	2	Modern	2011	2016	6	0	0
Ludwigia grandiflora	Waterteunisbloem	Plants	3	2,6	2	3	3	2	3	Modern	2011	2016	7	530965	1522
Ludwigia peploides	Kleine waterteunisbloem	Plants	4	3,6	4	4	4	3	3	Old 	2011	2016	7	12246	270
Lygodium japonicum	Japanse klimvaren	Plants	null	3	4	4	3	3	1	Old 	2018	2019	5	0
Lysichiton americanus	Moeraslantaarn	Plants	3	2,4	2	3	3	3	1	Modern	2011	2016	6	5356	213
Microstegium vimineum	Japans steltgras	Plants	3	3,2	4	4	3	3	2	Odd	2015	2017	7	0
Morone americana	Amerikaanse baars	Fish	null	1,6	3	2	1	1	1	Modern	2018	2022	6	0
Muntiacus reevesi	Chinese Muntjak	Mammals	2	2,6	3	4	2	2	2	Modern	2011	2016	4	105	17
Myocastor coypus	Beverrat	Mammals	2	4,2	4	4	5	4	4	Modern	2015	2016	6	17766	362
Myriophyllum aquaticum	Parelvederkruid	Plants	2	3,2	4	4	3	3	2	Modern	2011	2016	9	130816	843
Myriophyllum heterophyllum	Ongelijkbladig vederkruid	Plants	3	3,4	4	3	4	4	2	Old 	2015	2017	6	6903	204
Nasua nasua	Rode Neusbeer	Mammals	null	3,2	4	4	3	4	1	Modern	2015	2016	6	1	3
Nyctereutes procyonoides	Wasbeerhond	Mammals	3	3,2	3	3	4	3	3	Modern	2016	2017	7	1953	94
Ondatra zibethicus	Muskusrat	Mammals	2	3,2	4	4	5	2	1	Modern	2016	2017	6	1128753	2097
Oxyura jamaicensis	Rosse Stekelstaart	Birds	1	3,6	4	5	4	1	4	Modern	2011	2016	7	3029491	5848
Pacifastacus leniusculus	Californische rivierkreeft	Arthropods (etc.)	3	3,4	4	4	3	3	3	Modern	2011	2016	9	3160	172
Parthenium hysterophorus	Schijnambrosia	Plants	null	3,8	4	4	4	5	2	Odd	2014	2016	5	0
Perccottus glenii	Amoergrondel	Fish	null	2,8	4	3	4	1	2	Odd	2015	2016	5	0
Persicaria perfoliata	Gestekelde duizendknoop	Plants	3	2,8	3	4	4	2	1	Odd	2011	2016	7	0
Persicaria wallichii (Koenigia polystachya )	Afghaanse duizendknoop	Plants	3	2,6	4	3	3	2	1	Modern	2018	2022	4	4753
Pistia stratiotes	Watersla	Plants	3	3,8	4	4	4	4	3	Old 	2017	2022	8	6670	40
Plotosus lineatus	Gestreepte koraalmeerval	Fish	null	3,2	3	3	3	4	3	Modern	2016	2019	5	0
Procambarus clarkii	Rode Amerikaanse rivierkreeft	Arthropods (etc.)	1	3,2	4	4	4	1	3	Modern	2011	2016	9	8935878	6704
Procambarus virginalis	Marmerkreeft	Arthropods (etc.)	4	2,6	2	3	3	2	3	Modern	2011	2016	6	1326	83
Procyon lotor	Gewone Wasbeer	Mammals	2	3,4	3	3	4	3	4	Modern	2011	2016	8	6670	156
Prosopis juliflora	Mesquite	Plants	null	3,6	4	3	4	4	3	Old 	2018	2019	5	0
Pseudorasbora parva	Blauwband	Fish	2	2,8	3	4	3	2	2	Modern	2011	2016	9	40755	610
Pueraria montana	Heeft geen Nederlandse naam	Plants	null	2,8	3	3	4	2	2	Modern	2015	2016	5	0
Pycnonotus cafer	Roodbuikbuulbuul	Birds	null	2,6	3	3	4	1	2	Modern	2021	2022	5	1	0
Rugulopteryx okamurae	Heeft geen Nederlandse naam	Algen, wieren en eencelligen	null	3	4	4	4	1	2	Modern	2020	2022	2	0
Salvinia molesta	Grote vlotvaren	Plants	3	3,4	4	4	4	4	1	Old 	2017	2019	8	10	4
Sciurus carolinensis	Grijze Eekhoorn	Mammals	4	3	4	3	5	1	2	Modern	2011	2016	5	1	1
Sciurus niger	Amerikaanse Voseekhoorn	Mammals	1	2,6	3	3	3	3	1	Odd	2015	2016	4	0	1
Solenopsis geminata	Tropische vuurmier	Bees, hornets and ants	1	2	3	3	3	1	0	Modern	2018	2022	5	0
Solenopsis invicta	Rode vuurmier	Bees, hornets and ants	1	3,6	4	4	5	4	1	Modern	2017	2022	5	0
Solenopsis richteri	Heeft geen Nederlandse naam	Bees, hornets and ants	null	2,6	3	3	3	4	0	Modern	2020	2022	5	0
Threskiornis aethiopicus	Heilige Ibis	Birds	1	2,2	3	3	2	2	1	Modern	2011	2016	6	465	196
Trachemys scripta elegans	Roodwangschildpad	Reptiles and amphibians	2	3,2	4	4	3	4	1	Modern	2015	2016	7	903840	2582
Trachemys scripta scripta	Geelbuikschildpad	Reptiles and amphibians	2	3,2	4	4	3	4	1	Modern	2015	2016	4	891780	465
Trachemys scripta troostii	Geelwangschildpad	Reptiles and amphibians	2	3,2	4	4	3	4	1	Modern	2015	2016	3	38503	2179
Triadica sebifera	Chinese talgboom	Plants	null	2,8	4	4	2	2	2	Old 	2018	2019	5	0
Vespa velutina	Aziatische Hoornaar	Bees, hornets and ants	4	3	3	3	3	4	2	Modern	2011	2016	6	400960	1683
Wasmannia auropunctata	Dwergvuurmier	Bees, hornets and ants	1	3,2	3	4	4	4	1	Modern	2020	2022	6	0
Xenopus laevis	Afrikaanse Klauwkikker	Reptiles and amphibians	null	2	3	3	2	1	1	Modern	2021	2022	8	0
"""

def get_data(data):
    data = data.split("\n")
    data = data[0:-1]
    data2 = []
    for row in data:
        row = row.split("\t")
        data2.append(row)
    # print(data2)
    return data2

def data_to_df(data):
    file_path = "D:\\Project_IAS\\Analysis_R\\"
    file_name = "IAS_risks_dataset_updated2.csv"
    path = file_path + file_name
    df = pd.DataFrame.from_records(data)
    df.columns = df.iloc[0]     # first line is header
    df = df[1:]
    return df

def read_file(ias_names):
    try:
        ln_names_dict = {}
        with open(ias_names) as f:
            content = f.readlines()
        for line in content:
            temp_dict = line.split(": ")
            temp_dict[1] = int(temp_dict[1].strip('\n'))
            ln_names_dict.update({temp_dict[1] : [temp_dict[0]]})
        return ln_names_dict
    except IOError as ioe:
        print(ioe)

def new_counts(ln_names_dict, df):
    files_path = "D:\\Project_IAS\\Scraped\\Scraped_daily\\"
    files = os.listdir(files_path)
    file_str = "soup_"
    yearly_obs_counts = []
    for i in ln_names_dict.keys():
        file_str = "soup_"
        if ln_names_dict[i][0] != "Cipangopaludina chinensis":
            file_str = file_str + str(i)
            abs_path = (files_path + file_str)
            element_list = Waarnemingen_attributes.xml_parse_elements(abs_path)
            # print(element_list)
            name = ln_names_dict[i][0]

            if len(element_list)>0: # Only do this for species which have been observed once or more.
                obs_getter(element_list, df, name)
                split_year_dict = year_splitter(element_list, df, name)
            elif len(element_list) == 0:
                element_list = []
                split_year_dict = year_splitter(element_list, df, name)
            yearly_obs_counts.append(split_year_dict)
    
    yearly_counts_df = pd.DataFrame(yearly_obs_counts)
    yearly_counts_df.set_index('species', inplace=True)

    return yearly_counts_df
    
def year_splitter(element_list, df, name):
    split_year_dict = {"species" : name}

    for x in range(2000,2024):
        split_year_dict[str(x)] = 0

    if len(element_list) > 0:
        for i in element_list:
            i = i.split(",")
            i[1] = i[1][0:4]
            split_year_dict[i[1]] += int(i[2])
    
    # print(split_year_dict)
    return split_year_dict


def obs_getter(element_list, df, name):
    print("-"*80)
    print(name)
    # print(element_list)
    post_inclusion_obs = []
    post_inclusion_obs_df = pd.DataFrame({'Timestamp' : [],
                                          '# of observations' : []})
    pre_inclusion_obs = []
    all_unique_obs = []
    obs_data_key = "\/,[0-9--].*[0-9]"
    if name == "Tamias sibiricus":
        name = "Eutamias sibiricus"
    elif name == "Persicaria wallichii":
        name = "Persicaria wallichii (Koenigia polystachya )"
    row_data = (df['Species_name_latin'] == name)
    row_info = df[row_data]['Year_of_EU_List_inclusion']
    Year_of_EU_List_inclusion = int(row_info.iloc[0])

    for i in element_list:
        # print(i)
        matches = re.findall(obs_data_key, i)
        old_info = matches[0][2:]
        obs_info = old_info.split(",")
        obs_info[0] = obs_info[0][0:4]

        if int(obs_info[0]) >= Year_of_EU_List_inclusion:
            post_inclusion_obs.append(int(obs_info[1]))
        elif int(obs_info[0]) < Year_of_EU_List_inclusion:
            pre_inclusion_obs.append(int(obs_info[1]))
    # print(sum(pre_inclusion_obs))
    # print(sum(post_inclusion_obs))
    # print(sum(pre_inclusion_obs) + sum(post_inclusion_obs))


def df_to_csv(df):
    df.columns.values[-1] = "Total nr of observed individuals post EU list inclusion"
    # Set the first row as the column headers
    # df.columns = df.iloc[0]

    # # Drop the first row (old header)
    # df = df[1:].reset_index(drop=True)
    print(df)
    print(df.columns)

    # print(df)
    file_path = "D:\\Project_IAS\\Analysis_R\\"
    file_name = "IAS_risks_dataset_updated2.csv"
    path = file_path + file_name
    # Write DataFrame to CSV file
    df.to_csv(path, index=False)

def yearly_counts_to_csv(yearly_counts_df):
    file_path = "D:\\Project_IAS\\Analysis_R\\"
    file_name = "IAS_yearly_observed_counts.csv"
    path = file_path + file_name
    print(yearly_counts_df)
    yearly_counts_df.index = yearly_counts_df.index.str.replace('Tamias sibiricus', 'Eutamias sibiricus')
    yearly_counts_df = yearly_counts_df.sort_index()
    # Write DataFrame to CSV file
    yearly_counts_df.to_csv(path, index=False)  # Turned index to true to verify if columns checked out with analysis file, they did, for ease of copy-pasting the index was set to false.



def main(data):
    data = get_data(data)
    df = data_to_df(data)
    ias_file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = read_file(ias_file)
    yearly_counts_df = new_counts(ln_names_dict, df)
    # df_to_csv(df)
    yearly_counts_to_csv(yearly_counts_df)

if __name__ == "__main__":
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    
    main(data)

    t1_stop = perf_counter()
    print("Elapsed time during the whole program in seconds:",t1_stop-t1_start)

