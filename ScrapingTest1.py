"""
Author: Rutger Kemperman
Goal of script: webscraping google trends data on a singular species
"""

import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import os  


def scrape_trends(kw_list):
    pytrends = TrendReq(hl='en-US', tz=45)
    print(pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='NL', gprop=''))
    df_interest_ot = (pytrends.interest_over_time())
    df_interest_ot.to_csv('D:\\School - all things school related\\HAN Bio-informatica\\Stage_Ru\\ProjectCode\\GTrendsTest1.csv')  


if __name__ == "__main__":
    keywords_list = ["Blockchain", "Cardano", "Ethereum"]
    scrape_trends(keywords_list)
    print('Finished scraping, best of luck with the data!')
