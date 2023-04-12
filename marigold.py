from flask import Flask, render_template, request
import numpy as np
import json
import sys
import time 
import os

filespath  = "D:\\Project_IAS\\Scraped\\Scraped_files\\"
files = os.listdir(filespath)

# d = {}

for file in files:
    if file.endswith(".txt"):
        # print("+"*80)
        abs_path = (filespath + file) 
        with open(abs_path) as f:
            content = f.readlines()
            print(content)
        f.close()

            # for line in f:
            #     (key, val) = line.split(" $$$ ")
            #     val = val.strip("\n")





# sys.stdout = open("D:\\Project_IAS\\declare.js", "w")
# jsonobj = json.dumps(d)
# print("var jasonstr = '{}'".format(jsonobj))


# app = Flask(__name__)


# @app.route('/')
# def main_page():
#     return render_template('index.html', my_dict=d)

# if __name__ == "__main__":
#     # dict = read_dict()
#     # dict_to_json(dict)
#     # time.sleep(3)

#     app.run(debug="True")


