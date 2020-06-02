from random import choice
import pandas as pd
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from agents import user_agent_list
from settings import read_proxies
import time


def read_cities():
    """Read cities from file."""
    with open('cities.txt', 'r', encoding='utf8') as file:
        cities = file.read().split('\n')[:-1]
    return cities


def get_cities():
    """Get list of cities from KazPost site and save it into file."""
    file = open('cities.txt', 'w', encoding='utf8')

    #  selenium driver
    opts = Options()
    opts.headless = True
    assert opts.headless
    browser = Chrome('E:/chromedriver.exe', options=opts)

    #  gets source code of page
    browser.get('https://post.kz')
    cities = browser.find_elements_by_class_name('styles_menu__item__2kv7Z')

    #  saving into file
    for city in cities[3:]:
        name = city.get_attribute('innerHTML')
        file.write(name + '\n')
        print(name)
    file.close()


def main():
    """Main driver function."""
    df = pd.DataFrame()  # empty dataframe
    proxies = read_proxies()  # read proxies from file
    cities = read_cities()  # read cities from file
    get_data(proxies, cities, df)


def get_data(proxies, cities, df):
    """Get geo-data from API and save it into file"""
    proxy = choice(proxies).split('://')  # choosing proxy
    print('Starting with {}'.format(proxy[1]))

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': '__ddg1=jKjZlDGVGiFlw2evkYjW; NG_TRANSLATE_LANG_KEY=ru; __ddg2=7y6myF2kkKuhsjCC; __ddg1=tZrXKFIePZNAsCNkQPEI',
        'user-agent': choice(user_agent_list)  # choosing user-agent
    }

    proxydict = {proxy[0]: proxy[1]}

    try:
        copy_cities = cities.copy()
        for city in copy_cities:
            print("STARTING COLLECT DATA FOR {}".format(city))
            payload = "{\"address\":\"" + city + "\"}"
            res = requests.request('POST', 'https://post.kz/mail-app/api/public/find_dep', data=payload.encode('utf-8'),
                                   proxies=proxydict, headers=headers, timeout=5)
            df = df.append(pd.read_json(res.text))
            print(df)
            cities.remove(city)  # remove city if data collected

            time.sleep(20)  # delay
        print(df)
        df.sort_values('fp_id', inplace=True)  # sorting by id to minizing computations
        df.drop_duplicates(subset="fp_id", keep=False, inplace=True)  # deleting duplicates
        df.to_csv('data_kazpost.csv', index=False)  # saving
    except:
        proxies.remove('://'.join(proxy))  # delete from proxy list if it is not valid
        if len(proxies):
            get_data(proxies, cities, df)


main()
