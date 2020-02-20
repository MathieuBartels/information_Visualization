import os, json

from flask import render_template, request, jsonify
from bokeh.plotting import output_file
from app import app
from app import images
from app.utils import csv_to_dict
from decimal import Decimal
import pandas as pd
import numpy as np

# basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Welcome!')

@app.route("/view2", methods = ['GET', 'POST'])
def view2():
	# output_file('view2.html')
	return render_template('view2.html', title='this is view2')

# @app.route("/view3")
# def view3():
# 	# output_file('view2.html')
# 	return render_template('view3.html', title='this is view3')

@app.route('/view3', methods = ['GET', 'POST'])
def index():
	data = csv_to_dict.h
	images = ["Bloom_2006", "Annex_2013"]
	user = {'username': 'Pepijn', 'im':'Selected Image'}
	return render_template('view3.html', user=user, images=images, data=data)
