# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 01:37:51 2022

@author: samgo
"""

from stationdistances import *
from anytimefarefinder import *

import folium
import numpy as np
#from folium.plugins import HeatMap

# Definitions
save_fares_path = "saved_fares.csv"

file = 'table-1410-passenger-entries-and-exits-and-interchanges-by-station.csv'
#location = (51.5216848296857, -0.13785953967373285) # Arup 8FS.
#location = (54.774895878125825, -1.574515102594818) # Hatfield
location = (51.45024102401295, -2.588027316824446) # Arup Bristol
n_stations = 20

# Finding closest n stations to coords
station_data = get_station_distances(file, location)
sd_sorted = station_data.sort_values('Distance')
closest_stations = sd_sorted[0:n_stations+1]
target = closest_stations[:1]
target = target.reset_index()
closest_stations = closest_stations[1:]
closest_stations = closest_stations.reset_index()
closest_stations['Fares'] = -1
for n in range(len(closest_stations)):
    closest_stations['Fares'][n] = get_anytime_fare(closest_stations['TLC'][n],target['TLC'][0],save_fares_path)

# Mapping
for_map = closest_stations

# Working out colour gradient

min_fare = min(for_map['Fares'].values)
max_fare = max(for_map['Fares'].values)
min_colour = 25
max_colour = 255

diff = max_fare - min_fare

colours = np.round((((for_map['Fares'].values-min_fare)/diff) * (max_colour-min_colour)) + min_colour,).astype(int)


m = folium.Map(location, zoom_start=8)

for n in range(len(for_map)):
    folium.Circle(
        location=[for_map['Latitude'].values[n],for_map['Longitude'].values[n]],
        radius=1610, #1mile
        popup=for_map['Station name'].values[n]+" - "+for_map['Fares'].values[n].astype(str),
        color="#"+np.base_repr(colours[n],16)+"0000",
        fill=True,
        fill_color="#"+np.base_repr(colours[n],16)+"0000",
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
