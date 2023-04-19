from flask import Flask, render_template, request
import numpy as np
import json
import sys
import time 
import os
import re
import csv

filespath  = "D:\\Project_IAS\\Scraped\\Scraped_files\\"
files = os.listdir(filespath)
static_url_path = "/Project_IAS/ProjectCode/static"
gen_spec_info_dict = {}
for file in files:
    if file.endswith(".txt"):
        abs_path = (filespath + file) 
        with open(abs_path, encoding="utf-8") as f:
            stripped_content = []
            content = f.readlines()
            for line in content:
                line = line.strip("\n")
                
                stripped_content.append(line)
        gen_spec_info_dict[stripped_content[0]] = stripped_content[1:-1]
        f.close()

RA_scraped_file = "D:\\Project_IAS\\Scraped\\Scraped_RA\\Scraped_RA_info.csv"
RA_dict = {}
with open(file=RA_scraped_file) as file:
    content = file.readlines()[1:-1]
    for line in content:
        if (len(line) > 2):
            line = line.strip("\n")
            line = line.split(",")
            RA_dict[line[0]] = line[1:-1]   # line[0] is soup_id as key, line[1] is latin name, line[2:-1] are Risk Assessments.
file.close()

"""
Junk prints to get an idea of the code.
"""
print("-")
print(RA_dict.keys())
print(len(RA_dict["152"]))
print(RA_dict["152"][1:-1])
print(RA_dict["152"][0][3:-1])
print("--")
print(RA_dict["152"][2])
print(RA_dict["152"][3])
print(RA_dict["152"][4])
print(RA_dict["152"][5])


        
# print(content)



time.sleep(1)

# app = Flask(__name__, static_url_path=static_url_path)


# @app.route('/')
# def main_page():
#     return render_template('index.html', my_dict=gen_spec_info_dict, )

# @app.route('/species/<species_name>')
# def species_page(species_name):
#     selected_species = request.args.get('selected_species')
#     species_info = gen_spec_info_dict.get(species_name)
#     return render_template('species.html', species=species_info, selected_species=selected_species)

# if __name__ == "__main__":
    # app.run(debug="True")
    


