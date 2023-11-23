#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import json
import regex as re
#import matplotlib.pyplot as plt
import numpy as np
import folium
import streamlist as st

full_data=pd.read_csv('/Users/manaskaushik/Documents/OpiodTreat/full_data.csv')

m = folium.Map(location=[48, -102], zoom_start=3)
for x in range(len(full_data)):
    folium.Marker(
        location=[full_data.loc[x,'lat'],full_data.loc[x,'lon']],
        tooltip="Op Treat!",
        popup=full_data.loc[x,'PROVIDER NAME'],
        icon=folium.Icon(color="green"),
    ).add_to(m)
m

