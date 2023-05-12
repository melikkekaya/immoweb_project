import requests, csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
from time import perf_counter
import pandas as pd 

<<<<<<< HEAD
# We can create a class and add the root_url, estate type and 
# method of creating csv file to the init.

=======
>>>>>>> 125fd2e (pandas_main_test_creating_loop_byMelike)
root_url = "https://www.immoweb.be/en/search/"
estate_types = ['house', 'apartment']
max_page = 1  # Set the maximum page number to 333

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

def get_immo_dict(immo_links): 
     # we had some issues on data, it may not be possible to clean it, 
     # we may have to assign keys and values manually, i wrote here not to forget :D
   
    first_url = immo_links[0]
    create_csv(first_url)
    for root_url in immo_links:
        req = requests.get(root_url)
        print(req.status_code)
        read_html_houses = pd.read_html(req.text)
        data_frame_houses = pd.concat(read_html_houses)

        values = data_frame_houses.iloc[:,1]
        output_file = "real_estate_info.csv"

        with open(output_file, 'a') as csvfile:
            writer_object = csv.writer(csvfile)
            writer_object.writerow(values)

def replace_empty_with_none(dict_to_clean):
    for key, value in dict_to_clean.items():
        if isinstance(value, dict):
            replace_empty_with_none(value)
        elif isinstance(value, str) and not value:
            dict_to_clean[key] = None
    return dict_to_clean

def create_csv(first_url):
    req = requests.get(first_url)
    read_html_houses = pd.read_html(req.text)
    data_frame_houses = pd.concat(read_html_houses)

    keys = data_frame_houses.iloc[:,0]

    output_file = "real_estate_info.csv"
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()

def testing_sample_data(csv_file):
    csv_file = "real_estate_info.csv"
    data = pd.read_csv(csv_file, delimiter=',', on_bad_lines='skip')
    return data.head()



# get_immo_dict(get_url_list("house"))
testing_sample_data("real_estate_info.csv")

# start_time = perf_counter()

# immo_links = []
# with ThreadPoolExecutor() as executor:
#     for estate in estate_types:
#         immo_links.extend(executor.submit(get_url_list, estate).result())

# immo_dicts = []
# with ThreadPoolExecutor() as executor:
#     for link in immo_links:
#         result = executor.submit(get_immo_dict, link).result()
#         result = replace_empty_with_none(result)
#         immo_dicts.append(result)

# with open('immo_dump.json', 'w') as outfile:
#     json.dump(immo_dicts, outfile, indent=4)

# print("Scraping completed.")
# print(f"\nTime spent inside the loop: {perf_counter() - start_time} seconds.")