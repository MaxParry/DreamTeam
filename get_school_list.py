# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 10:59:18 2018

@author: Rayzel
"""

import requests
import json
import numpy as np
import pandas as pd

def findPlace(lat, lng, place_type, keyword):
  gkey = "AIzaSyCjKv0xK2wFVM8DFe9C7frIrtU6kh7kOwA"
  target_radius = 1609
  target_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
               "?location=%s,%s&radius=%s&types=%s&key=%s&keyword=%s" % (
                 lat, lng, target_radius,
                 place_type, gkey, keyword)
  places_data = requests.get(target_url).json()
  return places_data["results"]

def placeRating(placeid):
  gkey = "AIzaSyA_Clyz3478YAUnsESNHE5dyktvvMoa-vw"
  target_url = "https://maps.googleapis.com/maps/api/place/details/json" \
               "?placeid=%s&key=%s" % (
                 placeid, gkey)
  places_data = requests.get(target_url).json()
  return places_data["result"]

grid_data = pd.read_csv("unique_lat_lon.csv")


keyterm = "restaurant"
ratings = []
places = findPlace(47.51670804, -122.253, keyterm, "")
for place in places:
  try:  
    rating = placeRating(place["place_id"])["rating"]
    ratings.append(rating)
    #print(place["name"], ":", rating)
  except KeyError:
    pass

print("number of", keyterm, "around:", len(places))   
print("average rating:", np.average(ratings))