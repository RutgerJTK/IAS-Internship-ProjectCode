"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from NNSSGB.gov 
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

from time import perf_counter
import re
import bs4 
from bs4 import BeautifulSoup
import requests
import lxml
from lxml import html
from lxml import etree

def scrape_nnss():
    try:
        url = "https://www.nonnativespecies.org/non-native-species/risk-analysis/risk-assessment/#Riskassessments"
        page = requests.get(url, timeout=15)
        element_html = html.fromstring(page.content)
        table = element_html.xpath("//table[@id='sortTableTest']")
        table_tree = lxml.etree.tostring(table[0], method='xml')
        string_scraped = str(table_tree)
    except TimeoutError:
        print("Site could not be reached. Try again later.")
        pass
    except requests.exceptions.HTTPError as err:
        print("There was an error requesting the site HTTP.")
        pass
    return string_scraped

def species_ra_check(ln_names_dict, string_scraped):
    for i in ln_names_dict.keys():
        matches = re.findall(ln_names_dict[i][0], string_scraped)
        if len(matches) > 0:
            ln_names_dict[i].append("Has RA on NNSS Great Britain: https://www.nonnativespecies.org/non-native-species/risk-analysis/risk-assessment/#Riskassessments")
    return ln_names_dict



def main_scraper(ln_names_dict):
    string_scraped = scrape_nnss()
    ln_scraping_dict = species_ra_check(ln_names_dict, string_scraped)
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