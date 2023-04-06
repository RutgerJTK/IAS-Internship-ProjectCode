from flask import Flask, render_template, request
import numpy as np
import json
import sys
import time 

file = "D:\\Project_IAS\\ProjectCode\\ias_names_big_unedited"
d = {}
with open(file) as f:
    for line in f:
        (key, val) = line.split(":")
        val = val.strip("\n")
        d[(key)] = val
f.close()

sys.stdout = open("D:\\Project_IAS\\declare.js", "w")
jsonobj = json.dumps(d)
print("var jasonstr = '{}'".format(jsonobj))


# app = Flask(__name__)


# @app.route('/')
# def main_page():
#     return render_template('index.html')

# if __name__ == "__main__":
#     # dict = read_dict()
#     # dict_to_json(dict)
#     # time.sleep(3)

#     app.run(debug="True")


