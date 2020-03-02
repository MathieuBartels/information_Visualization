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
<<<<<<< Updated upstream
	return render_template('home.html', title='Welcome!')
=======
	data = nowhere_metadata
	print(type(data.human_factor))
	
	data2 = pd.DataFrame(dict(data.human_factor), index = ['Politics', 'Corporate', 'Private', 'Public', 'Interaction']) 
	print(data2['CH-1995-1'])
	source = ColumnDataSource(data=data2)
	print(source)
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

	# TODO active sliders need to be created when a click happens on the image
	# 1) click happens on image 2) top values of the image become active filters 3) slider changes the csv file
	test_image = 'CH-1995-3' # this needs to be the on-click image
	# available_filters = list(data.human_factor[test_image].keys()) # oeps pepijn is a bad programmer, how to get the sub-subjects which are not there????
	slider_1_value = 'Private'
	slider_2_value = "Public"
	slider_3_value = 'Interaction'

	active_text = TextInput(value="", title="Active Filters")
	# active_1 = Slider(title=slider_1_value, value=data.human_factor[test_image][slider_1_value], start=0, end=1, step=0.01)
	# active_2 = Slider(title=slider_2_value, value=data.human_factor[test_image][slider_2_value], start=0, end=1, step=0.01)
	# active_3 = Slider(title=slider_3_value, value=data.human_factor[test_image][slider_3_value], start=0, end=1, step=0.01)
	active_1 = Slider(title=slider_1_value, value=0.6, start=0, end=1, step=0.01)
	active_2 = Slider(title=slider_2_value, value=0.6, start=0, end=1, step=0.01)
	active_3 = Slider(title=slider_3_value, value=0.6, start=0, end=1, step=0.01)
	# active_4 = Slider(title="Corporate", value=0.3, start=0, end=1, step=0.01)
	# active_5 = Slider(title="Politics", value=0.3, start=0, end=1, step=0.01)
	# jvscript = """
	# 	var f = cb_obj.value;
	# 	var sdata = source.data;

	# 	console.log(sdata);

	# 	for (key in sdata) {console.log(key);}

	# 	if (f == "source") {
	# 	for (key in sdata) {
	# 		sdata[key].push(data1[key][i]);
	# 		}
	# 	}

	# 	source.trigger("change");
	# 	"""
	# active_1.callback = CustomJS(args=dict(source=source),code=jvscript)

	# button_grid = column([btn_geography],[btn_reality],[btn_humanfactor],[btn_domains],[btn_goals], [btn_means], [btn_myapproach], [btn_contenttome])
	button_grid = column([btn_geography, btn_reality, btn_humanfactor, btn_domains, btn_goals, btn_means, btn_myapproach, btn_contenttome, active_text, active_1, active_2, active_3])

	# define the components: the javascript used and the div
	grid = layout([[button_grid,p]])

	l_square_script, l_square_div = components(grid)

	return render_template('home.html',
		user=user, images=images, data=data, l_square_script=l_square_script, l_square_div=l_square_div)
	# return render_template('view3.html', title='Welcome!')
>>>>>>> Stashed changes

@app.route("/view2", methods = ['GET', 'POST'])
def view2():
	# output_file('view2.html')
	return render_template('view2.html', title='this is view2')

@app.route('/view3', methods = ['GET', 'POST'])
def index():
	data = nowhere_metadata

	images = os.listdir('app/static/230_works_1024x/')
	urls = [f'/static/230_works_1024x/{image}' for image in images]
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