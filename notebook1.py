#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import folium
import streamlit as st
from streamlit_folium import st_folium
#full_data=pd.read_csv('/Users/manaskaushik/Documents/OpiodTreat/full_data.csv')

full_data=pd.read_csv('https://raw.githubusercontent.com/mangospace/OpTreat/main/oct_data.csv')
full_data.reset_index(drop=True)

statelist=full_data['STATE'].tolist()

st.title('Opiod Treatment Centers')
st.caption("Oct 2023")
st.caption('Made by @manas8u')
st.caption('Please share your feedback and suggestions. DM @manas8u')

"""
option1 = st.selectbox(
    'Which state would you like to explore in detail?',
    (statelist))

m = folium.Map(location=[48, -102], zoom_start=3)
for x in range(len(full_data)):
    folium.Marker(
        location=[full_data.loc[x,'lat'],full_data.loc[x,'lon']],
        tooltip=full_data.loc[x,'CITY'],
        popup=full_data.loc[x,'PROVIDER NAME'],
        icon=folium.Icon(color="green"),
    ).add_to(m)
m
#st_data = st_folium(m, width=725)
"""
option1="AL"
state_data=pd.read_csv('https://raw.githubusercontent.com/mangospace/OpTreat/main/state_center.csv')
state_data=state_data[state_data["STATE"]==option1]
state_data=state_data.reset_index(drop=True)
state_data

long=state_data.loc[0,'lon']
latt=state_data.loc[0,'lat']

full_data1=full_data[full_data['STATE']==option1]
full_data1=full_data1.reset_index(drop=True)
full_data1
#m = folium.Map(location=[long, latt], zoom_start=4)
m = folium.Map(location=[32, -86], zoom_start=6)
for x in range(len(full_data1)):
    folium.Marker(
        location=[full_data1.loc[x,'lat'],full_data1.loc[x,'lon']],
        tooltip=full_data1.loc[x,'CITY'],
        popup=full_data1.loc[x,'PROVIDER NAME'],
        icon=folium.Icon(color="green"),
    ).add_to(m)
m
#st_data = st_folium(m, width=725)
