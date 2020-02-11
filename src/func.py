import math
from pymongo import MongoClient
import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()
from shapely.geometry import Point

def asGeoJSON(lat,lng): 
    try:
        lat = float(lat)
        lng = float(lng)
        if not math.isnan(lat) and not math.isnan(lng):
            return {
                "type":"Point",
                "coordinates":[lng,lat]
            }
    except Exception:
        print("Invalid data")
        return None

def withGeoQuery(location,maxDistance=10000,minDistance=0,field="location"):
    return {
       field: {
         "$near": {
           "$geometry": location if type(location)==dict else geocode(location),
           "$maxDistance": maxDistance,
           "$minDistance": minDistance
         }
       }
    }

def geocode(address):
    data = requests.get(f"https://geocode.xyz/{address}?json=1").json()
    return {
        "type":"Point",
        "coordinates":[float(data["longt"]),float(data["latt"])]
    }

def geoDataFrame(df):
    geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    crs = {"init": "epsg:4326"}
    gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
    return gdf

def starbucks250m(val):
    API_key = os.getenv('API_KEY')
    lat = val["coordinates"][1]
    lon = val["coordinates"][0]
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    endpoint = "query=starbucks&location={0},{1}&radius=250&key={2}".format(lat, lon, API_key)
    res = requests.get(base_url+endpoint).json()
    number = len(res["results"])
    return number

def design():
    API_key = os.getenv('API_KEY')
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    endpoint = "query=design+agency+in+london&key={}".format(API_key)
    res = requests.get(base_url+endpoint).json()
    return res