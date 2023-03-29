"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

from time import perf_counter
import re
import bs4 
import requests


def scrape_nobanis(ln_names_dict):
    try:
        url = "https://www.nobanis.org/fact-sheets/"
        page = requests.get(url, timeout=15)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        soup = str(soup)
        for i in ln_names_dict.keys():
            matches = re.findall(ln_names_dict[i][0], soup)
            matches = list(set(matches))
            if len(matches) > 0:
                ln_names_dict[i].append("Nobanis")
    except TimeoutError:
        pass
    return(ln_names_dict)

def main_scraper(ln_names_dict):
    ln_scraping_dict = scrape_nobanis(ln_names_dict)
    return ln_scraping_dict

if __name__ == "__main__":
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    ias_file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = {}

    try: 
        import RA_scraping_suite
    except ModuleNotFoundError:
        from RA_Code import RA_scraping_suite

    ln_names_dict = RA_scraping_suite.read_file(ias_file)
    ln_scraping_dict = main_scraper(ln_names_dict)

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)