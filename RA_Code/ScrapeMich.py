"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

from time import perf_counter
import re
import bs4 
import requests

def scrape_mich(ln_names_dict):
    mich_urls_list = ["https://www.michigan.gov/invasives/id-report/worms", 
                      "https://www.michigan.gov/invasives/id-report/mollusks", 
                      "https://www.michigan.gov/invasives/id-report/insects", 
                      "https://www.michigan.gov/invasives/id-report/mammals", 
                      "https://www.michigan.gov/invasives/id-report/fish",
                      "https://www.michigan.gov/invasives/id-report/birds",
                      "https://www.michigan.gov/invasives/id-report/crustaceans",
                      "https://www.michigan.gov/invasives/id-report/plants/aquatic",
                      "https://www.michigan.gov/invasives/id-report/plants/grass",
                      "https://www.michigan.gov/invasives/id-report/plants/herbs",
                      "https://www.michigan.gov/invasives/id-report/plants/shrubs",
                      "https://www.michigan.gov/invasives/id-report/plants/trees",
                      "https://www.michigan.gov/invasives/id-report/plants/vines",
                      "https://www.michigan.gov/invasives/id-report/watchlist"]
    token = "(?:h3).*\n.*{}"
    counter = 0
    check_list = []
    try:
         for url in mich_urls_list:
            # print(url)
            page = requests.get(url, timeout=15)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            soup = str(soup)
            for i in ln_names_dict.keys():
                matches = re.findall(token.format(ln_names_dict[i][0]), soup)
                matches = list(set(matches))
                if len(matches) > 0:
                    matches2 = re.findall("(?<=h3.).*(?:/h3)", matches[0])
                    matches2[0] = matches2[0][0:-4]
                    conc_url = (url + "/" + matches2[0])
                    # print(matches, matches2[0])
                    # print(conc_url)
                    if matches2[0] not in check_list:
                        check_list.append(matches2[0])
                        ln_names_dict[i].append("On Michigan's watchlist: " + conc_url)


            # page.close()
    except TimeoutError:
        pass

    print(counter)
    return(ln_names_dict)

def main_scraper(ln_names_dict):
    ln_scraping_dict = scrape_mich(ln_names_dict)
    print(ln_scraping_dict)
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