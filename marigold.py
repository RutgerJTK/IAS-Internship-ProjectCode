from flask import Flask, render_template, request
import numpy as np
import json
import sys
import time 
import os


filespath  = "D:\\Project_IAS\\Scraped\\Scraped_files\\"
files = os.listdir(filespath)
static_url_path = "/Project_IAS/ProjectCode/static"
gen_spec_info_dict = {}
for file in files:
    if file.endswith(".txt"):
        # print("+"*80)
        abs_path = (filespath + file) 
        with open(abs_path, encoding="utf-8") as f:
            stripped_content = []
            content = f.readlines()
            for line in content:
                line = line.strip("\n")
                stripped_content.append(line)
        gen_spec_info_dict[stripped_content[0]] = stripped_content[1:-1]
            # print(content[0])
        f.close()
# print(gen_spec_info_dict)
            # for line in f:
            #     (key, val) = line.split(" $$$ ")
            #     val = val.strip("\n")
time.sleep(1)

app = Flask(__name__, static_url_path=static_url_path)


@app.route('/')
def main_page():
    return render_template('index.html', my_dict=gen_spec_info_dict, )

@app.route('/species/<species_name>')
def species_page(species_name):
    selected_species = request.args.get('selected_species')
    species_info = gen_spec_info_dict.get(species_name)
    return render_template('species.html', species=species_info, selected_species=selected_species)

if __name__ == "__main__":
    # dict = read_dict()
    # dict_to_json(dict)
    # time.sleep(3)

    app.run(debug="True")


