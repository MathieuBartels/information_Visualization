from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

plot = figure()
plot.circle([1,2], [3,4])

html = file_html(plot, CDN, "my_plot")

# from bokeh.plotting import figure, ColumnDataSource
# from bokeh.layouts import row, column, widgetbox
# from bokeh.models import HoverTool, Slider, CustomJS, PointDrawTool
# from bokeh.embed import json_item
# from app import data
# from bokeh.events import Tap

# from bokeh.plotting import figure, show, output_file
# from bokeh.plotting import figure, curdoc
# from bokeh.models import ColumnDataSource, Range1d

# def show_img(div_name="myplot"):
#     output_file('view2.html')
#     logo_src = ColumnDataSource(dict(url = ["https://images.pexels.com/photos/736230/pexels-photo-736230.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"]))
#     page_logo = figure(plot_width = 500, plot_height = 500, title="ed")
    # page_logo.toolbar.logo = None
    # page_logo.toolbar_location = None
    # page_logo.x_range=Range1d(start=0, end=1)
    # page_logo.y_range=Range1d(start=0, end=1)
    # page_logo.xaxis.visible = None
    # page_logo.yaxis.visible = None
    # page_logo.xgrid.grid_line_color = None
    # page_logo.ygrid.grid_line_color = None
    # page_logo.image_url(url='url', x=0.05, y = 0.85, h=0.7, w=0.9, source=logo_src)
    # page_logo.outline_line_alpha = 0 
	# curdoc().add_root(page_logo)
    # layout = row(
	# 	page_logo,
	# 	width=850
	# )
    # plot_json = json_item(layout, div_name)
    # return plot_json
