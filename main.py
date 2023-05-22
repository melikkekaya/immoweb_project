import requests, json, lxml, re, csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import pandas as pd
from typing import List, Dict
import itertools
from functools import partial
from tqdm.contrib.concurrent import thread_map

def get_urls_from_search_page(search_url):
    req = requests.get(search_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    card_results = soup.find_all('article', class_='card--result')
    
    immo_links = []
    for article in card_results:
        link = article.find('a', class_='card__title-link')
        if link:
            immo_links.append(link['href'])
    return immo_links

def get_search_url_list(end_page):
    estate_types = ["house","apartment"]

    search_links = []
    for estate in estate_types:
        for page in range(1, end_page): #for testing purpose I changed from 334 to 2
            url = f"https://www.immoweb.be/en/search/{estate}/for-sale?countries=BE&page={page}&orderBy=relevance"
            search_links.append(url)
    return search_links


def get_property(url, session): 
    data_prop = []

    try:
        req = session.get(url)
        read_html_prop = pd.read_html(req.text)
        property = pd.concat(read_html_prop).set_index(0).T
        property["id"] = url.split("/")[-1]
        property["location"] = url.split("/")[-3]
        
        window_data = re.findall("window.dataLayer =(.+?);\n", req.text, re.S)
        extra_data = json.loads(window_data[0])[0]['classified']

        property["Type"] = extra_data["type"]
        property["Subtype"] = extra_data["subtype"]
        property["Price"] = extra_data["price"]
        property["Transaction Type"] = extra_data["transactionType"]
        property["Zip"] = extra_data["zip"]
        
        property = property.set_index("id")
        property = property.loc[:, ~property.columns.duplicated()].copy()

        return property
    
    except Exception as e:
        print(type(e))
        return e

if __name__ == "__main__":
    search_links = get_search_url_list(end_page=334)

    urls = list(itertools.chain.from_iterable(thread_map(get_urls_from_search_page, search_links)))

    with requests.Session() as session:
        properties = pd.concat(df for df in thread_map(partial(get_property, session=session), urls) 
                               if isinstance(df, pd.DataFrame))

    properties.to_csv("properties_data.csv")

