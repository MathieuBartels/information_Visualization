from bokeh.plotting import figure, show, output_file
import numpy as np

def plot_images():
    # Plotting multiple images

    output_file('image.html')

    #naming images
    url01 = "app/data/230_works_1024x/13aeroplanes_1998.jpg"
    url02 = "app/data/230_works_1024x/Access_2007.jpg"
    url03 = "app/data/230_works_1024x/Annex_2003.jpg"

    #Used to set spacing of images in grid
    N = 3
    xr = 100
    yr = 100
    x1 = np.linspace(0, 100, N+1)

    #Greate figure
    p = figure(x_range=(0,xr), y_range=(0,yr))
    p.image_url(url=[url01], x=x1[0], y=yr, w=xr/N, h=yr/N)
    p.image_url(url=[url02], x=x1[1], y=yr, w=xr/N, h=yr/N)
    p.image_url(url=[url03], x=x1[2], y=yr, w=xr/N, h=yr/N)

    #Remove grid and axis
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.xaxis.visible = False
    p.yaxis.visible = False


    show(p)