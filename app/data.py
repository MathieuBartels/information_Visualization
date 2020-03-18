import pandas as pd
import os
from app import image_plotting
from bokeh.models import ColumnDataSource, Slider
import numpy as np
import math
from scipy.spatial.distance import euclidean

from numpy import dot
from numpy.linalg import norm




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
df['rank'] = df['simrank'] = range(1, images_length+1)
df['newrank'] = df['rank']
df['score'] = df['rank']
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

# Get all slider titles in same array
slider_index_total = [geography_data.columns, reality_data.columns, human_factor_data.columns, domains_data.columns,goals_data.columns, means_data.columns,my_approach_data.columns, content_to_me_data.columns]

active = {}
active_list = ['Control']
for index in slider_index_total:
    for sliders in index:    
        active[sliders] = [False, 0]
        if sliders is 'Control':
            active[sliders] = [True, 0.3]

all_index_names = list(active.keys())

def update_active(names, values):
    print("update active")
    for name, value in zip(names, values):
        if value:
            active[name][0] = True
            if not name in active_list:
                active_list.append(name)
        else:
            active[name] = [False, 0]
            if name in active_list:
                active_list.remove(name)
    return active

def cosine(a,b):
    denom = norm(a)*norm(b)
    if denom == 0:
        return 0
    else:
        return (a @ b.T)/denom

def similarity(a, b):
    return euclidean(a,b)


def update_slider_value(slider, value):
    print("update active")
    active[slider][1] = value

    slider_values = np.array([active[slider][1] for slider in active_list])


    df['score'] = df[active_list].apply(lambda x: similarity(x, slider_values), raw=True, axis=1)
    df.replace(np.nan, 0, regex=True)
    for rank, row in enumerate(np.argsort(df['score'])):
        df['rank'].iloc[row] = rank

    return df['rank']

def update_active_view2(names, values):
    print("update active")
    for name, value in zip(names, values):
        if value:
            active[name][0] = True
        else:
            active[name] = [False, 0]
    return active


def update_slider_value_view2(slider, value, image_name):
    print("update active")
    image_data = df[df['name'] == image_name[0]]
    image_values = image_data[all_index_names].to_numpy()

    if not len(active_list) == 0:
        slider_values = np.array([active[slider][1] for slider in active_list])

        df.loc[df['name']==image_name[0], 'score'] = image_data[active_list].apply(lambda x: similarity(x, slider_values), raw=True, axis=1)
        df.loc[df['name']==image_name[0], 'newrank'] = list(np.argsort(df['score'])).index(image_data.index[0])

    df['simscore'] = df[all_index_names].apply(lambda x: similarity(x, image_values), raw=True, axis=1)
    df.replace(np.nan, 0, regex=True)
    for rank, row in enumerate(np.argsort(df['simscore'])):
        df['simrank'].iloc[row] = rank -1

    return df['simrank']

def update_data(row, column, new_value):
    df.loc[df['name']==row, column] = float(new_value)
    return df


