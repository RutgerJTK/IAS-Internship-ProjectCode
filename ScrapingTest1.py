"""
Author: Rutger Kemperman
Goal of script: webscraping google trends data on a singular species
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import pandas as pd


def scraping(name1, name2):
    print(name1, name2)
    options = Options()
    driver = webdriver.Chrome("https://trends.google.com/trends/explore?geo=NL&q=nijlgans,Alopochen%20aegyptiaca", options=options)
    # driver.get("https://trends.google.com/trends/explore?geo=NL&q=nijlgans,Alopochen%20aegyptiaca")
    driver.find_elements_by_xpath('(//button[@class="widget-actions-item export" and @title="CSV"]//i)[1]').click()
    # print(download_bttn)


if __name__ == "__main__":
    species_name = "golden bell frog"
    species_name_latin = "Litoria aurea"
    scraping(species_name, species_name_latin)
