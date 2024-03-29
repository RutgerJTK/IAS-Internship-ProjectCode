"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all marketdata from Welle diertotaal.
Inner workings: All species for sale are scraped, these are compared to the invasive species list. If any invasive species are being sold, the site link will be added to that species profile.
"""

from time import perf_counter
import re
import bs4 
import requests


def scrape_welle():
    url = "https://www.wellediertotaal.nl/c-5408932/actuele-dierenlijst"
    sell_list = []
    new_soup = ""
    try:
        print("At part of the site: "+  url)
        page = requests.get(url, timeout=15)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        soup = str(soup)
        soup.strip("\n")
        for i in soup:
            if i != "\n":
                new_soup += i
        
    except TimeoutError:
        print(TimeoutError)
        pass

    return sell_list, new_soup

def compare_spec(ln_names_dict, new_soup, store_supply):
    counter = 0
    new_soup = new_soup.split(">")
    print(len(new_soup))
    new_soup = new_soup[500:1260]
    print(len(new_soup))
    site_offers_list = []
    for i in range(len(new_soup)):
        match = re.search("(?:[0-9][.][0-9]).*", new_soup[i])
        if match:
            print(match.group())
            site_offers_list.append(match.group())
            # counter += 1

    print("+"*80)
    if len(site_offers_list) > 0:
        for i in ln_names_dict.keys():
            for j in range(len(site_offers_list)):  
                token = ln_names_dict[i][0].lower()
                matches = re.findall(token, site_offers_list[j])
                if matches:
                    quote = "$Sold on https://www.wellediertotaal.nl/c-5408932/actuele-dierenlijst:$ " +  site_offers_list[j][4:-4]
                    ln_names_dict[i].append(quote)
                    store_supply['Welle Diertotaal'].append(ln_names_dict[i][0])
                    counter += 1
    if counter > 0:
        store_supply['Welle Diertotaal'][0] = counter

    print(ln_names_dict)
    print(counter)
    print(store_supply)
    return ln_names_dict, store_supply

def main_scraper(ln_names_dict, store_supply):
    sell_list, new_soup = scrape_welle()
    ln_names_dict, store_supply = compare_spec(ln_names_dict, new_soup, store_supply)
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