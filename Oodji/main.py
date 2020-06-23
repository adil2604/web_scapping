import geopandas as gpd
import pandas as pd
import requests


def get_data():
    url = 'https://www.oodji.com/local/components/oodji/shops.list/ajax.php'
    data = {'type': 'getShops', 'sessid': '82db094b58e8e83d935f558ac0aadcb9'}
    headers = {
        'cookie': 'PHPSESSID=7B0idw119zNfG6h5R11nQO5h03wA837V; BITRIX_SM_CITY=%7B%22id%22%3A%22760%22%2C%22name%22%3A%22%5Cu041c%5Cu043e%5Cu0441%5Cu043a%5Cu0432%5Cu0430%22%7D; BITRIX_SM_DELIVERY_CITY=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; BITRIX_SM_SALE_UID=45ec2e667d29ecbefb08b8acc9b94bf3; BITRIX_SM_SHOWED_CZ=1; x_mobile=0; ipp_uid2=JQ7iaL8VBa0FNWoT/hZnBsENbOJgolrTQJL/jHg==; ipp_uid1=1592929399447; ipp_uid=1592929399447/JQ7iaL8VBa0FNWoT/hZnBsENbOJgolrTQJL/jHg==; rerf=AAAAAF7yLHfC9z99AwjQAg==; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2020-06-23%2022%3A23%3A20%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.oodji.com%2Fmap%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2020-06-23%2022%3A23%3A20%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.oodji.com%2Fmap%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F83.0.4103.106%20Safari%2F537.36; sbjs_session=pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.oodji.com%2Fmap%2F; BITRIX_CONVERSION_CONTEXT_ru=%7B%22ID%22%3A5%2C%22EXPIRE%22%3A1592945940%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; mindboxDeviceUUID=aa880a59-2b31-4244-b3cd-65bd338ecaaf; directCrm-session=%7B%22deviceGuid%22%3A%22aa880a59-2b31-4244-b3cd-65bd338ecaaf%22%7D; tmr_lvid=d7803e7ce971ce880d5da71f6bfedea4; tmr_lvidTS=1592929401528; tmr_detect=1%7C1592929401588; tmr_reqNum=2; _ga=GA1.2.1919126920.1592929402; _gid=GA1.2.1240317257.1592929402; BITRIX_SM_CITY=%7B%22id%22%3A%22760%22%2C%22name%22%3A%22%5Cu041c%5Cu043e%5Cu0441%5Cu043a%5Cu0432%5Cu0430%22%7D; BITRIX_SM_DELIVERY_CITY=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; BITRIX_SM_SALE_UID=45ec2e667d29ecbefb08b8acc9b94bf3; BITRIX_SM_SHOWED_CZ=1; _ym_uid=1592929403647293004; _ym_d=1592929403',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'

    }
    res = requests.post(url, data=data, headers=headers)
    data = res.json()
    #     print(data)
    df = pd.DataFrame(data).transpose()
    df[['latitude', 'longitude']] = df.GMAP.str.split(',', expand=True)
    df.to_csv('out/Oodji_data_dirty.csv')

    df = df.drop('LINKS_NEW', 1)
    df.dropna(subset=['latitude', 'longitude'], inplace=True)
    df.to_csv('out/Oodji_data_clean.csv')

    df[['latitude', 'longitude']] = df[['latitude', 'longitude']].astype(float)

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    gdf.to_file('out/Oodji_data.geojson', driver="GeoJSON")
    print(df)


get_data()
