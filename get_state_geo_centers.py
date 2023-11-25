import requests
import pandas as pd
import regex as re

url = 'https://en.wikipedia.org/wiki/List_of_geographic_centers_of_the_United_States'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[1]
df

daf=df['Coordinates'].str.split(pat="/",expand=True)
daf['coord']=daf[1]
daf=daf.drop([0,1], axis=1)
daf=daf['coord'].str.split(pat=" ",expand=True)

for x in range(len(daf)):
    if re.findall('°N',daf.loc[x,1]):
        daf.loc[x, 1]=re.sub('°N' ,'' ,daf.loc[x, 1])       
        daf.loc[x, 'lat']=int(round(float(re.sub('\ufeff','',daf.loc[x, 1])),0))

    if re.findall('°S',daf.loc[x,1]):
        daf.loc[x, 1]=re.sub('°S' ,'' ,daf.loc[x, 1])       
        daf.loc[x, 'lat']=round(float(re.sub('\ufeff','',daf.loc[x, 1])),0)*-1


    if re.findall('°E',daf.loc[x,2]):
        daf.loc[x, 2]=re.sub('°E' ,'' ,daf.loc[x, 2])       
        daf.loc[x, 'lon']=int(round(float(re.sub('\ufeff','',daf.loc[x, 2])),0))

    if re.findall('°W',daf.loc[x,2]):
        daf.loc[x, 2]=re.sub('°W' ,'' ,daf.loc[x, 2])       
        daf.loc[x, 'lon']=round(float(re.sub('\ufeff','',daf.loc[x, 2])),0)*-1


daf=daf[['lat','lon']]
daf

daf=pd.merge(daf, df, left_index=True, right_index=True, how="outer")


url = 'https://www.faa.gov/air_traffic/publications/atpubs/cnt_html/appendix_a.html'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[0]
df1=df[['STATE(TERRITORY)','STATE(TERRITORY).1']]
df1=df1.rename(columns={'STATE(TERRITORY)':'State or federal district','STATE(TERRITORY).1':"STATE"})
df2=df[['STATE(TERRITORY).2','STATE(TERRITORY).3']]
df2=df2.rename(columns={'STATE(TERRITORY).2':'State or federal district','STATE(TERRITORY).3':"STATE"})
df3=df[['STATE(TERRITORY).4','STATE(TERRITORY).5']]
df3=df3.rename(columns={'STATE(TERRITORY).4':'State or federal district','STATE(TERRITORY).5':"STATE"})
df4=pd.concat([df1,df2,df3])
df4=df4.reset_index(drop=True)

daf1=pd.merge(daf, df4, left_on='State or federal district', right_on="State or federal district", how="outer")
daf1=daf1.drop(columns=['Location','Coordinates'])
daf1=daf1.dropna(subset=['lat','lon'])
daf1.to_csv(r"D:\Data\OpTreat\state_center.csv")