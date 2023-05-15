import requests
from bs4 import BeautifulSoup
import concurrent.futures
# from multiprocessing import Pool, Process, freeze_support

import json
from time import perf_counter

root_url = "https://www.immoweb.be/en/search/"
estate_types = ['house', 'apartment']
max_page = 333  # Set the maximum page number to 333

def get_url_list(estate):
    immo_links = []
    page = 1

    while page <= max_page:
        url = f"{root_url}{estate}/for-sale?countries=BE&page={page}&orderBy=relevance"
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        card_results = soup.find_all('article', class_='card--result')
        for article in card_results:
            link = article.find('a', class_='card__title-link')
            if link:
                immo_links.append(link['href'])
        page += 1
    return immo_links




        for country in countries:
            leaders_response = requests.get(leaders_url, cookies=get_cookie(), params={"country": country})
            leaders_per_country[country] = leaders_response.json()
            
            with Pool () as pool:
                leaders_per_country[country]=list(pool.map(leader_setter, leaders_per_country[country]))

def get_immo_dict(link):
    
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser')
    script_tags = soup.find_all('script')
    second_script = script_tags[1]
    script_content = second_script.string
    new_script_content = script_content.split('"classified": ')[1]
    new_new_cont = new_script_content.split(""",
                                    "customer": """)[0]
    dict1 = json.loads(new_new_cont)
    return dict1

def replace_empty_with_none(dict_to_clean):
    for key, value in dict_to_clean.items():
        if isinstance(value, dict):
            replace_empty_with_none(value)
        elif isinstance(value, str) and not value:
            dict_to_clean[key] = None
    return dict_to_clean

start_time = perf_counter()

immo_links = []
with ThreadPoolExecutor() as executor:
    for estate in estate_types:
        immo_links.extend(executor.submit(get_url_list, estate).result())

immo_dicts = []
with ThreadPoolExecutor() as executor:
    for link in immo_links:
        result = executor.submit(get_immo_dict, link).result()
        result = replace_empty_with_none(result)
        immo_dicts.append(result)

with open('immo_dump.json', 'w') as outfile:
    json.dump(immo_dicts, outfile, indent=4)

print("Scraping completed.")
print(f"\nTime spent inside the loop: {perf_counter() - start_time} seconds.")