import json
import re

import geopandas as gpd
import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = 'https://www.wildberries.kz/services/besplatnaya-dostavka'


def is_file_contain_country(path, country):
    with open(path) as file:
        countries = file.read().split('\n')[:-1]
        if country in countries:
            return False
        return True


def prettify_get(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')  # content is a html page
    return soup


def search_pickup(soup, script):
    info = soup.findAll('script')[script]
    match = re.search(r"var pickpoints = \[(.+)\]", str(info))
    return match


def get_countries():
    """Get list countries from WildBerries."""
    soup = prettify_get(URL)
    countries = soup.find('li', class_='item change-locale')
    countries = countries.find_all('a', href=True)
    for country in countries:
        print("Starting mining for {}".format(country.getText()))
        URL_COUNTRY = country['href']
        get_data(URL_COUNTRY, country.getText())
        # print(URL_COUNTRY)


def get_data(url, name):
    """Get all pickup points in country."""
    try:
        soup = prettify_get(url + '/services/besplatnaya-dostavka')
        data = search_pickup(soup, 10)
        data = json.loads(data.group(0).split('=')[1])
    except AttributeError:
        try:
            soup = prettify_get(url + '/services/free-shipping')
            data = search_pickup(soup, 8)
            data = json.loads(data.group(0).split('=')[1])
        except AttributeError:
            print('Error in parsing {}'.format(url))
            data = {}
    print("Founded {} pickup points.".format(len(data)))
    df = pd.DataFrame(data)
    df['country'] = name.split(' / ')[1]
    df.to_csv('Wildberries/Data-{}.csv'.format(name.split(' / ')[1]))
    if is_file_contain_country('countries.txt', name.split(' / ')[1]):
        with open('Wildberries/countries.txt', 'a') as file:
            file.write(name.split(' / ')[1] + '\n')
            file.close()


def data_to_geodata():
    """Convert CSV data to GeoJson format."""
    with open('Wildberries/countries.txt', 'r') as file:
        countries = file.read().split('\n')[:-1]
    print(countries)
    df = pd.DataFrame()
    for country in countries:
        df = df.append(pd.read_csv('Wildberries/Data-{}.csv'.format(country)))
    df[['latitude', 'longitude']] = df.coordinates.str.split(',', expand=True)
    df[['latitude', 'longitude']] = df[['latitude', 'longitude']].astype(float)
    df.to_csv('out/Wildberries_data.csv')
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    print(gdf.head())
    gdf.to_file('out/Wildberries_data.geojson', driver="GeoJSON")


# get_data('https://sk.wildberries.eu')
get_countries()
data_to_geodata()
