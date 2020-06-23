import geopandas as gpd
import pandas as pd
import requests


def get_data():
    url = 'https://rtapi.south.rt.ru/apiman-gateway/new-rt/offices-location/1.0/offices?apikey=d1568b75-38cd-40e2-8420-5e49c45fc8df'
    data = {"right_top": {"lat": "82.67628497834903", "long": "233.08593749999997"},
            "left_bottom": {"lat": "-17.644022027872712", "long": "-40.42968749999999"}}
    headers = {
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'

    }
    res = requests.post(url, json=data, headers=headers)
    data = res.json()['result']
    df = pd.DataFrame(data)

    df.rename(
        columns={'cn': 'city_name', 'sn': 'street_name', 'hn': 'house_number', 'lat': 'latitude', 'long': 'longitude'},
        inplace=True)
    df[['latitude', 'longitude']] = df[['latitude', 'longitude']].astype(float)
    df.to_csv('out/Rostelecom_data.csv')

    df = df.drop('svc', 1)
    df = df.drop('tc', 1)
    df = df.drop('tt', 1)
    df = df.drop('m', 1)
    df = df.drop('pb2b', 1)
    df = df.drop('fl', 1)

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    gdf.to_file('out/Rostelecom_data.geojson', driver="GeoJSON")
    print(df.info())


get_data()
