from time import perf_counter

def read_file(ias_names):
    try:
        ln_names_dict = {}
        with open(ias_names) as f:
            content = f.readlines()
        
        for line in content:
            temp_dict = line.split(": ")
            temp_dict[1] = int(temp_dict[1].strip('\n'))
            ln_names_dict.update({temp_dict[1] : [temp_dict[0]]})
        return ln_names_dict
    except IOError as ioe:
        print(ioe)

def risk_suite():
    ias_file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
    ln_names_dict = read_file(ias_file)
    try:
        import ScrapeNobanis, ScrapeISNA
        ln_names_dict = ScrapeNobanis.main_scraper(ln_names_dict)
        ln_names_dict = ScrapeISNA.main_scraper(ln_names_dict)

    except ModuleNotFoundError:
        from RA_Code import ScrapeNobanis
        # ScrapeNobanis.main_scraper(ln_names_dict)


if __name__ == "__main__":
    """

    """
    t1_start = perf_counter()   
    print( "-" * 80, "\n", "Controller start", "\n", "-" * 80)

    risk_suite()

    print("-" * 80, "\n", "Controller end, script finished", "\n", "-" * 80)
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start) 
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)