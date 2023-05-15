import requests, json, lxml, re, csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import pandas as pd
from typing import List, Dict

class Immoweb():
    # root_url = "https://www.immoweb.be/en/search/"
    # all_data_file = "all_data.csv"
    # search_links = []
    # estate_types = ['house', 'apartment']
    # all_immo_links = []

    # def __init__(self):
    #     self.search_links = self.get_search_list()
    #     self.immo_links = self.get_link_from_search_page()
        
    # def get_search_list(self) -> List:
    #     for estate in self.estate_types:
    #         for page in range(1,334): #for testing purpose I changed from 334 to 2
    #             url = f"{self.root_url}{estate}/for-sale?countries=BE&page={page}&orderBy=relevance"
    #             self.search_links.append(url)
    #     with ThreadPoolExecutor() as pool:
    #         self.all_immo_links = list(pool.map(self.get_link_from_search_page, self.search_links))
    #     return self.search_links

    # def get_link_from_search_page(self,search_links):
    #     for link in search_links:
    #         req = requests.get(link)
    #         soup = BeautifulSoup(req.content, 'html.parser')
    #         card_results = soup.find_all('article', class_='card--result')
    #         immo_links = []
    #         for article in card_results:
    #             link = article.find('a', class_='card__title-link')
    #             if link:
    #                 immo_links.append(link['href'])
    #     # return immo_links

    # def new(self):
    #     with ThreadPoolExecutor() as pool:
    #         self.all_immo_links = list(pool.map(self.get_link_from_search_page, self.search_links))
    #     return self.all_immo_links
    
    def get_from_search_page(self,search_url):
        req = requests.get(search_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        card_results = soup.find_all('article', class_='card--result')
        immo_links = []
        for article in card_results:
            link = article.find('a', class_='card__title-link')
            if link:
                immo_links.append(link['href'])
        return immo_links

    def get_url_list(self) -> List:
        root_url = "https://www.immoweb.be/en/search/"
        estate_types = ['house', 'apartment']
        all_immo_links = []
        search_links = []

        for estate in estate_types:
            for page in range(1,2): #for testing purpose I changed from 334 to 2
                url = f"{root_url}{estate}/for-sale?countries=BE&page={page}&orderBy=relevance"
                search_links.append(url)
        
        with ThreadPoolExecutor() as pool:
            all_immo_links = list(pool.map(self.get_from_search_page, search_links))
        all_immo_links = all_immo_links[0]+all_immo_links[1]

        return all_immo_links

    def get_one_property_info(self, url_one_property:str) -> Dict: 
        req = requests.get(url_one_property)
        print(req.status_code)
        read_html_prop = pd.read_html(req.text)
        df_one_property = pd.concat(read_html_prop, ignore_index=True)

        list_of_property_info = []
        window_data = re.findall("window.dataLayer =(.+?);\n", req.text, re.S)
        if window_data:
            list_of_property_info.append(json.loads(window_data[0])[0]['classified'])
        
        house_dict = list_of_property_info[0]

        for i in df_one_property.index:
            house_dict[df_one_property[0][i]] = df_one_property[1][i]

        return house_dict


    def clean_data_to_csv(self, original_dict) -> Dict:
        """
        take info from get_one_prop_info() as json or dict,
        and add them to a csv for only one property.
        """

        has_fireplace = int(original_dict.get('How many fireplaces?'))
        new_dict = {
        "Id": original_dict.get('id'), 
        'Locality': original_dict.get('Neighbourhood or locality'),
        'Type of property': original_dict.get('type'),
        'Subtype of property': original_dict.get('subtype'),
        'Price': original_dict.get('price'),
        'Type of sale': original_dict.get('transactionType'),
        'Number of rooms': original_dict.get('Bedrooms'),
        'Living Area': original_dict.get('Living area').split(' ', 1)[0],
        'Fully equipped kitchen': original_dict['kitchen']['type'],
        'Furnished': True if original_dict.get('Furnished').lower()== 'yes' else False,
        'Open fire': True if has_fireplace >= 1 else False,
        'Terrace': False if original_dict['outdoor']['terrace']['exists'].lower() != 'true' else True,
        'Garden': False if int(original_dict['outdoor']['garden']['surface'])<1  else True,
        'Surface area of the plot of land': original_dict.get('Surface of the plot').split(' ', 1)[0],
        'Number of facades': original_dict.get('Number of frontages'),
        "Swimming pool": original_dict['wellnessEquipment']['hasSwimmingPool'],
        "State of the building": original_dict.get('Building condition'),
        "Url": original_dict.get('url')
        }
        return new_dict
        


    def adding_one_line_into_csv(self, new_dict):
        new_dict = self.clean_data_to_csv()
        header = ["Id", 'Locality', 'Type of property','Subtype of property','Price','Type of sale','Number of rooms','Living Area','Fully equipped kitchen','Furnished','Open fire','Terrace','Garden','Surface area of the plot of land','Number of facades',"Swimming pool","State of the building","Url"]
        with open(self.all_data_file, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerow(new_dict)

    def get_collective_data(self):
        """
        clean_data_to_csv() for all urls from get_url_list() using pool
        """
        all_links = self.get_url_list()
        with ThreadPoolExecutor() as pool:
            
            pool.map(self.adding_one_line_into_csv(self.clean_data_to_csv(self.get_one_property_info)), all_links)

# get_collective_data()

# adding_one_line_into_csv(clean_data_to_csv(get_one_property_info("https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/10459437")))
# get_one_property_info("https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/10459437")


# main.get_collective_data()
# print(main.get_link_from_search_page())



main = Immoweb()
# print(len(main.get_collective_data()))  
print(main.get_collective_data())  




# if __name__ == "__main__":
#     main = Immoweb()
#     start = perf_counter()
#     # print(len(main.get_link_from_search_page()))
#     end=perf_counter()
#     pool_time = end-start
#     print("pool_time: ", pool_time)