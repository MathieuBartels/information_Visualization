import os, json

from flask import render_template, request, jsonify, send_from_directory

from bokeh.plotting import output_file, figure
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, Range1d

from app import app
from app import image_plotting
from app.utils.csv_to_dict import nowhere_metadata
from decimal import Decimal
import pandas as pd
import numpy as np

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

	#Create a dataframe of the csv file and sort it by name
	df = pd.read_csv("app/data/NOWHERE_DATASET.csv") 
	header = df.iloc[2]
	df = pd.DataFrame(df.values[4:], columns=header)
	df.columns.values[1] = "year"
	df.rename(columns={'1= very related': 'name'}, inplace=True)
	df.sort_values(by=['name'], inplace=True)

	#Get urls of the images and add to the dataframe
	images = os.listdir('app/static/230_works_1024x')
	images = images[0:220]
	urls = [f'/static/230_works_1024x/{image}' for image in images]
	df['urls'] = urls
	df.fillna(0, inplace=True)

	df['x1'] = [1] * 220
	df['y1'] = [1] * 220
	df['w'] = [1] * 220
	df['h'] = [1] * 220

	data_source = ColumnDataSource(df)

	xr = 10
	yr = 10

	p = figure(x_range=(0,xr), y_range=(0,yr), plot_width=1000, plot_height=1000,toolbar_location=None)
	p.image_url(url='urls', x='x1', y='y1', w='w', h='h', source=data_source)




	data = nowhere_metadata

	# images = os.listdir('app/static/230_works_1024x/')
	# urls = [f'/static/230_works_1024x/{image}' for image in images]
	# names = [image[:-4] for image in images]
	# image_to_source = {name : [source] for name, source in zip(names, urls)}

	user = {'username': 'Pepijn', 'im':'Selected Image'}

	# data_source = ColumnDataSource(image_to_source)

	# image_selection = names # TODO make this selection more fancy and maybe dynamic
	# N = min(len(image_selection), 15)
	# xr = 10
	# yr = 10
	# x1 = np.linspace(0, xr, N+1)
	# y1 = np.linspace(0, yr, N+1)

	# #Greate figure
	# p = figure(x_range=(0,xr), y_range=(0,yr), plot_width=300, plot_height=500,toolbar_location=None)
	# for i, url in enumerate(image_selection):
	# 	p.image_url(url=url, x=x1[i % 15], y=i//15, w=xr/N, h=yr/N, source=data_source)

	#Remove grid and axis
	p.xgrid.visible = False
	p.ygrid.visible = False
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
	grid = gridplot([[l_square, p, r_square]], plot_width=400, plot_height=600)

	# define the components: the javascript used and the div
	l_square_script, l_square_div = components(grid)
	
	return render_template('view3.html',
		user=user, images=images, data=data, l_square_script=l_square_script, l_square_div=l_square_div)


@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
										'favicon.ico', mimetype='image/vnd.microsoft.icon')