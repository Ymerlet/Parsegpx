# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 15:07:15 2017

@author: merlety

Parser un gpx, parser une list de WP OSM et dans le futur garder ceux qui sont
proches et les ajouter au gpx en tant que WP
"""

    
import gpxpy
import gpxpy.gpx
from math import radians, cos, sin, asin, sqrt
import json
import pandas as pd
import numpy as np

def distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
    
def jsonparser(file):
    """
    Parse a json file from OSM overpass and returns a dataframe with all
    the data of the waypoints    
    """
    with open(file) as data_file:
        data=json.load(data_file)
    
    data = data["elements"]
    
    waypoints = pd.io.json.json_normalize(data)
    
    return waypoints

def gpxparser(file):
    """
    Parse a GPX file and returns a dataframe with latitude, longitude and
    elevation with column lat, lon and ele
    """
    with open(file) as gpxfile:
        gpx = gpxpy.parse(gpxfile)
        
    lat = []
    lon = []
    ele = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
                ele.append(point.elevation)
    
    trkpt=list(zip(*[lat,lon,ele]))

    gpx_track = pd.DataFrame(trkpt,columns=['lat','lon','ele'])
    
    return gpx_track

def far_away(waypoint,waypoint_close):
    """
    test the distance between a waypoint and track is less than 10k
    """
    for j in len(gpx.index):
        if distance(waypoint['lon'],waypoint['lat'],gpx['lon'][j],gpx['lat'][j]) < 10:
            return True
        
if __name__ == '__main__':   
    path='D:/Desktop'
    name='Velotaf_aller.gpx'
    file=path+'/'+name
    
#    json='camping.json'
#    json_file=path+'/'+json
    
    gpx_file = open('./archies_europe-f.gpx','r', encoding='latin-1')

    waypoint = gpxpy.parse(gpx_file)
     
    gpx = gpxparser(file)
#    waypoint=jsonparser(json_file)
    
    
    
    waypoint_close=pd.DataFrame(columns=waypoint.columns.values.tolist())
    
    for i in len(waypoint.index) :
        if far_away(waypoint.iloc[i],gpx) == True:
            waypoint_close.append(waypoint.iloc)
    
    wpgpx = gpxpy.gpx.GPX()
    
    for Pt in waypoint_close:
            wpgpx.waypoints.append(gpxpy.gpx.GPXWaypoint(
            Pt.lat, Pt.lon, elevation=Pt.ele))
    
    with open('output.gpx', 'w') as f:
            f.write(gpx.to_xml())
        

