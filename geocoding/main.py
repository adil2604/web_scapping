import geopandas as gpd
import pandas as  pd
from geopy.distance import geodesic
from shapely.geometry import LineString


def geo_distances(dataframe_file, geocoded_dataframe_file,name=''):
    df = pd.read_csv(dataframe_file)
    geocoded_df = pd.read_csv(geocoded_dataframe_file)
    geocoded_df = geocoded_df.drop('Unnamed: 0', 1)
    new_df = pd.DataFrame()
    new_df['latitude'] = df['latitude']
    new_df['longitude'] = df['longitude']
    new_df['address'] = df['address']
    merged_df = new_df.merge(geocoded_df, how='inner', on=['address'])

    distances = []
    df_distances = gpd.GeoDataFrame()
    for index, row in merged_df.iterrows():
        df_point = (row["latitude"], row["longitude"])
        geocoded_point = (row["displayLatitude"], row["displayLongitude"])

        distances.append(geodesic(df_point, geocoded_point).km)

    z1 = [point for point in zip(merged_df["longitude"], merged_df["latitude"])]
    z2 = [point for point in zip(merged_df["displayLongitude"], merged_df["displayLatitude"])]

    df_distances["geometry"] = [LineString(resu) for resu in zip(z1, z2)]
    df_distances.to_file('out/{}_distances.geojson'.format(name), driver="GeoJSON")
    print('Done.')


def geocoded_data_to_geojson(file,name):
    geocoded_df = pd.read_csv(file)
    geocoded_gdf = gpd.GeoDataFrame(geocoded_df, geometry=gpd.points_from_xy(geocoded_df.displayLongitude,
                                                                             geocoded_df.displayLatitude))
    geocoded_gdf.to_file('out/{}_data_geocoded.geojson'.format(name), driver="GeoJSON")

# geo_distances('out/Wildberries_data.csv','out/Wildberries_geocoded_df.csv','Wildberries')

geocoded_data_to_geojson('out/Wildberriesgeocoded_df.csv','Wildberries')
