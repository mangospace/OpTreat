import requests
import pandas as pd
import json
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

full_data = pd.concat(dflist)
print(full_data)
print(full_data.columns)

x1=full_data.loc[2,"ADDRESS LINE 1"]
x2=full_data.loc[2,"ADDRESS LINE 2"]
x3=full_data.loc[2,"CITY"]
x4=full_data.loc[2,"STATE"]
x5=full_data.loc[2,"ZIP"]

print(f"{x1=} {x2=} , {x3=} {x4=}")
#for x in range(len(full_data)):
#    full_data.loc[x,"PROVIDER NAME"])
y=x1+","+x3+","+x4+","+x5+",USA"
print(y)    
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="example app")
#print(geolocator.geocode("Tuscany, Italy").raw)
print(geolocator.geocode("5715 PRINCESS ANNE RD,VIRGINIA BEACH,VA,23462-3222,USA"))