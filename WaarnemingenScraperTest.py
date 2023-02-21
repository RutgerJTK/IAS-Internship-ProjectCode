"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

"""
#ToDo
- make list of dates to check
for i in dates_list: go to site --> scrape all --> store.

Notes (depending on how data is scraped):
from scraped data store all unique species names in a list (if not in - mysql - table)

"""

import datetime
import pandas as pd

from bs4 import BeautifulSoup
from lxml import etree
import requests


# # initializing date
# test_date = datetime.datetime.strptime("01-7-2022", "%d-%m-%Y")
 
# # initializing K
# K = 5
 
# date_generated = pd.date_range(test_date, periods=K)

# print(date_generated.strftime("%d-%m-%Y"))

# for date in date_generated:

# def save_html(html, path):
#     with open()

def scrape_waarnemingen():
    url = "https://waarneming.nl/fieldwork/observations/daylist/?date=2023-02-21&species_group=9&province=&rarity=&search="
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    dom = etree.HTML(str(soup))
    spec_name_nl = (dom.xpath("//span[@class='species-common-name']"))
    
    for i in range(len(spec_name_nl)):
        print(spec_name_nl[i].text)


if __name__ == "__main__":
    # save_html(html, path):
    scrape_waarnemingen()