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

def write_dict(ln_names_dict):
    with open('D:\\Project_IAS\\Scraped\\Scraped_RA\\Scraped_RA_info.csv', 'w') as csv_file:  
        write = csv.writer(csv_file)
        header = ["Species_ID", "Nobanis", "CABI", "FWS", "ISNA", "NNSSGB", "Glansis", "INPN", "Biodiversityireland", "Michigan's Invasive Species", "Global invasive species database (EICAT)"]
        write.writerow(header)
        for key, value in ln_names_dict.items():
            write.writerow([key, value])
        #     f.write(f'{key} $$$ {values[0:]}\n')
    csv_file.close()

def risk_suite():
    ias_file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = read_file(ias_file)
    try:
        import ScrapeNobanis, ScrapeISNA, ScrapeNNSSGB, ScrapeGlansis, ScrapeINPN, ScrapeBDI, ScrapeMich, ScrapeGISD, ScrapeCABI, ScrapeFWS
        print("Nobanis")
        ln_names_dict = ScrapeNobanis.main_scraper(ln_names_dict)
        print("CABI")
        ln_names_dict = ScrapeCABI.main_scraper(ln_names_dict)
        print("FWS")
        ln_names_dict = ScrapeFWS.main_scraper(ln_names_dict)
        print("ISNA")
        ln_names_dict = ScrapeISNA.main_scraper(ln_names_dict)
        print("NNSSGB")
        ln_names_dict = ScrapeNNSSGB.main_scraper(ln_names_dict)
        print("Glansis")
        ln_names_dict = ScrapeGlansis.main_scraper(ln_names_dict)
        print("INPN")
        ln_names_dict = ScrapeINPN.main_scraper(ln_names_dict)
        print("biodiversityireland")
        ln_names_dict = ScrapeBDI.main_scraper(ln_names_dict)
        print("Michigan's Invasive Species")
        ln_names_dict = ScrapeMich.main_scraper(ln_names_dict)
        print("Global invasive species database (EICAT)")
        ln_names_dict = ScrapeGISD.main_scraper(ln_names_dict)
    except ModuleNotFoundError:
        from RA_Code import ScrapeNobanis

    print(ln_names_dict)
    write_dict(ln_names_dict)
    return ln_names_dict

if __name__ == "__main__":
    """

    """
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)

    risk_suite()

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)