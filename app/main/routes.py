import os, json
import random
from bokeh.events import ButtonClick, Tap, Press, MouseMove
from flask import render_template, request, jsonify, send_from_directory

from bokeh.plotting import output_file, figure
from bokeh.embed import components
from bokeh.layouts import row, column, widgetbox, layout, gridplot
from bokeh.models import ColumnDataSource, Range1d,  CustomJS, Slider, HoverTool, OpenURL, TapTool

from bokeh.io import output_file, show
from bokeh.models.glyphs import Text
from bokeh.models.widgets import PreText
from bokeh.models import Label
from bokeh.models.widgets import Button, TextInput, Select, CheckboxGroup

from . import main
from app import image_plotting, data
from decimal import Decimal
import pandas as pd
import numpy as np


@main.route('/', methods = ['GET', 'POST'])
@main.route('/home', methods = ['GET', 'POST'])
def home():
	df = data.df

	df['filter_1'] = ""
	df['filter_2'] = ""
	df['filter_3'] = ""
	
	data_source = ColumnDataSource(data=df)

	TOOLTIPS = [
		('Name', "@name"),
		('Rank', "@rank"),
		('filter 1', "@filter_1"),
		('filter 2', "@filter_2"),
		('filter 3', "@filter_3"),
	]


	p = figure(x_range=(0, data.x_range), y_range=(0, data.y_range), plot_width=1000, plot_height=4000, tools='hover, wheel_zoom', tooltips=TOOLTIPS, toolbar_location=None)
	p.image_url(url='urls', x='x1', y='y1', w='w', h='h', source=data_source)

	p.quad(top='y1', bottom= 'y2', left='x1', right='x2', source=data_source, alpha=0)

	p.js_on_event(Tap, CustomJS(args=dict(data=data_source, per_row=data.per_row, rows=data.rows), code="""


		console.log(data)
		const getKey = (obj,val) => Object.keys(obj).find(key => obj[key] === val);

		let x = Math.ceil(cb_obj.x);
		let y = Math.ceil(cb_obj.y+1);

		let data_rank = (rows - y) * per_row + x
		
		let data_index = getKey(data['attributes']['data']['rank'], data_rank)

		window.location.href = '/view2/' + data['attributes']['data']['name'][data_index]; //relative to domain

	"""))

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

	human_factor_sources = ColumnDataSource(data=data.human_factor_data)
	geography_sources = ColumnDataSource(data=data.geography_data)
	reality_sources = ColumnDataSource(data=data.reality_data)
	domains_sources = ColumnDataSource(data=data.domains_data)
	goals_sources = ColumnDataSource(data=data.goals_data)
	means_sources = ColumnDataSource(data=data.means_data)
	my_approach_sources = ColumnDataSource(data=data.my_approach_data)
	content_to_me_sources = ColumnDataSource(data=data.content_to_me_data)

	# TODO active sliders need to be created when a click happens on the image
	# 1) click happens on image 2) top values of the image become active filters
	# So this needs to communicate with the buttons which is not hard, and the subsubjects is also not hard
	# the hard thing could be that this needs to change on click, so the sliders will need to change on a click of the button, how to do???
	sources = [human_factor_sources, geography_sources, reality_sources,domains_sources,
		goals_sources, means_sources, my_approach_sources, content_to_me_sources]

	# only the first works because of the hard-coded sliders
	sources = sources[0]

	btn_geography = Button(label="Geography", button_type="primary", width=150 )
	btn_reality = Button(label="Reality", button_type="danger", width=150)
	btn_humanfactor = Button(label="Human Factor", button_type="warning", width=150)
	btn_domains = Button(label="Domains", button_type="success", width=150)
	btn_goals = Button(label="Goals", button_type="success", width=150)
	btn_means = Button(label="Means", button_type="warning", width=150)
	btn_myapproach = Button(label="My Approach", button_type="danger", width=150)
	btn_contenttome = Button(label="Content To Me", button_type="primary", width=150)


	def get_active(column):
		return [index for index, value in  enumerate(column) if data.active[value][0]]

	cb_reality = CheckboxGroup(labels=list(data.reality_data.columns), active=get_active(data.reality_data.columns))
	cb_geography = CheckboxGroup(labels=list(data.geography_data.columns), active=get_active(data.geography_data.columns))
	cb_humanfactor = CheckboxGroup(labels=list(data.human_factor_data.columns), active=get_active(data.human_factor_data.columns))
	cb_domains = CheckboxGroup(labels=list(data.domains_data.columns), active=get_active(data.domains_data.columns))
	cb_goals = CheckboxGroup(labels=list(data.goals_data.columns), active=get_active(data.goals_data.columns))
	cb_means = CheckboxGroup(labels=list(data.means_data.columns), active=get_active(data.means_data.columns))
	cb_myapproach = CheckboxGroup(labels=list(data.my_approach_data.columns), active=get_active(data.my_approach_data.columns))
	cb_contenttome = CheckboxGroup(labels=list(data.content_to_me_data.columns), active=get_active(data.content_to_me_data.columns))

	# The names of the sub-catogory data instead of sources is the pandas df
	sub_cat_names = data.human_factor_data.columns

	

     # TODO this needs to be an on-click image, now its just a random image
	# print(test_image)
	# test_image = random.choice(list(data.naming_convention.keys()))

	#Dictionary for all the sliders
	all_sliders = {}

	topic_to_idx = {'Corporate':[1], 'Politics': [0], 'Private':[2], 'Public':[3],'Interaction':[4]}
	
	active_text = PreText(text="Active Filters",width=200, height=40)


	# leave this after the sliders because this thing is not a dict
	topic_to_idx = ColumnDataSource(topic_to_idx)

	# create a list of the active sliders
	# all_sliders = [active_1, active_2, active_3, active_4, active_5]

	# copy_data_source = ColumnDataSource(data=df)

	#Dictionary for all the sliders
	all_sliders = {}
	
	# Create all sliders and set them to invisible
	for index in data.slider_index_total:
		for sliders in index:
			all_sliders[sliders] = Slider(title=sliders, value=data.active[sliders][1], start=0, end=1, step=0.01)
			all_sliders[sliders].visible = data.active[sliders][0] 

	callback = CustomJS(args=dict(source=data_source, sliders=list(all_sliders.values()), image_height=data.image_height, image_width=data.image_width, per_row=data.per_row, rows=data.rows, images=data.images_length), code="""
		source_data = source["data"]
		updateSliderValue(cb_obj.attributes.title, cb_obj.attributes.value)

		// subtraction function where we subtract a value from an array
		const subtract = function(array, value) {return array.map( array_at_i => array_at_i -value)}

		// slider array values
		//console.log(sliders);
		const active_sliders = sliders.filter(slider => slider["attributes"]["visible"]);
		const slider_array = active_sliders.map(slider => slider['properties']['value']['spec']['value'] );
		// slider array names
		const slider_idx_to_name = active_sliders.map(slider => slider['attributes']['title']);

		// source data for all images
		const source_vectors = slider_idx_to_name.map(name => source_data[name]);

		// for each row of features subtract the slider value
		const subtracted_feature_matrix = source_vectors.map(function(v, i) { return subtract(v,  slider_array[i])});

		var scores = new Array(images)
		for (i = 0; i < images; i++) {
			scores[i] = Math.abs(subtracted_feature_matrix.map(value => value[i]).reduce((a,b) => a+b, 0))
		} 

		indexedScores = scores.map(function(e,i){return {ind: i, val: e}});
		// sort index/value couples, based on values
		indexedScores.sort(function(x, y){return x.val > y.val ? 1 : x.val == y.val ? 0 : -1});
		// make list keeping only indices
		const rank = indexedScores.map(function(e){return e.ind + 1});

		source["data"]['rank'] = rank 
		source["data"]["x1"] = rank

		const x_range = per_row * image_width
		const y_range = images / per_row * image_height

		source["data"]['x1'] = source["data"]['rank'].map(value => (value - 1) % per_row)
		source["data"]['y1'] = source["data"]['rank'].map(value => y_range - Math.floor((value - 1) / per_row))
		source["data"]['x2'] = source["data"]['rank'].map(value => (value - 1) % per_row + image_width) 
		source["data"]['y2'] = source["data"]['rank'].map(value => y_range - Math.floor((value - 1) / per_row) - image_height) 
		
		source.change.emit()
	"""	)

	for slider in all_sliders.values():
		slider.js_on_change('value', callback)


	#Grid of checkbox buttons. Had to be before callback to make it work.
	cb_grid = column([cb_geography, cb_reality, cb_humanfactor, cb_domains, cb_goals, cb_means, cb_myapproach, cb_contenttome])
	cb_grid.visible = False

	#list of buttons and checkbox for for-loop callback
	button_col = [btn_geography, btn_reality, btn_humanfactor, btn_domains, btn_goals, btn_means, btn_myapproach, btn_contenttome]
	cb_col = [cb_geography, cb_reality, cb_humanfactor, cb_domains, cb_goals, cb_means, cb_myapproach, cb_contenttome]

	#Callback Javascript code for buttons
	code_button = """
		grid.visible=true;
		cb_geography.visible=false;
		cb_reality.visible=false;
		cb_humanfactor.visible=false;
		cb_domains.visible=false;
		cb_goals.visible=false;
		cb_means.visible=false;
		cb_myapproach.visible=false;
		cb_contenttome.visible=false;
		cb.visible=true;
		"""

	code_cb = """
		const label = cb_obj.active.map(i=>cb_obj.labels[i]);
		const values = cb_obj.labels.map(x => label.includes(x));

		updateVisible(cb_obj.labels, values);

		for(i=0;i<cb_obj.labels.length;i++) {
			if(label.includes(cb_obj.labels[i])) {
				slider[cb_obj.labels[i]].visible=true;
			}
			else {
				slider[cb_obj.labels[i]].visible=false;
			}
		}
	
	
		
		"""
	# ColumnDataSource(data.active
	# active_data = ColumnDataSource(data=data.active)
	
	for button, cb in zip(button_col, cb_col):
		button.js_on_click(CustomJS(args=dict(button=button,cb=cb,cb_reality=cb_reality,cb_geography=cb_geography,
											  cb_humanfactor=cb_humanfactor, cb_domains=cb_domains, cb_goals=cb_goals,
											  cb_means=cb_means, cb_myapproach=cb_myapproach, cb_contenttome=cb_contenttome,
											  grid=cb_grid), code=code_button))

	for cb in cb_col:
		cb.js_on_change("active", CustomJS(args=dict(slider=all_sliders), code=code_cb))


	# button_grid = column([btn_geography],[btn_reality],[btn_humanfactor],[btn_domains],[btn_goals], [btn_means], [btn_myapproach], [btn_contenttome])
	left_grid = column([btn_geography, btn_reality, btn_humanfactor, btn_domains, 
	btn_goals, btn_means, btn_myapproach, btn_contenttome, active_text, *all_sliders.values()])


	# button_grid = column([btn_geography],[btn_reality],[btn_humanfactor],[btn_domains],[btn_goals], [btn_means], [btn_myapproach], [btn_contenttome])
	#checkbox_grid = column([cb_reality]
	button_grid = column([btn_geography, btn_reality, btn_humanfactor, btn_domains, btn_goals, btn_means, btn_myapproach, btn_contenttome])

	slider_grid= column([active_text, *list(all_sliders.values())])
	# define the components: the javascript used and the div
	# grid = layout([[button_grid,p]])
	# page = row()
	left_grid = layout([[button_grid,cb_grid],[slider_grid]])
	right_grid = layout([[p]])

	total_grid = row([left_grid, right_grid])


	# l_script, l_div = components(left_grid)
	# r_script, r_div = components(right_grid)

	script, div = components(total_grid)

	return render_template('home.html', r_script=script, r_div=div)
	# return render_template('view3.html', title='Welcome!')

@main.route("/view2/<image_name>", methods = ['GET', 'POST'])
def view2(image_name):
	df = data.df
	
	image_data_row = df[df['name']==image_name]

	#Greate figure
	p = figure(x_range=(0,10), y_range=(0,10), plot_width=20, plot_height=20,toolbar_location=None)
	p.image_url(url=image_data_row['urls'], x=2.5, y=8, w=5, h=5)

	#Remove grid and axis
	p.xgrid.visible = False
	p.ygrid.visible = False
	p.axis.visible = False
	p.xgrid.grid_line_color = None

	# right square
	# r_square = figure(plot_width=500, plot_height=500,toolbar_location=None, tools="")
	# # r_square.square(x=[1], y=[2], size=[300], color="#74ADD1")
	# r_square.rect([0.6], [0.6], [0.3], [0.3], color="#74ADD1")
	# r_square.axis.visible = False
	# r_square.xgrid.grid_line_color = None

	active_text = PreText(text="Active Filters",width=200, height=40)

	btn_geography = Button(label="Geography", button_type="primary", width=150 )
	btn_reality = Button(label="Reality", button_type="danger", width=150)
	btn_humanfactor = Button(label="Human Factor", button_type="warning", width=150)
	btn_domains = Button(label="Domains", button_type="success", width=150)
	btn_goals = Button(label="Goals", button_type="success", width=150)
	btn_means = Button(label="Means", button_type="warning", width=150)
	btn_myapproach = Button(label="My Approach", button_type="danger", width=150)
	btn_contenttome = Button(label="Content To Me", button_type="primary", width=150)


	def get_active(column):
		return [index for index, value in  enumerate(column) if data.active[value][0]]

	cb_reality = CheckboxGroup(labels=list(data.reality_data.columns), active=get_active(data.reality_data.columns))
	cb_geography = CheckboxGroup(labels=list(data.geography_data.columns), active=get_active(data.geography_data.columns))
	cb_humanfactor = CheckboxGroup(labels=list(data.human_factor_data.columns), active=get_active(data.human_factor_data.columns))
	cb_domains = CheckboxGroup(labels=list(data.domains_data.columns), active=get_active(data.domains_data.columns))
	cb_goals = CheckboxGroup(labels=list(data.goals_data.columns), active=get_active(data.goals_data.columns))
	cb_means = CheckboxGroup(labels=list(data.means_data.columns), active=get_active(data.means_data.columns))
	cb_myapproach = CheckboxGroup(labels=list(data.my_approach_data.columns), active=get_active(data.my_approach_data.columns))
	cb_contenttome = CheckboxGroup(labels=list(data.content_to_me_data.columns), active=get_active(data.content_to_me_data.columns))

	cb_col = [cb_geography, cb_reality, cb_humanfactor, cb_domains, cb_goals, cb_means, cb_myapproach, cb_contenttome]


	cb_grid = column([cb_geography, cb_reality, cb_humanfactor, cb_domains, cb_goals, cb_means, cb_myapproach, cb_contenttome])
	cb_grid.visible = False

	#list of buttons and checkbox for for-loop callback
	button_col = [btn_geography, btn_reality, btn_humanfactor, btn_domains, btn_goals, btn_means, btn_myapproach, btn_contenttome]
	cb_col = [cb_geography, cb_reality, cb_humanfactor, cb_domains, cb_goals, cb_means, cb_myapproach, cb_contenttome]

	#Callback Javascript code for buttons
	code_button = """
		grid.visible=true;
		cb_geography.visible=false;
		cb_reality.visible=false;
		cb_humanfactor.visible=false;
		cb_domains.visible=false;
		cb_goals.visible=false;
		cb_means.visible=false;
		cb_myapproach.visible=false;
		cb_contenttome.visible=false;
		cb.visible=true;
		"""

	code_cb = """

		const label = cb_obj.active.map(i=>cb_obj.labels[i]);
		const values = cb_obj.labels.map(x => label.includes(x));

		updateVisible(cb_obj.labels, values);

		for(i=0;i<cb_obj.labels.length;i++) {
			if(label.includes(cb_obj.labels[i])) {
				slider[cb_obj.labels[i]].visible=true;
			}
			else {
				slider[cb_obj.labels[i]].visible=false;
			}
		}
	
		
		"""
	# ColumnDataSource(data.active
	# active_data = ColumnDataSource(data=data.active)
	
	for button, cb in zip(button_col, cb_col):
		button.js_on_click(CustomJS(args=dict(button=button,cb=cb,cb_reality=cb_reality,cb_geography=cb_geography,
											  cb_humanfactor=cb_humanfactor, cb_domains=cb_domains, cb_goals=cb_goals,
											  cb_means=cb_means, cb_myapproach=cb_myapproach, cb_contenttome=cb_contenttome,
											  grid=cb_grid), code=code_button))
	#Dictionary for all the sliders
	all_sliders = {}
	
	# Create all sliders and set them to invisible
	for index in data.slider_index_total:
		for sliders in index:
			all_sliders[sliders] = Slider(title=sliders, value=float(image_data_row.iloc[0][sliders]), start=0, end=1, step=0.01)
			all_sliders[sliders].visible = data.active[sliders][0] 

	for cb in cb_col:
		cb.js_on_change("active", CustomJS(args=dict(slider=all_sliders), code=code_cb))
	

	callback = CustomJS(args=dict(image_name=image_data_row['name']), code="""
		updateDataframe(image_name, cb_obj.attributes.title, cb_obj.attributes.value)
	""")

	for slider in list(all_sliders.values()):
		slider.js_on_change('value', callback)


	right_grid = column([btn_geography, btn_reality, btn_humanfactor, btn_domains, 
	btn_goals, btn_means, btn_myapproach, btn_contenttome, active_text, *all_sliders.values()])


	button_grid = column([btn_geography, btn_reality, btn_humanfactor, btn_domains, btn_goals, btn_means, btn_myapproach, btn_contenttome])

	slider_grid= column([active_text, *list(all_sliders.values())])
	right_grid = layout([[button_grid,cb_grid],[slider_grid]])

	slider_grid= column([active_text, *all_sliders.values()])
	# define the components: the javascript used and the div

	grid = gridplot([[p, right_grid]], plot_width=600, plot_height=600, toolbar_location = None, sizing_mode='scale_both')

	# define the components: the javascript used and the div
	l_square_script, l_square_div = components(grid)
	
	return render_template('view2.html', images=data.images, data=data, l_square_script=l_square_script, l_square_div=l_square_div)

@main.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(main.root_path, 'static'),
										'favicon.ico', mimetype='image/vnd.microsoft.icon')

