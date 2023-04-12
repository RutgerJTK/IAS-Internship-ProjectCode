"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

from time import perf_counter
import re
import bs4 
import requests


def scrape_gisd(ln_names_dict):
    token = re.compile("//li//a//small")
    gisd_list = []
    counter = 0
    try:
        for i in ln_names_dict.keys():
            print(counter)
            counter += 1
            soup2 = ""
            url = "http://www.iucngisd.org/gisd/speciesname/" + ln_names_dict[i][0]
            page = requests.get(url, timeout=15)
            soup = str(bs4.BeautifulSoup(page.text, 'html.parser'))
            soup2 += ln_names_dict[i][0] + "\n"
            soup2 += soup
            gisd_list.append(soup2)
        # write_soup(soup2)
    except TimeoutError:
        pass
    return(gisd_list)

def write_soup(soup2):      # Temp file, don't actually use this.
    print(len(soup2))
    print(type(soup2))
    with open('D:\\Project_IAS\\Scraped\\Scraped_RA\\Scraped_GISD_soup.txt', 'w', encoding="utf-8") as f:
        print("here")
        f.write(soup2)
    f.close()

def get_gisd_spec(ln_names_dict, gisd_list):
    url = "http://www.iucngisd.org/gisd/speciesname/"
    impact_token = re.compile("javascript:;.{2}(?:Not Evaluated|No Alien Population|Data Deficient|Minimal Concern|Minor|Moderate|Major|Massive)")
    impact_short = ">.*"
    absent_token = re.compile("is not present yet in our archive.")
    counter = 0

    for count, value in enumerate(ln_names_dict.keys()):
        matches = []
        absent = []
        matches = re.findall(impact_token, gisd_list[count])
        matches = list(set(matches))
        absent = re.findall(absent_token, gisd_list[count])
        absent = list(set(absent))
        if len(matches) > 0:
            # print(ln_names_dict[value][0] + ": " + matches[0])
            spec_match = re.findall(impact_short, matches[0])
            name = ln_names_dict[value][0]
            name = name.replace(" ", "+")
            spec_url = url + name
            quote = "Species EICAT classification: " + spec_match[0] + " on: " + spec_url
            ln_names_dict[value].append(quote)
            counter += 1
        elif len(absent) > 0:
            pass
        else:
            counter += 1
            name = ln_names_dict[value][0]
            name = name.replace(" ", "+")
            spec_url = url + name
            quote = "Species general info available on: " + spec_url
            ln_names_dict[value].append(quote)

    return ln_names_dict

def main_scraper(ln_names_dict):
    gisd_list = scrape_gisd(ln_names_dict)
    ln_scraping_dict = get_gisd_spec(ln_names_dict, gisd_list)
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