import pandas as pd
import os
from app import image_plotting
from bokeh.models import ColumnDataSource

df = pd.read_csv("app/data/NOWHERE_DATASET.csv") 
header = df.iloc[2]
df = pd.DataFrame(df.values[4:], columns=header)
df.rename(columns={'1= very related': 'name'}, inplace=True)
df.columns.values[1] = "year"	
df.fillna(0, inplace=True)
df.sort_values(by=['name'], inplace=True)

image_amount = len(df)
df['rank'] = range(1, image_amount+1)

#Get urls of the images and add to the dataframe
images = os.listdir('app/static/230_works_1024x')
images = images[0:image_amount]
urls = [f'/static/230_works_1024x/{image}' for image in images]
df['urls'] = urls

#Plot formatting
image_height = 1
image_width = 1
per_row = 5
rows = image_amount/5
x_range = per_row * image_width
y_range = image_amount / per_row * image_height

#Add columns to the dataframe for the placing and formatting
df['w'] = [image_width] * image_amount
df['h'] = [image_height] * image_amount
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

human_factor_sources = ColumnDataSource(data=human_factor_data)
geography_sources = ColumnDataSource(data=geography_data)
reality_sources = ColumnDataSource(data=reality_data)
domains_sources = ColumnDataSource(data=domains_data)
goals_sources = ColumnDataSource(data=goals_data)
means_sources = ColumnDataSource(data=means_data)
my_approach_sources = ColumnDataSource(data=my_approach_data)
content_to_me_sources = ColumnDataSource(data=content_to_me_data)

def update_data(row, column, new_value):
    df.loc[row, column] = new_value
    return df


