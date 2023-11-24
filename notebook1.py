#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import json
import regex as re
import numpy as np
import folium
import streamlit as st
from streamlit.web import cli as stcli
from streamlit_folium import st_folium
#full_data=pd.read_csv('/Users/manaskaushik/Documents/OpiodTreat/full_data.csv')

full_data=pd.read_csv('https://raw.githubusercontent.com/mangospace/OpTreat/main/full_data.csv')
full_data=full_data.dropna()
full_data=full_data.reset_index(drop=True)
statelist=full_data['STATE'].tolist()

st.title('Opiod Treatment Centers')
st.caption("Oct 2023")
st.caption('Made with \u2764\uFE0F @manas8u in Python and Streamlit')
st.caption('Please share your feedback and suggestions. DM @manas8u')

#option1 = st.selectbox(
#    'Which state would you like to explore in detail?',
#    (statelist))

m = folium.Map(location=[48, -102], zoom_start=3)
for x in range(len(full_data)):
    folium.Marker(
        location=[full_data.loc[x,'lat'],full_data.loc[x,'lon']],
        tooltip=full_data.loc[x,'CITY'],
        popup=full_data.loc[x,'PROVIDER NAME'],
        icon=folium.Icon(color="green"),
    ).add_to(m)
m
st_data = st_folium(m, width=725)
