import requests
import re
import pandas as pd
import geopandas as gpd
from bs4 import BeautifulSoup

def get_data():
    url = 'https://vimos.ru/contacts'
    res = requests.get(url)
    match = re.search(r"clusterer\.add\(new ymaps\.Placemark\((;|(.|\n)+) \);", str(res.text))

    data = match.group(0).split(' );')[:-1]

    df = pd.DataFrame(columns=['address', 'phone', 'time', 'latitude', 'longitude'])

    for point in data:
        soup = BeautifulSoup(re.search(r"{balloonContent: \'.+\'", point).group(0), 'lxml')

        latitude, longitude = map(float, re.search(r"\[.+\]", point).group(0)[1:-1].split(','))
        address = soup.find_all('div')[4].getText()
        phone = soup.find_all('div')[5].getText()
        time = soup.find_all('div')[7].getText()

        df = df.append(pd.Series([address, phone, time, latitude, longitude], index=df.columns), ignore_index=True)
    df.to_csv('out/Vimos_data.csv')
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    gdf.to_file('out/Vimos_data.geojson', driver="GeoJSON")
    print(df)


#     print(res.text)

get_data()