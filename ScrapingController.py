"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""
import Waarnemingen_scraper
import selenium_gtrends_scraper
from time import perf_counter
from RA_Code.RA_scraping_suite import risk_suite

def trends_controller():
    Waarnemingen_scraper.scrape_master_class()
    selenium_gtrends_scraper.GT_master_class()
    pass

def market_controller():
    # TBD, WIP
    pass

def ias_risk_controller():
    # TBD, WIP
    risk_suite()
    pass

if __name__ == "__main__":
    """
    input: Human interaction / clockwork action
    args: Run through the different classes/modules --> split them up in 3 parts 
        1. google trends analysis package.
        2. market research package.
        3. risk analysis and assessment package.
    output: Awsum Wepsaite :D
    """
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)
    trends_controller() # controls and runs all modules for the google trends analysis
    market_controller() # controls and runs all modules for the google trends analysis
    ias_risk_controller() # controls and runs all modules for the google trends analysis
    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)
