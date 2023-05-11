from time import perf_counter
import csv

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

def MA_store_nrs():
    supply_dict = {
        "AnimalAttraction" : [0],
        "Blue-Lagoon" : [0],
        "Heevis" : [0],
        "Welle Diertotaal" : [0],
        "Marktplaats" : [0], 
        "Tuincentrum" : [0], 
        "AquaPlantsOnline.nl" : [0]
    }
    return supply_dict

def write_supply(supply_dict):
    with open('D:\\Project_IAS\\Scraped\\Scraped_MA\\Scraped_MA_supply.csv', 'w') as csv_file:  
        write = csv.writer(csv_file)
        header = ["Webstore", "# of Species Offered and Species"]
        write.writerow(header)
        for key, value in supply_dict.items():
            write.writerow([key, value])
    csv_file.close()

def write_info(ln_names_dict):
    with open('D:\\Project_IAS\\Scraped\\Scraped_MA\\Scraped_MA_info.csv', 'w') as csv_file:  
        write = csv.writer(csv_file)
        header = ["Species_ID", "Species_Name_Latin", "Store offer"]
        write.writerow(header)
        for key, value in ln_names_dict.items():
            write.writerow([key, value])
    csv_file.close()

def market_suite():
    supply_dict = MA_store_nrs()
    ias_file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = read_file(ias_file)
    try:
        import ScrapeBlueLagoon, ScrapeWelle, ScrapeAnimalAttraction, ScrapeHeevis, ScrapeMarktSelenium, ScrapeAquariumPlanten, ScrapeTuinCentrum
        print("Marktplaats")
        ln_names_dict, supply_dict = ScrapeMarktSelenium.main_scraper(ln_names_dict, supply_dict)
        print("Blue-Lagoon")
        ln_names_dict, supply_dict = ScrapeBlueLagoon.main_scraper(ln_names_dict, supply_dict)
        print("Welle diertotaal")
        ln_names_dict, supply_dict = ScrapeWelle.main_scraper(ln_names_dict, supply_dict)
        print("AnimalAttraction")
        ln_names_dict, supply_dict = ScrapeAnimalAttraction.main_scraper(ln_names_dict, supply_dict)
        print("Heevis")
        ln_names_dict, supply_dict = ScrapeHeevis.main_scraper(ln_names_dict, supply_dict)
        print("AquaPlantsOnline")
        ln_names_dict, supply_dict = ScrapeAquariumPlanten.main_scraper(ln_names_dict, supply_dict)
        print("Tuincentrum")
        ln_names_dict, supply_dict = ScrapeTuinCentrum.main_scraper(ln_names_dict, supply_dict)

        print(ln_names_dict)
        print(supply_dict)

    except ImportError:
        print(ImportError)
        pass
    
    write_supply(supply_dict)
    write_info(ln_names_dict)

if __name__ == "__main__":
    """

    """
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)

    market_suite()

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)