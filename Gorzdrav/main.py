import requests
from bs4 import BeautifulSoup
import pandas as pd
import geopandas as gpd


def get_data():
    url='https://gorzdrav.org/store-finder/all/'
    headers={
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'

    }
    res=requests.get(url,headers=headers)
    data=res.json()['data']
    df=pd.DataFrame(data)

    df[['latitude', 'longitude']] = df[['latitude', 'longitude']].astype(float)
    df.to_csv('out/Gorzdrav_data.csv')

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    gdf.to_file('out/Gorzdrav_data.geojson', driver="GeoJSON")
    print(df.info())

get_data()
