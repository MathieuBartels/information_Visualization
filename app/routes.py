import os, json

from bokeh.events import ButtonClick
from flask import render_template, request, jsonify, send_from_directory

from bokeh.plotting import output_file, figure
from bokeh.embed import components
from bokeh.layouts import row, column, widgetbox, layout, gridplot
from bokeh.models import ColumnDataSource, Range1d,  CustomJS, Slider
from bokeh.models import ColumnDataSource, Range1d, CustomJS

from bokeh.io import output_file, show
from bokeh.models.widgets import Button


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

	#Creating a dataframe that can be used for the bokeh input
	df = pd.read_csv("app/data/NOWHERE_DATASET.csv") 
	header = df.iloc[2]
	df = pd.DataFrame(df.values[4:], columns=header)
	df.rename(columns={'1= very related': 'name'}, inplace=True)
	df.columns.values[1] = "year"	
	df.fillna(0, inplace=True)
	df.sort_values(by=['name'], inplace=True)
	df['rank'] = range(1, 221)
	
	#Get urls of the images and add to the dataframe
	images = os.listdir('app/static/230_works_1024x')
	images = images[0:220]
	urls = [f'/static/230_works_1024x/{image}' for image in images]
	df['urls'] = urls
	
	#Plot formatting
	image_height = 1
	image_width = 1
	per_row = 10
	xr = per_row * image_width
	yr = 220 / per_row * image_height

	#Add columns to the dataframe for the placing and formatting
	df['w'] = [image_width] * 220
	df['h'] = [image_height] * 220
	df['x1'] = (df['rank'] - 1) % per_row
	df['y1'] = yr - (df['rank'] - 1) // per_row
	
	data_source = ColumnDataSource(df)

	p = figure(x_range=(0,xr), y_range=(0,yr), plot_width=2000, plot_height=2000, toolbar_location=None)
	p.image_url(url='urls', x='x1', y='y1', w='w', h='h', source=data_source)


	# images = os.listdir('app/static/230_works_1024x/')
	# urls = [f'/static/230_works_1024x/{image}' for image in images]
	# images = os.listdir('app/static/thumbnails/')
	# urls = [f'/static/thumbnails/{image}' for image in images]
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

	

	btn_geography = Button(label="Geography", button_type="primary")
	btn_reality = Button(label="Reality", button_type="danger")
	btn_humanfactor = Button(label="Human Factor", button_type="warning")
	btn_domains = Button(label="Domains", button_type="success")
	btn_goals = Button(label="Goals", button_type="success")
	btn_means = Button(label="Means", button_type="warning")
	btn_myapproach = Button(label="My Approach", button_type="danger")
	btn_contenttome = Button(label="Content To Me", button_type="primary")
	# button_grid = column([btn_geography],[btn_reality],[btn_humanfactor],[btn_domains],[btn_goals], [btn_means], [btn_myapproach], [btn_contenttome])
	button_grid = column([btn_geography, btn_reality, btn_humanfactor, btn_domains, btn_goals, btn_means, btn_myapproach, btn_contenttome])

	# but_script, but_div = components(button_grid)
	
	# the layout is a grid: square -- image -- square
	# grid = gridplot([[grid, p]], plot_width=600, plot_height=600, toolbar_location = None)

	# define the components: the javascript used and the div
	grid = layout([[button_grid,p]])
	
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

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
										'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/filter", methods = ['GET', 'POST'])
def filter():

	#Buttons Maybe use for-loop?
	btn_geography = Button(label="Geography", button_type="primary")
	btn_reality = Button(label="Reality", button_type="danger")
	btn_humanfactor = Button(label="Human Factor", button_type="warning")
	btn_domains = Button(label="Domains", button_type="success")
	btn_goals = Button(label="Goals", button_type="success")
	btn_means = Button(label="Means", button_type="warning")
	btn_myapproach = Button(label="My Approach", button_type="danger")
	btn_contenttome = Button(label="Content To Me", button_type="primary")

	grid = gridplot([[btn_geography],[btn_reality],[btn_humanfactor],[btn_domains],[btn_goals], [btn_means], [btn_myapproach], [btn_contenttome]])

	script, div = components(grid)
	#Components for placing it on html
	script0, div0 = components(btn_geography)
	script1, div1 = components(btn_reality)
	script2, div2 = components(btn_humanfactor)
	script3, div3 = components(btn_domains)
	script4, div4 = components(btn_goals)
	script5, div5 = components(btn_means)
	script6, div6 = components(btn_myapproach)
	script7, div7 = components(btn_contenttome)


	return render_template('filter.html', title='this is left square',
						   script0=script0, div0=div0, btn_geography=btn_geography,
						   script1=script1, div1=div1, btn_reality=btn_reality,
						   script2=script2, div2=div2, btn_humanfactor=btn_humanfactor,
						   script3=script3, div3=div3, btn_domains=btn_domains,
						   script4=script4, div4=div4, btn_goals=btn_goals,
						   script5=script5, div5=div5, btn_means=btn_means,
						   script6=script6, div6=div6, btn_myapproach=btn_myapproach,
						   script7=script7, div7=div7, btn_contenttome=btn_contenttome)