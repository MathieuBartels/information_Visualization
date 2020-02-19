from flask import render_template, request, jsonify
from bokeh.plotting import output_file
from app import app
from app import images
import os, json

from decimal import Decimal

import pandas as pd
import numpy as np



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Welcome!')

@app.route("/view2")
def view2():
	output_file('view2.html')
	plot = images.show_img()
	jsonify(plotData=plot)
	return render_template('view2.html')
	# return jsonify(plotData=plot)