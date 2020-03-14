import pandas as pd
import os
from app import image_plotting
from bokeh.models import ColumnDataSource, Slider
import numpy as np
import math

df = pd.read_csv("app/data/NOWHERE_DATASET.csv") 
header = df.iloc[2]
df = pd.DataFrame(df.values[4:], columns=header)
df.rename(columns={'1= very related': 'name'}, inplace=True)
df.columns.values[1] = "year"	
df["year"] = df["year"].astype('int32')
df.sort_values(by=['name'], inplace=True)


for name in df:
    if name not in ['year', 'name']:
        df[name] = pd.to_numeric(df[name], errors='coerce')
        
df = df.replace(np.nan, 0, regex=True)

#Get urls of the images and add to the dataframe
images = os.listdir('app/static/230_works_1024x')
images = images[0:len(df)]

urls = [f"/static/230_works_1024x/{name.replace(' ', '_')}_{year}.jpg" for (name, year) in zip(df['name'], df['year'])]
df['urls'] = urls

# print(urls)

df = df[[os.path.exists(f"app/static/230_works_1024x/{name.replace(' ', '_')}_{year}.jpg") for (name, year) in zip(df['name'], df['year'])]]
images_length = len(df)
df['rank'] = range(1, images_length+1)

#Plot formatting
image_height = 1
image_width = 1
per_row = 5
rows = math.ceil(images_length/5)
x_range = per_row * image_width
y_range = images_length / per_row * image_height

#Add columns to the dataframe for the placing and formatting
df['w'] = [image_width] * images_length
df['h'] = [image_height] * images_length
df['x1'] = (df['rank'] - 1) % per_row
df['y1'] = y_range - (df['rank'] - 1) // per_row
df['x2'] = (df['rank'] - 1) % per_row + image_width
df['y2'] = y_range - (df['rank'] - 1) // per_row - image_height

human_factor_data = df[['Politics', 'Corporate', 'Private', 'Public', 'Interaction']]
geography_data =df[['Europe', 'Nrth America', 'Middle East', 'Asia', 'Sth America']]
reality_data = df[['Void', 'Non-place', 'Space', 'Nature', 'Development', 'Suburbia', 'Urbanisation', 'Sprawl', 'One Building', 'Part of a building', 'City Center', 'Grid/Order', 'Interior', 'Poster', 'Screen', 'Facade', 'Geographically Specific', 'Public Space', 'Private Space', 'Model', 'Plan']]
domains_data = df[['Advertising / Promotion', 'Philosophy', 'Sociology', 'Communication', 'Urbanity', 'Science', 'Entertainment / Leisure', 'Industry', 'Information', 'Art', 'Architecture', 'Design', 'Public Service', 'Transportation', 'Nature']]
goals_data = df[['Control', 'Power', 'Consuming', 'Knowledge', 'Information', 'Surveillance', 'Security', 'Money Wealth', 'Change', 'Progress', 'Community', 'Empowerment', 'Decoration', 'Escape', 'Symbolism', 'Globalisation', 'Mobility', 'Visibility', 'Fun']]
means_data = df[['Confrontation', 'Exaggaration', 'Exclusivity', 'Conditioning', 'Repetition', 'Experimentation', 'Celebration', 'Chaos', 'Presence', 'Selection', 'Isolation', 'Manipulation', 'Persuasion', 'Promise', 'Coöperation', 'Variety', 'Improvisation', 'Destruction', 'Reconstruction', 'Simplification', 'Planning', 'Constrainment', 'System']]
my_approach_data = df[['About the medium', 'Documentary', 'Abstraction', 'Framing', 'Scaling', 'Reflection', 'Symmetry', 'Repeating elements', 'Composite', 'Front facing', 'Angle', 'Looking Up', 'Bird Eye View', 'Importance of Detail', 'Blur', 'Video', 'Long Exposure', 'Loop', 'Time Lapse', 'Crossover', 'Layers', 'Photoshop', 'Archetype', 'Metaphor', 'Location focus']] 
content_to_me_data = df[['Desire', 'Greed', 'Competition', 'Illusion', 'Attraction / Play', 'Memory', 'Solution', 'Contemplation', 'Images Rule', 'Movie references', 'Game references', 'Future Orientation', 'Ambition', 'Tradition', '24/7', 'Digitalisation', 'Degradation', 'Loneliness', 'Anonimity', 'Inhabitation', 'Individuality', 'Identity', 'Austerity', 'Limitation', 'Convention', 'Struggle', 'Interference', 'Substitution', 'Alienation', 'Space & Time', 'Pretention', 'Addiction', 'Belief/disbelief', 'High/Kick']] 

# human_factor_sources = ColumnDataSource(data=human_factor_data)
# geography_sources = ColumnDataSource(data=geography_data)
# reality_sources = ColumnDataSource(data=reality_data)
# domains_sources = ColumnDataSource(data=domains_data)
# goals_sources = ColumnDataSource(data=goals_data)
# means_sources = ColumnDataSource(data=means_data)
# my_approach_sources = ColumnDataSource(data=my_approach_data)
# content_to_me_sources = ColumnDataSource(data=content_to_me_data)

# Get all slider titles in same array
slider_index_total = [geography_data.columns, reality_data.columns, human_factor_data.columns, domains_data.columns,goals_data.columns, means_data.columns,my_approach_data.columns, content_to_me_data.columns]

active = {}
for index in slider_index_total:
    for sliders in index:
        active[sliders] = [False, 0]

def update_active(actives):
    print("update active")
    for index in slider_index_total:
        for sliders in index:
            active[sliders] = [False, 0]

    for slider in actives:
        active[slider][0] = True
    return active


def update_slider_value(slider, value):
    print("update active")
    active[slider][1] = value
    return active


# #Dictionary for all the sliders
# all_sliders = {}

# # Get all slider titles in same array
# slider_index_total = [geography_data.columns, reality_data.columns, human_factor_data.columns, domains_data.columns,goals_data.columns, means_data.columns,my_approach_data.columns, content_to_me_data.columns]

# # Create all sliders and set them to invisible
# for index in slider_index_total:
#     for sliders in index:
#         all_sliders[sliders] = Slider(title=sliders, value=0, start=0, end=1, step=0.01)
#         all_sliders[sliders].visible = False

def update_data(row, column, new_value):
    df.loc[df['name']==row, column] = float(new_value)
    return df


