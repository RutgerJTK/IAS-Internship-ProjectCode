"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all marketdata from blue-lagoon.
Inner workings: All species for sale are scraped, these are compared to the invasive species list. If any invasive species are being sold, the site link will be added to that species profile.
"""

from time import perf_counter
import re
import bs4 
import requests
import math
import time


def scrape_aquarium():
    url = "https://www.aquaplantsonline.nl/aquariumplanten/page{}.html?limit=72&sort=asc&brand=0&min=0&max=150"
    new_soup = ""

    try:
        url = url.format("1")
        print("At part of the site: "+  url)
        page = requests.get(url, timeout=15)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        soup = str(soup)
        soup.strip("\n")
        print("hi")
        match = re.search("h5.*Producten", soup)
        product = match.group().split(">")[1][0:3]
        nr_of_pages = math.ceil(int(product)/72)
        page.close()
        time.sleep(1)
        for i in range(nr_of_pages):
            url = "https://www.aquaplantsonline.nl/aquariumplanten/page{}.html?limit=72&sort=asc&brand=0&min=0&max=150"
            i += 1
            print(i)
            url2 = url.format(i)
            print("At part of the site: "+  url2)
            page = requests.get(url2, timeout=15)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            soup = str(soup)
            soup.strip("\n")
            print("soup")
            print(len(soup))
            new_soup += soup
            print(len(new_soup))
            page.close()
    except TimeoutError:
        print(TimeoutError)
        pass

    return new_soup

def compare_spec(ln_names_dict, store_supply, new_soup):
    counter = 0
    for i in ln_names_dict.keys():
        print(type(new_soup))
        matches = re.findall(ln_names_dict[i][0], new_soup)
        if len(matches) > 0:
            name = ln_names_dict[i][0].lower()
            name = name.replace(" ", "-")
            quote = "Species up for offer on aquaplantsonline.nl: https://www.aquaplantsonline.nl/{}.html?".format(name)
            ln_names_dict[i].append(quote)
            store_supply.append(ln_names_dict[i][0])
            counter += 1
            print(matches)

    print("-"*80)
    if counter == 0:
        print("No invasive species for sale.")
    else:
        print("Waarempel!")
        store_supply['AquaPlantsOnline.nl'][0] = counter
    return ln_names_dict, store_supply

def main_scraper(ln_names_dict, store_supply):
    new_soup = scrape_aquarium()
    ln_names_dict, store_supply = compare_spec(ln_names_dict, store_supply, new_soup)
    ma_scraping_dict = ln_names_dict
    print(ln_names_dict)
    print(store_supply)

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