# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 09:45:35 2022

@author: samgo
"""

# Commuting location finder code
# Based on transport-cost-finder

# Imports
from stationdistances import *
from anytimefarefinder import *
from Housing import *
from statistics import median

import folium
import numpy as np
import csv
#from folium.plugins import HeatMap

# Definitions
save_fares_path = "saved_fares.csv"
save_loc_codes_path = "location_codes.csv"
radius = 1.0 #miles
beds = 2
days_in_office = 22*(2/5)

file = 'table-1410-passenger-entries-and-exits-and-interchanges-by-station.csv'
#location = (51.5216848296857, -0.13785953967373285) # Arup 8FS.
#location = (54.774895878125825, -1.574515102594818) # Hatfield
office = (51.45024102401295, -2.588027316824446) # Arup Bristol
n_stations = 20

# Finding closest n stations to coords
station_data = get_station_distances(file, location)
sd_sorted = station_data.sort_values('Distance')
closest_stations = sd_sorted[0:n_stations+1]
target = closest_stations[:1]
target = target.reset_index()
closest_stations = closest_stations[1:]
closest_stations = closest_stations.reset_index()

# Getting rightmove codes
# Todo replace with automated location code finder.
with open(save_loc_codes_path, 'r') as f:
        dict_reader = csv.DictReader(f)
        rm_codes = list(dict_reader)

# Get fares and rents
closest_stations['Fares'] = -1
closest_stations['Rent'] = -1
closest_stations['Combined'] = -1
for n in range(len(closest_stations)):
    closest_stations['Fares'][n] = get_anytime_fare(closest_stations['TLC'][n],target['TLC'][0],save_fares_path)
    rents = rental_price_scraper(rm_codes[n]['Rightmove'] , radius, beds)
    if len(rents) == 0:
        closest_stations['Rent'][n] = -2    
    else:
        closest_stations['Rent'][n] = median(rents)
        closest_stations['Combined'][n] = closest_stations['Rent'][n] +  days_in_office*closest_stations['Fares'][n]


# Mapping
for_map = closest_stations

# Working out colour gradient

min_fare = min(for_map['Combined'].values)
max_fare = max(for_map['Combined'].values)
min_colour = 25
max_colour = 255

diff = max_fare - min_fare

colours = np.round((((for_map['Combined'].values-min_fare)/diff) * (max_colour-min_colour)) + min_colour,).astype(int)


m = folium.Map(office, zoom_start=8)

for n in range(len(for_map)):
    c = "#"+np.base_repr(colours[n],16)+"0000"
    print(for_map['Combined'].values[n])
    if for_map['Combined'].values[n] == -1:
        print("Green")
        c = "#00FF00"
        # no housing available
    folium.Circle(
        location=[for_map['Latitude'].values[n],for_map['Longitude'].values[n]],
        radius=1610, #1mile
        popup=for_map['Station name'].values[n]+", Train: "+(days_in_office*for_map['Fares'].values[n]/100).astype(str) + ", Rent: "+(for_map['Rent'].values[n]/100).astype(str) + ", Total: "+(for_map['Combined'].values[n]/100).astype(str),
        color=c,
        fill=True,
        fill_color=c,
    ).add_to(m)

m.save("map.html")

# hm_wide = HeatMap(
#     list(np.transpose(np.array((for_map['Latitude'].values, for_map['Longitude'].values, for_map['Fares'].values)))),
#     min_opacity=0.2,
#     radius=17, 
#     blur=15, 
#     max_zoom=1,
# )

# hmap.add_child(hm_wide)
# hmap.save("map.html")
