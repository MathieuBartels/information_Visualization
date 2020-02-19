from flask import render_template, request, jsonify
from bokeh.plotting import output_file
from app import app
from app import images, csv_to_dict
import os, json

from decimal import Decimal

import pandas as pd
import numpy as np
# import collections



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Welcome!')

@app.route("/view2")
def view2():
	# output_file('view2.html')
	return render_template('view2.html', title='this is view2')

# @app.route("/view3")
# def view3():
# 	# output_file('view2.html')
# 	return render_template('view3.html', title='this is view3')

@app.route('/view3')
def index():
	data = csv_to_dict.h
	images = ["Bloom_2006", "Annex_2013"]
	user = {'username': 'Pepijn', 'im':'Selected Image'}
	return render_template('view3.html', user=user, images=images, data=data)
