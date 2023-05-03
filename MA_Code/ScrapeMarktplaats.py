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
import time

def scrape_mp(ln_names_dict):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    token_better = "<h3 class=\"hz-Listing-title\">.{}<span class=\"hz-Listing-priority hz-Listing-priority--all-devices\">"
    spec_matches = []
    try:
        for i in ln_names_dict.keys():
            # time.sleep(2)
            name_crude = ln_names_dict[i][0].lower()
            name = name_crude.replace(" ", "+")
            names_part = name.split("+")
            url = "https://www.marktplaats.nl/q/{}/".format(name)
            print("At part of the site: "+  url)
            page = requests.get(url, headers=agent, timeout=15)
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            soup = str(soup)
            if (len(soup)) > 1000:
                format = "{0,50}"+names_part[0]+".{1,500}"
                matches = re.findall(token_better.format(format), soup)
                if len(matches) > 0:
                    print(matches[0])
                    print(len(matches))
                    for i in range(len(matches)):
                        spec_matches.append(ln_names_dict[i][0] + " is currently for sale: "+ matches[i])
            else:
                print(soup)
                print("Got kicked out by site.")
                return spec_matches

    except TimeoutError:
        print(TimeoutError)
        pass

    return spec_matches

def write_matches(spec_matches):
    today = str(date.today())
    if len(spec_matches) > 0:
        with open(r'D:\\Project_IAS\\Scraped\\Scraped_MA\\Scraped_marktplaats.txt', 'r+') as fp:
            if ("last scraping date: " +  today) not in text:
                fp.write("last scraping date: " +  today + "\n")
            for item in spec_matches:
                fp.write("%s\n" % item)
    else:
        with open(r'D:\\Project_IAS\\Scraped\\Scraped_MA\\Scraped_marktplaats.txt', 'r+') as fp:
            text = fp.read()
            if ("last scraping date: " +  today) not in text:
                print("No new species were found, or site timeout")
                fp.write("last scraping date: " +  today + "\n")
    fp.close()
    print('Done')

def main_scraper(ln_names_dict):
    spec_matches = scrape_mp(ln_names_dict)
    write_matches(spec_matches)
    ma_scraping_dict = ln_names_dict
    return ma_scraping_dict

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
    ln_scraping_dict = main_scraper(ln_names_dict)

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)