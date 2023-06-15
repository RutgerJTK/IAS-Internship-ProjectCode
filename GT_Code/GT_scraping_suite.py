"""
Author and Copyright owner: Rutger Kemperman
Goal of script: Scrape all data from waarnemingen.nl (and maybe store it in a database)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

from time import perf_counter
import datetime
import Waarnemingen_daily

def dates_parser(file):
    with open(file, 'r+') as f:
        content = f.readline()
        old_date = datetime.datetime.strptime(content, "%Y-%m-%d").date()    
        new_date = datetime.date.today()
        if old_date > new_date:
            print("That's not supposed to happen.")
            new_date = str(new_date)
            f.seek(0)
            f.truncate()
            f.write(new_date)
            quit()  # fail-safe to keep the program from running entire code missing out vital new info that might have been included in previous iterations. 
        elif new_date > old_date:
            new_date = str(new_date)
            f.seek(0)
            f.truncate()
            f.write(new_date)
            print("New date: " , new_date)
        else:
            # print("dates are equal, don't run twice in a day!")
            print("Dates are identical")
        f.close()
    return new_date


def trends_controller():
    file = "D:\\Project_IAS\\Scraped\\Scraped_daily\\date_keep.txt"
    new_date = dates_parser(file) # controls the dates being parsed, sees to it that the right dates get scraped.
    print("Scraping Waarnemingen.nl")
    Waarnemingen_daily.main_scraper(new_date)
    print("Scraping google trends.")
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

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)
