from flask import Flask, render_template, request
import numpy as np
import json
import sys
import time 
import os
import re
import csv
import marigold_boot_req

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html', my_dict=gen_spec_info_dict )

@app.route('/species/<species_name>')
def species_page(species_name):
    selected_species = request.args.get('selected_species')
    species_info = gen_spec_info_dict.get(species_name)
    return render_template('species.html', species=species_info, selected_species=selected_species)

if __name__ == "__main__":
    names_dict, static_url_path, gen_spec_info_dict, RA_dict = marigold_boot_req.main()
    app.static_url_path=static_url_path
    app.config['NAMES_DICT'] = names_dict
    app.run()
    
