import os, json

from flask import render_template, request, jsonify, send_from_directory

from bokeh.plotting import output_file, figure
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, Range1d,  CustomJS, Slider

from app import app
from app import image_plotting
from app.utils.csv_to_dict import nowhere_metadata
from decimal import Decimal
import pandas as pd
import numpy as np

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
	data = nowhere_metadata

	# images = os.listdir('app/static/230_works_1024x/')
	# urls = [f'/static/230_works_1024x/{image}' for image in images]
	images = os.listdir('app/static/thumbnails/')
	urls = [f'/static/thumbnails/{image}' for image in images]
	names = [image[:-4] for image in images]
	image_to_source = {name : [source] for name, source in zip(names, urls)}

	user = {'username': 'Pepijn', 'im':'Selected Image'}

	data_source = ColumnDataSource(image_to_source)

	image_selection = names # TODO make this selection more fancy and maybe dynamic
	N = min(len(image_selection), 15)
	xr = 10
	yr = 10
	x1 = np.linspace(0, xr, N+1)
	y1 = np.linspace(0, yr, N+1)

	#Greate figure
	p = figure(x_range=(0,xr), y_range=(0,yr), plot_width=300, plot_height=500,toolbar_location=None)
	for i, url in enumerate(image_selection):
		p.image_url(url=url, x=x1[i % 15], y=i//15, w=xr/N, h=yr/N, source=data_source)

	#Remove grid and axis
	p.xgrid.visible = False
	p.ygrid.visible = False
	p.axis.visible = False
	p.xgrid.grid_line_color = None

	# script, div = components(p)

	# square 1
	l_square = figure(plot_width=500, plot_height=500,toolbar_location=None, tools="")
	l_square.rect([0.6], [0.6], [0.3], [0.3], color="#74ADD1")
	# l_square.square(x=[1], y=[2], size=[300], color="#74ADD1")

	l_square.axis.visible = False
	l_square.xgrid.grid_line_color = None

	# square 2
	r_square = figure(plot_width=500, plot_height=500,toolbar_location=None, tools="")
	# r_square.square(x=[1], y=[2], size=[300], color="#74ADD1")
	r_square.rect([0.6], [0.6], [0.3], [0.3], color="#74ADD1")
	r_square.axis.visible = False
	r_square.xgrid.grid_line_color = None

	# the layout is a grid: square -- image -- square
	grid = gridplot([[l_square, p]], plot_width=600, plot_height=600, toolbar_location = None)

	# define the components: the javascript used and the div
	l_square_script, l_square_div = components(grid)
	
	return render_template('view3.html',
		user=user, images=images, data=data, l_square_script=l_square_script, l_square_div=l_square_div)
	# return render_template('view3.html', title='Welcome!')

@app.route("/view2", methods = ['GET', 'POST'])
def view2():
	data = nowhere_metadata

	# images = os.listdir('app/static/230_works_1024x/')
	# urls = [f'/static/230_works_1024x/{image}' for image in images]
	images = os.listdir('app/static/thumbnails/')
	urls = [f'/static/thumbnails/{image}' for image in images]
	names = [image[:-4] for image in images]
	image_to_source = {name : [source] for name, source in zip(names, urls)}

	user = {'username': 'Pepijn', 'im':'Selected Image'}

	data_source = ColumnDataSource(image_to_source)

	image_selection = names # TODO make this selection more fancy and maybe dynamic
	N = min(len(image_selection), 15)
	xr = 10
	yr = 10
	x1 = np.linspace(0, xr, N+1)
	y1 = np.linspace(0, yr, N+1)

	#Greate figure
	p = figure(x_range=(0,xr), y_range=(0,yr), plot_width=300, plot_height=500,toolbar_location=None)
	for i, url in enumerate(image_selection):
		p.image_url(url=url, x=x1[i % 15], y=i//15, w=xr/N, h=yr/N, source=data_source)

	#Remove grid and axis
	p.xgrid.visible = False
	p.ygrid.visible = False
	p.axis.visible = False
	p.xgrid.grid_line_color = None

	# script, div = components(p)

	# right square
	r_square = figure(plot_width=500, plot_height=500,toolbar_location=None, tools="")
	# r_square.square(x=[1], y=[2], size=[300], color="#74ADD1")
	r_square.rect([0.6], [0.6], [0.3], [0.3], color="#74ADD1")
	r_square.axis.visible = False
	r_square.xgrid.grid_line_color = None

	amp_slider = Slider(start=0.1, end=10, value=1, step=.1, title="Amplitude")
	# freq_slider = Slider(start=0.1, end=10, value=1, step=.1, title="Frequency")
	# phase_slider = Slider(start=0, end=6.4, value=0, step=.1, title="Phase")
	# offset_slider = Slider(start=-5, end=5, value=0, step=.1, title="Offset")

	# the layout is a grid: square -- image -- square
	grid = gridplot([[p, r_square]], plot_width=600, plot_height=600, toolbar_location = None, sizing_mode='scale_both')

	# define the components: the javascript used and the div
	l_square_script, l_square_div = components(grid)
	
	return render_template('view2.html',
		user=user, images=images, data=data, l_square_script=l_square_script, l_square_div=l_square_div)
	# output_file('view2.html')
	# return render_template('view2.html', title='this is view2')

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
										'favicon.ico', mimetype='image/vnd.microsoft.icon')