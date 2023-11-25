#!/usr/bin/env python
# coding: utf-8

# In[44]:


import requests
import pandas as pd
import json
import regex as re
import geopandas
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="example app")
#import matplotlib.pyplot as plt
import numpy as np
import folium
from googlemaps import Client as GoogleMaps
import googlemaps


# In[45]:


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

full_data1 = pd.concat(dflist)
#print(full_data)
#print(full_data.columns)
#full_data=full_data.dropna()


# In[46]:


print(full_data1)


# In[47]:


full_data=pd.read_csv('/Users/manaskaushik/Documents/OpiodTreat/full_data.csv')


# In[48]:


fd=pd.merge(left=full_data1, right=full_data, left_on='NPI', right_on='NPI', how='outer')


# In[49]:


fd=fd[fd['lat'].isna()]
fd


# In[ ]:





# In[50]:


gmaps = googlemaps.Client(key=xxx)


    


# In[55]:


fd.columns


# In[51]:


fd=fd.reset_index(drop=True)
geolat=[]
geolong=[]
for z in range(len(fd)): 
    x1=re.split(r',|( ste)|( st)',  fd.loc[z,"ADDRESS LINE 1_x"].capitalize())[0]
    x2=fd.loc[z,"ADDRESS LINE 2_x"]
    x3=fd.loc[z,"CITY_x"].capitalize()
    x4=fd.loc[z,"STATE_x"]
    x5=fd.loc[z,"ZIP_x"][0:5]
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


# In[ ]:


fd=fd.rename({'PROVIDER NAME_x':'PROVIDER NAME', 'ADDRESS LINE 1_x':'ADDRESS LINE 1', 'ADDRESS LINE 2_x':'ADDRESS LINE 2',
       'CITY_x':'CITY', 'STATE_x':'STATE', 'ZIP_x':'ZIP_x', 'MEDICARE ID EFFECTIVE DATE_x': 'MEDICARE ID EFFECTIVE DATE', 'PHONE_x':'PHONE'})
fd=fd.drop(axis=1, 'PROVIDER NAME_y', 'ADDRESS LINE 1_y',
       'ADDRESS LINE 2_y', 'CITY_y', 'STATE_y', 'ZIP_y',
       'MEDICARE ID EFFECTIVE DATE_y', 'PHONE_y')


# In[53]:


fd['lat']=geolat
fd['lon']=geolong
print(fd['lat'])
fd.to_csv('/Users/manaskaushik/Documents/OpiodTreat/suppl.csv')


# In[54]:


print(fd)

