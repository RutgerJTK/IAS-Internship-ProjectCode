"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

from time import perf_counter
import re
import bs4 
import requests
import lxml
from lxml import html
from lxml import etree

def scrape_isna():
    page_nr = 1    
    page_end = False
    string_scraped = ""
    url_builder_list = []
    while page_end == False:
        try:
            url = "https://invasivespeciesni.co.uk/species-accounts?pg={}".format(page_nr)
            page = requests.get(url, timeout=15)
            element_html = html.fromstring(page.content)
            table = element_html.xpath("//section[@class='container']")
            table_tree = lxml.etree.tostring(table[0], method='xml')
            if element_html.xpath("//a[@class='pods-pagination-label pods-pagination-next ']"): 
                page_nr = page_nr + 1
                string_scraped = string_scraped + str(table_tree)
            else:
                page_end = True
                string_scraped = string_scraped + str(table_tree)
                # print(len(string_scraped))
        except TimeoutError:
            print("Site could not be reached. Try again later.")
            continue
        except requests.exceptions.HTTPError as err:
            print("There was an error requesting the site HTTP.")
            continue
    return string_scraped

def species_check(ln_names_dict, string_scraped):
    url_builder_list = []
    status_token = "{}.*(Potential|Established)"
    habitat_token = "{}.*(Freshwater|Marine|Terrestrial|Brackish)"
    crude_name_token = "\"name\"(.*).*{}"
    name_token = ">.*</"
    string_scraped = string_scraped.split("species-data")
    out_of_89 = []
    for i in ln_names_dict.keys():
        for item in string_scraped:
            matches = re.findall(ln_names_dict[i][0], item)
            if len(matches) > 0:
                match_status = re.findall(status_token.format(ln_names_dict[i][0]), item)
                match_habitat = re.findall(habitat_token.format(ln_names_dict[i][0]), item)
                match_name_crude = re.findall(crude_name_token.format(ln_names_dict[i][0]), item)[0]
                match_name = re.findall(name_token, match_name_crude)[0][1:-2]
                match_name = match_name.replace(",","")
                match_name = match_name.replace(" ", "-")
                match_name = match_name.lower()
                check = ra_check(match_status, match_habitat, match_name)
                ln_names_dict[i].append(check)
                out_of_89.append(ln_names_dict[i][0])

    return url_builder_list, ln_names_dict

def ra_check(match_status, match_habitat, match_name):
    base_url = "https://invasivespeciesni.co.uk/species-accounts/"
    url = base_url+match_status[0]+"/"+match_habitat[0]+"/"+str(match_name)

    page = requests.get(url, timeout=15)
    element_html = html.fromstring(page.content)
    table = element_html.xpath("//section[@class='container']")
    table_tree = lxml.etree.tostring(table[0], method='xml')
    if "file-area" in str(table_tree):
        check = "ISNA - has RA: {}".format(url)
        return check
    else: 
        check = "ISNA - no RA: {}".format(url)
        return check

def main_scraper(ln_names_dict):
    string_scraped = scrape_isna()
    url_builder_list, ln_scraping_dict = species_check(ln_names_dict, string_scraped)
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