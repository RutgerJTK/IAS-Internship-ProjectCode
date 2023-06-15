"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all marketdata from blue-lagoon.
Inner workings: All species for sale are scraped, these are compared to the invasive species list. If any invasive species are being sold, the site link will be added to that species profile.
"""

from time import perf_counter
import re
import bs4 
import requests
from requests_respectful import RespectfulRequester
from datetime import date

def scrape_mp():
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    token_better = "elementor-heading-title elementor-size-medium.*h3"
    total_supply = []
    try:
        url = "https://animalattraction.nl/?s=&Soort=*&herkomst=*"
        page = requests.get(url, headers=agent, timeout=45)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        soup = str(soup)
        supply = re.findall(token_better, soup)
        if len(supply) > 0:
            total_supply = supply
    except TimeoutError:
        print(TimeoutError)
        pass

    return total_supply

def check_spec(total_supply, ln_names_dict, store_supply):
    x = False
    counter = 0
    for i in range(len(total_supply)):
        total_supply[i] = total_supply[i][47:-4]

    for i in ln_names_dict.keys():
        if ln_names_dict[i][0] in total_supply:
            x = True  
            counter += 1 
            print(ln_names_dict[i][0])
            quote = "For sale on: https://animalattraction.nl/?s=&Soort=*&herkomst=*"
            if quote not in ln_names_dict[i]:
                ln_names_dict[i].append(quote)
                store_supply['AnimalAttraction'].append(ln_names_dict[i][0])
    if x == False:
        print("No IAS for sale in the online Animal attraction store at present time.")

    store_supply['AnimalAttraction'][0] = counter
    return ln_names_dict, store_supply

def main_scraper(ln_names_dict, store_supply):
    total_supply = scrape_mp()
    ma_scraping_dict, store_supply = check_spec(total_supply, ln_names_dict, store_supply)
    return ma_scraping_dict, store_supply

if __name__ == "__main__":
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    ias_file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = {}
    try: 
        import MA_scraping_suite
    except ModuleNotFoundError:
        from MA_Code import MA_scraping_suite

    ln_names_dict = MA_scraping_suite.read_file(ias_file)
    store_supply = MA_scraping_suite.MA_store_nrs()
    ln_scraping_dict, store_supply = main_scraper(ln_names_dict, store_supply)

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)