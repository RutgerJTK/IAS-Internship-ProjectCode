import csv

data = """Species_name_latin	Species_name_dutch	Species_type	Rarity	Overall impact	Biodiversity impact	Environmental (ecosystem services) impact	Economic impact	Social impact	Other impacts	Risk assessment structure	Year_of_CIRCABC RA_Revision	Year_of_EU_List_inclusion	Nr of references on marigold	Total nr of observed individuals
Acacia saligna	Wilgacacia	Plants	null	3,8	4	4	4	4	3	Old 	2018	2019	6	0
Acridotheres tristis	Treurmaina	Birds	2	3,2	4	3	4	3	2	Modern	2017	2019	5	3486
Ailanthus altissima	Hemelboom	Plants	2	2,8	4	4	3	1	2	Modern	2018	2019	9	977901
Alopochen aegyptiaca	Nijlgans	Birds	1	2,8	3	3	3	3	2	Modern	2016	2017	5	10529689521
Alternanthera philoxeroides	Alligatorkruid	Plants	3	3,6	4	4	4	4	2	Old 	2015	2017	6	0
Ameiurus melas	Zwarte dwergmeerval	Fish	4	3,2	4	4	3	3	2	Odd		2022	6	153
Andropogon virginicus	Amerikaans bezemgras	Plants	null	3,6	4	3	4	4	3	Old 	2018	2019	5	0
Arthurdendyus triangulatus	Nieuw-Zeelandse landplatworm	Other invertebrates	null	3,2	4	4	4	2	2	Modern	2017	2019	5	0
Asclepias syriaca	Zijdeplant	Plants	3	2,6	2	4	3	2	2	Modern	2015	2017	3	11781
Axis axis	Axishert	Mammals	null	2,8	3	3	3	2	3	Modern	2021	2022	5	0
Baccharis halimifolia	Struikaster	Plants	3	3,4	4	4	4	1	4	Odd	2014	2016	5	0
Cabomba caroliniana	Waterwaaier	Plants	3	3	3	3	3	4	2	Odd	2015	2016	9	12246
Callosciurus erythraeus	Pallas' Eekhoorn	Mammals	2	3,6	4	4	4	3	3	Modern	2014	2016	5	1
Callosciurus finlaysonii	Thaise Eekhoorn	Mammals	1	2,6	3	3	4	1	2	Modern	2018	2022	4	0
Cardiospermum grandiflorum	Ballonrank	Plants	null	3	3	3	3	3	3	Old 	2017	2019	5	0
Celastrus orbiculatus	Heeft geen Nederlandse naam	Plants	3	2	2	2	3	1	2	Odd	2021	2022	7	3
Cenchrus setaceus (Pennisetum setaceum)	Fraai lampenpoetsergras	Plants	3	3,4	4	4	4	2	3	Modern	2016	2017	2	0
Channa argus	Heeft geen Nederlandse naam	Fish	null	3,2	4	3	3	2	4	Modern	2020	2022	7	0
Cortaderia jubata	Hoog pampagras	Plants	null	2,8	3	3	3	3	2	Old 	2018	2019	5	0
Corvus splendens	Huiskraai	Birds	3	3,6	4	4	3	4	3	Modern	2011	2016	6	0
Ehrharta calycina	Roze rimpelgras	Plants	null	2,6	4	4	2	2	1	Old 	2018	2019	4	0
Eichhornia crassipes	Waterhyacint	Plants	3	3,4	4	4	4	3	2	Odd	2015	2016	8	10
Elodea nuttallii	Smalle waterpest	Plants	1	3,2	4	4	4	3	1	Modern	2016	2017	9	1680861
Eriocheir sinensis	Chinese wolhandkrab	Arthropods (etc.)	2	3,2	4	4	2	3	3	Modern	2011	2016	9	831405
Eutamias sibiricus	Siberische Grondeekhoorn	Mammals	2	2,6	3	3	4	2	1	Modern	2011	2016	6	429201
Faxonius limosus	Gevlekte Amerikaanse rivierkreeft	Arthropods (etc.)	1	2,4	2	3	3	2	2	Modern	2015	2016	5	606651
Faxonius rusticus	Roestbruine Amerikaanse Rivierkreeft	Arthropods (etc.)	null	3,4	4	3	4	2	4	Modern	2019	2022	4	0
Faxonius virilis	Geknobbelde Amerikaanse rivierkreeft	Arthropods (etc.)	2	2,2	2	4	2	2	1	Old 	2015	2016	2	76245
Fundulus heteroclitus	Heeft geen Nederlandse naam	Fish	null	2,6	4	2	3	1	3	Modern	2019	2022	5	0
Gambusia affinis	Muskietenvisje	Fish	null	3,4	4	4	4	2	3	Modern	2020	2022	6	0
Gambusia holbrooki	Oostelijk Muskietenvisje	Fish	null	3,2	4	4	4	2	2	Modern	2020	2022	6	0
Gunnera tinctoria	Reuzenrabarber	Plants	3	3,2	4	4	4	2	2	Modern	2016	2017	6	21
Gymnocoronis spilanthoides	Smalle theeplant	Plants	3	3	4	3	3	3	2	Old 	2017	2019	6	55
Hakea sericea	Hakea	Plants	null	3,4	5	3	3	3	3	Old 	2018	2022	5	0
Heracleum mantegazzianum	Reuzenberenklauw	Plants	1	3,6	4	4	5	4	1	Modern	2016	2017	9	60549510
Heracleum persicum	Perzische berenklauw	Plants	3	2,4	2	2	2	4	2	Modern	2015	2016	4	0
Heracleum sosnowskyi	Sosnowsky's berenklauw	Plants	3	2,6	3	1	4	3	2	Odd	2015	2016	5	0
Herpestes javanicus	Indische Mangoeste (javanicus)	Mammals	null	3,8	4	5	4	4	2	Modern	2015	2016	4	0
Humulus scandens	Japanse hop	Plants	3	3	4	3	3	3	2	Old 	2018	2019	4	0
Hydrocotyle ranunculoides	Grote waternavel	Plants	2	3,6	3	5	4	4	2	Modern	2011	2016	8	5000703
Impatiens glandulifera	Reuzenbalsemien	Plants	1	3	3	3	3	1	1	Modern	2015	2017	9	65981328
Lagarosiphon major	Verspreidbladige waterpest	Plants	3	3,2	3	4	3	3	3	Modern	2011	2016	9	435
Lampropeltis getula	Koningsslang	Reptiles and amphibians	null	2,6	4	2	4	1	2	Modern	2017	2022	4	0
Lepomis gibbosus	Zonnebaars	Fish	2	2,6	4	3	3	2	1	Modern	2018	2019	7	336610
Lespedeza cuneata	Chinese struikklaver	Plants	null	3	4	4	3	3	1	Old 	2018	2019	5	0
Lithobates catesbeianus	Amerikaanse stierkikker	Reptiles and amphibians	4	2,2	3	4	1	1	2	Modern	2011	2016	6	0
Ludwigia grandiflora	Waterteunisbloem	Plants	3	2,6	2	3	3	2	3	Modern	2011	2016	7	530965
Ludwigia peploides	Kleine waterteunisbloem	Plants	4	3,6	4	4	4	3	3	Old 	2011	2016	7	12246
Lygodium japonicum	Japanse klimvaren	Plants	null	3	4	4	3	3	1	Old 	2018	2019	5	0
Lysichiton americanus	Moeraslantaarn	Plants	3	2,4	2	3	3	3	1	Modern	2011	2016	6	5356
Microstegium vimineum	Japans steltgras	Plants	3	3,2	4	4	3	3	2	Odd	2015	2017	7	0
Morone americana	Amerikaanse baars	Fish	null	1,6	3	2	1	1	1	Modern	2018	2022	6	0
Muntiacus reevesi	Chinese Muntjak	Mammals	2	2,6	3	4	2	2	2	Modern	2011	2016	4	105
Myocastor coypus	Beverrat	Mammals	2	4,2	4	4	5	4	4	Modern	2015	2016	6	17766
Myriophyllum aquaticum	Parelvederkruid	Plants	2	3,2	4	4	3	3	2	Modern	2011	2016	9	130816
Myriophyllum heterophyllum	Ongelijkbladig vederkruid	Plants	3	3,4	4	3	4	4	2	Old 	2015	2017	6	6903
Nasua nasua	Rode Neusbeer	Mammals	null	3,2	4	4	3	4	1	Modern	2015	2016	6	1
Nyctereutes procyonoides	Wasbeerhond	Mammals	3	3,2	3	3	4	3	3	Modern	2016	2017	7	1953
Ondatra zibethicus	Muskusrat	Mammals	2	3,2	4	4	5	2	1	Modern	2016	2017	6	1128753
Oxyura jamaicensis	Rosse Stekelstaart	Birds	1	3,6	4	5	4	1	4	Modern	2011	2016	7	3029491
Pacifastacus leniusculus	Californische rivierkreeft	Arthropods (etc.)	3	3,4	4	4	3	3	3	Modern	2011	2016	9	3160
Parthenium hysterophorus	Schijnambrosia	Plants	null	3,8	4	4	4	5	2	Odd	2014	2016	5	0
Perccottus glenii	Amoergrondel	Fish	null	2,8	4	3	4	1	2	Odd	2015	2016	5	0
Persicaria perfoliata	Gestekelde duizendknoop	Plants	3	2,8	3	4	4	2	1	Odd	2011	2016	7	0
Persicaria wallichii (Koenigia polystachya )	Afghaanse duizendknoop	Plants	3	2,6	4	3	3	2	1	Modern	2018	2022	4	4753
Pistia stratiotes	Watersla	Plants	3	3,8	4	4	4	4	3	Old 	2017	2022	8	6670
Plotosus lineatus	Gestreepte koraalmeerval	Fish	null	3,2	3	3	3	4	3	Modern	2016	2019	5	0
Procambarus clarkii	Rode Amerikaanse rivierkreeft	Arthropods (etc.)	1	3,2	4	4	4	1	3	Modern	2011	2016	9	8935878
Procambarus virginalis	Marmerkreeft	Arthropods (etc.)	4	2,6	2	3	3	2	3	Modern	2011	2016	6	1326
Procyon lotor	Gewone Wasbeer	Mammals	2	3,4	3	3	4	3	4	Modern	2011	2016	8	6670
Prosopis juliflora	Mesquite	Plants	null	3,6	4	3	4	4	3	Old 	2018	2019	5	0
Pseudorasbora parva	Blauwband	Fish	2	2,8	3	4	3	2	2	Modern	2011	2016	9	40755
Pueraria montana	Heeft geen Nederlandse naam	Plants	null	2,8	3	3	4	2	2	Modern	2015	2016	5	0
Pycnonotus cafer	Roodbuikbuulbuul	Birds	null	2,6	3	3	4	1	2	Modern	2021	2022	5	1
Rugulopteryx okamurae	Heeft geen Nederlandse naam	Algen, wieren en eencelligen	null	3	4	4	4	1	2	Modern	2020	2022	2	0
Salvinia molesta	Grote vlotvaren	Plants	3	3,4	4	4	4	4	1	Old 	2017	2019	8	10
Sciurus carolinensis	Grijze Eekhoorn	Mammals	4	3	4	3	5	1	2	Modern	2011	2016	5	1
Sciurus niger	Amerikaanse Voseekhoorn	Mammals	1	2,6	3	3	3	3	1	Odd	2015	2016	4	0
Solenopsis geminata	Tropische vuurmier	Bees, hornets and ants	1	2	3	3	3	1	0	Modern	2018	2022	5	0
Solenopsis invicta	Rode vuurmier	Bees, hornets and ants	1	3,6	4	4	5	4	1	Modern	2017	2022	5	0
Solenopsis richteri	Heeft geen Nederlandse naam	Bees, hornets and ants	null	2,6	3	3	3	4	0	Modern	2020	2022	5	0
Threskiornis aethiopicus	Heilige Ibis	Birds	1	2,2	3	3	2	2	1	Modern	2011	2016	6	465
Trachemys scripta elegans	Roodwangschildpad	Reptiles and amphibians	2	3,2	4	4	3	4	1	Modern	2015	2016	7	903840
Trachemys scripta scripta	Geelbuikschildpad	Reptiles and amphibians	2	3,2	4	4	3	4	1	Modern	2015	2016	4	891780
Trachemys scripta troostii	Geelwangschildpad	Reptiles and amphibians	2	3,2	4	4	3	4	1	Modern	2015	2016	3	38503
Triadica sebifera	Chinese talgboom	Plants	null	2,8	4	4	2	2	2	Old 	2018	2019	5	0
Vespa velutina	Aziatische Hoornaar	Bees, hornets and ants	4	3	3	3	3	4	2	Modern	2011	2016	6	400960
Wasmannia auropunctata	Dwergvuurmier	Bees, hornets and ants	1	3,2	3	4	4	4	1	Modern	2020	2022	6	0
Xenopus laevis	Afrikaanse Klauwkikker	Reptiles and amphibians	null	2	3	3	2	1	1	Modern	2021	2022	8	0
"""
file_path = "D:\\Project_IAS\\Analysis_R\\"
file_name = "IAS_risks_dataset_updated.csv"
path = file_path + file_name
data = data.split("\n")
data2 = []
for ele in data:
    if ele == "\n":
        ele = ""
        line = ele
        data2.append(line)
    else:
        ele += ele

    # line = line.replace(",", ".")
    # line = line.replace("\t", ",")
    # data2.append(line)
    # print(line)

print(data2)

# with open(path, "w+") as f:
