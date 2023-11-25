#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import json
import regex as re
from googlemaps import Client as GoogleMaps
import googlemaps
import numpy as np


# Use CMS Dataset Versions UUID and not Dataset Type Identifier 
cms_data_version="7a101036-1595-443f-84b8-6bffca1786b8"
resp = requests.get(f"https://data.cms.gov/data-api/v1/dataset/{cms_data_version}/data")


headers = {
    'accept': 'application/json',
}

y=0
dflist=[]
size1=5000 # determined by the data.cms.gov as max rows per call
rows=5000 # Check the data documentation to see the number of rows, this determines the number of loops to run below
looplength=1 + rows//size1

for x in range(looplength):
    offset1=y+x*size1
    #change params to ensure number of rows matches interest
    params = {
        'offset': offset1,
        'size': size1,
    }
    response = requests.get(f"https://data.cms.gov/data-api/v1/dataset/{cms_data_version}/data",
        params=params,
        headers=headers,
    )
    df=pd.read_json(json.dumps(response.json()))
    dflist.append(df)

fd = pd.concat(dflist)

gmaps = googlemaps.Client(key="xxxx")
fd=fd.reset_index(drop=True)
geolat=[]
geolong=[]
for z in range(len(fd)): 
    x1=re.split(r',|( ste)|( st)',  fd.loc[z,"ADDRESS LINE 1"].capitalize())[0]
    x2=fd.loc[z,"ADDRESS LINE 2"]
    x3=fd.loc[z,"CITY"].capitalize()
    x4=fd.loc[z,"STATE"]
    x5=fd.loc[z,"ZIP"][0:5]
    y=x1+","+x3+","+x4+","+x5+",US"
    fd.loc[z,"address"]=y
    try:
        xlat=gmaps.geocode(y)[0]['geometry']['location'] ['lat']
        xlon=gmaps.geocode(y)[0]['geometry']['location'] ['lng']
        geolat.append(xlat)
        geolong.append(xlon)
    except:
        xlat=np.nan
        xlon=np.nan
        geolat.append(np.nan)
        geolong.append(np.nan)
    print(xlat)
    print(xlon)
fd['lat']=geolat
fd['lon']=geolong
fd=fd.dropna()
fd
fd=fd.reset_index()
fd.to_csv("D:\Data\OpTreat\oct_data.csv")

