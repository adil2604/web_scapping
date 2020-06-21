#!/usr/bin/env python
# coding: utf-8

# # Создание слоя в GeoJSON формате

# In[1]:
import asyncio
import time

import aiohttp
import pandas as pd


async def download_site(session, url, query, country):
    """Get data for single address."""
    params = {
        'apiKey': 'SC3Kn9RrlGONe-DLadY4m4XMG4H-4xjogpzmCZXBF1A',
        'searchtext': query,
        'country': country
    }
    async with session.get(url, params=params) as res:
        try:
            data = await res.json()
            if data['Response']['View'][0]['Result'][0]['MatchLevel']=='houseNumber':
                data = data['Response']['View'][0]['Result'][0]['Location']
                return [data['Address']['Label'], data['DisplayPosition']['Longitude'], data['DisplayPosition']['Latitude'],query]
            else:
                return None
        except:
            print("Error with {}".format(query))


async def download_all_sites(geocode_df):
    """Helper function. Run all tasks."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        url = 'https://geocoder.ls.hereapi.com/6.2/geocode.json'
        for index, query in geocode_df.iterrows():
            task = asyncio.ensure_future(download_site(session, url, query['searchText'], query['country']))
            tasks.append(task)

        return await asyncio.gather(*tasks, return_exceptions=True)


def geocode_data(name,path_csv_file,path_to_out='out'):
    """Main driver function."""
    df = pd.read_csv(path_csv_file, sep=",", encoding="utf-8")
    df = df[df.latitude < 180]
    df = df[df.longitude < 180]
    geocode_df = pd.DataFrame(data={'recId': df.index, 'searchText': df['address'], 'country': df['country']})
    columns = [
        'address_geocoded',
        'displayLongitude',
        'displayLatitude',
        'address'
    ]
    geocoded_df = pd.DataFrame(columns=columns)
    start_time = time.time()
    all_data = asyncio.get_event_loop().run_until_complete(download_all_sites(geocode_df))
    duration = time.time() - start_time
    print(f"Geocoded in {duration} sec.")
    invalid = 0
    for d in all_data:
        # print(d)

        if d is not None:
            geocoded_df = geocoded_df.append(pd.Series(d, index=geocoded_df.columns), ignore_index=True)
        else:
            invalid = +1
    print(geocoded_df.head())
    geocoded_df.to_csv('{}/{}_geocoded_df.csv'.format(path_to_out,name))
    duration = time.time() - start_time
    print(f"Done in  {duration} seconds. {invalid} invalid address.")


geocode_data('Wildberries','Wildberries/all_data.csv')