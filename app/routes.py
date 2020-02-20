import os, json

from flask import render_template, request, jsonify
from bokeh.plotting import output_file, figure
# from bokeh.io import curdoc
from bokeh.embed import components
from bokeh.layouts import gridplot

from app import app
from app import image_plotting
from app.utils import csv_to_dict
from decimal import Decimal
import pandas as pd
import numpy as np

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Welcome!')

@app.route("/view2", methods = ['GET', 'POST'])
def view2():
	# output_file('view2.html')
	return render_template('view2.html', title='this is view2')

@app.route('/view3', methods = ['GET', 'POST'])
def index():
	data = csv_to_dict.h
	images = ["Bloom_2006", "Annex_2013"]
	user = {'username': 'Pepijn', 'im':'Selected Image'}
	
	# TODO make the base url working, the direction is right, but no idea why it doesn't show
	url = f"{basedir}\\data\\230_works_1024x\\13aeroplanes_1998.jpg"
	url_2 = "https://github.com/MathieuBartels/information_visualization/blob/master/app/data/230_works_1024x/13aeroplanes_1998.jpg?raw=true"
	
	p = figure(plot_width=300, plot_height=300,toolbar_location=None)
	# p.image_url(url=[url01], x=0, y=100, w=50, h=50)
	p.image_url(url=[url_2], x=0, y=200, w=50, h=50)
	p.axis.visible = False
	p.xgrid.grid_line_color = None

	# script, div = components(p)

	# square 1
	l_square = figure(plot_width=500, plot_height=500,toolbar_location=None, tools="")
	# l_square.square(x=[1], y=[2], size=[300], color="#74ADD1")
	l_square.square(x=[1], y=[2], size=[300], color="#74ADD1")
	l_square.axis.visible = False
	l_square.xgrid.grid_line_color = None

	# square 2
	r_square = figure(plot_width=500, plot_height=500,toolbar_location=None, tools="")
	r_square.square(x=[1], y=[2], size=[300], color="#74ADD1")
	r_square.axis.visible = False
	r_square.xgrid.grid_line_color = None

	# the layout is a grid: square -- image -- square
	grid = gridplot([[l_square, p, r_square]], plot_width=400, plot_height=400)

	# define the components: the javascript used and the div
	l_square_script, l_square_div = components(grid)
	
	return render_template('view3.html',
		user=user, images=images, data=data, l_square_script=l_square_script, l_square_div=l_square_div)
