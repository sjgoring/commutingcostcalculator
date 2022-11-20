# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 00:46:28 2022

@author: samgo
"""
import pyproj
import pandas as pd

## Coords

def get_station_distances(file, location):
    # Gets every station's crow flies distance from the given lat long coords.
    # Uses Gov data contained in file.
    
    lat_ref = location[0]
    long_ref = location[1] 
    
    crs_british = pyproj.Proj(init='EPSG:27700')
    crs_wgs84 = pyproj.Proj(init='EPSG:4326')
    
    g = pyproj.Geod(ellps='clrk66')
    
    data = pd.read_csv(file)
    
    data_reduce = data[['Station name', 'TLC', 'OS grid Easting','OS grid Northing']]
    data_reduce['Longitude'] = 1000.00
    data_reduce['Latitude'] = 1000.00
    data_reduce['Distance'] = -1.00
    
    for n in range(len(data)):
        long,lat = pyproj.transform(crs_british, crs_wgs84,data['OS grid Easting'][n],data['OS grid Northing'][n])
        data_reduce['Longitude'][n] = long
        data_reduce['Latitude'][n] = lat
        _,_,data_reduce['Distance'][n] = g.inv(long, lat, long_ref, lat_ref)
        #print(data_reduce['Distance'][n])
        #print(n)
    return data_reduce
    
# file = 'table-1410-passenger-entries-and-exits-and-interchanges-by-station.csv'
# location = (51.5216848296857, -0.13785953967373285) # Arup 8FS.
# #location = (54.774895878125825, -1.574515102594818) # Hatfield
# station_data = get_station_distances(file, location)
    
# sd_sorted = station_data.sort_values('Distance')
# n_stations = 50
# #top 51 (closest station is ref station for fares).
# closest_stations = sd_sorted[0:n_stations+1]
