from time import perf_counter


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
        "AnimalAttraction" : 0,
        "Blue-Lagoon" : 0,
        "Heevis" : 0,
        "Welle Diertotaal" : 0,
        "Marktplaats" : 0
    }
    return supply_dict

def market_suite():
    supply_dict = MA_store_nrs()
    ias_file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = read_file(ias_file)
    try:
        import ScrapeBlueLagoon, ScrapeWelle, ScrapeHeevis
        # print("Blue-Lagoon")
        # ln_names_dict = ScrapeBlueLagoon.main_scraper(ln_names_dict)
        # print("Welle diertotaal")
        # ln_names_dict = ScrapeWelle.main_scraper(ln_names_dict)
        print("Heevis")
        ln_names_dict, supply_dict = ScrapeHeevis.main_scraper(ln_names_dict, supply_dict)
        print(ln_names_dict)
    except ImportError:
        print(ImportError)
        pass

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