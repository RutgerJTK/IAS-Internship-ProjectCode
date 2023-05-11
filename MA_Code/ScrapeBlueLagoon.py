"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all marketdata from blue-lagoon.
Inner workings: All species for sale are scraped, these are compared to the invasive species list. If any invasive species are being sold, the site link will be added to that species profile.
"""

from time import perf_counter
import re
import bs4 
import requests


def scrape_blue():
    url_list = ["https://www.blue-lagoon.nl/levende-dieren/amfibieen.html?product_list_limit=36", "https://www.blue-lagoon.nl/dieren/hagedissen?product_list_limit=36", 
                "https://www.blue-lagoon.nl/dieren/slangen?product_list_limit=36", "https://www.blue-lagoon.nl/dieren/schildpadden?product_list_limit=36", 
                "https://www.blue-lagoon.nl/dieren/geleedpotigen?product_list_limit=36", "https://www.blue-lagoon.nl/dieren/weekdieren?product_list_limit=36"]
    costs_token = re.compile("data-price-amount.*data-price-type")
    species_token = re.compile("href.*tabindex")
    specific_species_token = re.compile(".nl.*.html")
    sell_list = []
    try:
        for url in url_list:
            new_soup = ""
            print("At part of the site: "+  url)
            page = requests.get(url, timeout=15)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            soup = str(soup)
            soup.strip("\n")
            for i in soup:
                if i != "\n":
                    new_soup += i
            new_soup = new_soup.split("item product product-item")
            new_soup = new_soup[1:]
            for i in new_soup:
                species = re.findall(species_token, i)
                matches = re.findall(costs_token, i)
                species2 = (re.findall(specific_species_token, species[0]))[0][4:-5]
                matches2 = (re.findall('\".*\"', matches[0]))[0][1:-1]
                matches2 = round(float(matches2), 2)
                supply = "Species: " + species2 + ", Sells for: " + str(matches2)
                sell_list.append(supply)
    except TimeoutError:
        print(TimeoutError)
        pass

    return sell_list

def compare_spec(ln_names_dict, sell_list, store_supply):
    counter = 0
    for i in ln_names_dict.keys():
        for j in range(len(sell_list)):
            matches = re.findall(ln_names_dict[i][0], sell_list[j])
            if matches:
                ln_names_dict[i].append(sell_list[j])
                store_supply['Blue-Lagoon'].append(ln_names_dict[i][0])
                counter += 1
                print(matches)
    print("-"*80)
    if counter == 0:
        print("No invasive species for sale.")
    else:
        print("Waarempel!")
        store_supply['Blue-Lagoon'][0] += counter
    return ln_names_dict, store_supply

def main_scraper(ln_names_dict, store_supply):
    sell_list = scrape_blue()
    ln_names_dict, store_supply = compare_spec(ln_names_dict, sell_list, store_supply)
    ma_scraping_dict = ln_names_dict
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