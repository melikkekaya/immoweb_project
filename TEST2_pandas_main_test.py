import requests, csv, json, time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd 

# we had some issues on data, it may not be possible to clean it, 
# we may have to assign keys and values manually, i wrote here not to forget :D

class Immo_scrapy():
    search_url = "https://www.immoweb.be/en/search/"
    estate_types = ['house', 'apartment']
    max_page = 1  

    def get_url_list(self):
        immo_links = []
        page = 1
        for estate in self.estate_types:
            while page <= self.max_page:
                url = f"{self.search_url}{estate}/for-sale?countries=BE&page={page}&orderBy=relevance"
                req = requests.get(url)
                soup = BeautifulSoup(req.content, 'html.parser')
                card_results = soup.find_all('article', class_='card--result')
                for article in card_results:
                    link = article.find('a', class_='card__title-link')
                    if link:
                        immo_links.append(link['href'])
                page += 1
        return immo_links
    
    def get_search_page(self):
        response = requests.get(self.search_url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception("Error accessing the search page.")
    
    def scrape_data(self):
        for url in self.get_url_list():
            search_page_content = requests.get(url).content
            all_tables = pd.read_html(search_page_content, keep_default_na=False)
            data_frame_houses = pd.concat(all_tables, ignore_index=True)
        # search_soup = BeautifulSoup(search_page_content, 'html.parser')
        
        # property_urls = search_soup.find_all('a', class_='property-url')
        # all_data = []
        
        # for url in property_urls:
        #     property_url = url['href']
        #     property_data = self.scrape_property_data(property_url)
        #     all_data.append(property_data)
        
            # self.write_to_csv(data_frame_houses)
            return data_frame_houses
    
    def scrape_property_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            property_content = response.content
            property_soup = BeautifulSoup(property_content, 'html.parser')
            
            # TODO: Implement the specific scraping logic for property data
            
            # Example:
            property_title = property_soup.find('h1', class_='property-title').text.strip()
            property_price = property_soup.find('span', class_='price').text.strip()
            property_description = property_soup.find('div', class_='description').text.strip()
            
            return {
                'Title': property_title,
                'Price': property_price,
                'Description': property_description
            }
        else:
            raise Exception("Error accessing the property page.")
    
    def write_to_csv(self):
        house_dict = {}
        data_frame_houses = self.scrape_data()
        print(data_frame_houses)
        # for i in data_frame_houses.index:
        #     house_dict[data_frame_houses[0][i]] = data_frame_houses[1][i]
        
        # fieldnames = house_dict.keys
        # filename = 'real_estate_data.csv'

        # print(fieldnames)

        
        # with open(filename, mode='w', newline='') as file:
        #     writer = csv.DictWriter(file, fieldnames=fieldnames)
        #     writer.writeheader()
            
        #     for item in house_dict.values:
        #         writer.writerow(item)
        
        # print(f"Data has been written to {filename}.")

# Example usage
# search_url = 'https://www.example.com/search'
scraper = Immo_scrapy()
scraper.write_to_csv()


# Load data into a pandas DataFrame
# dataframe = pd.read_csv('real_estate_data.csv')
# print(dataframe.head())












# # #     root_url = "https://www.immoweb.be/en/search/"
# # #     estate_types = ['house', 'apartment']
# # #     max_page = 1  

#     def __init__(self):
#         output_file = "real_estate_info.csv"
#         first_url = self.get_url_list.immo_links[0]
#         req = requests.get(first_url)
#         read_html_houses = pd.read_html(req.text)
#         data_frame_houses = pd.concat(read_html_houses)

#         keys = data_frame_houses.iloc[:,0]
#         with open(output_file, 'w', newline='') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=keys)
#             writer.writeheader()

#     def get_url_list(self):
#         immo_links = []
#         page = 1
#         for estate in self.estate_types:
#             while page <= self.max_page:
#                 url = f"{self.root_url}{estate}/for-sale?countries=BE&page={page}&orderBy=relevance"
#                 req = requests.get(url)
#                 soup = BeautifulSoup(req.content, 'html.parser')
#                 card_results = soup.find_all('article', class_='card--result')
#                 for article in card_results:
#                     link = article.find('a', class_='card__title-link')
#                     if link:
#                         immo_links.append(link['href'])
#                 page += 1
#         return immo_links

#     def create_csv(first_url):
#         first_url = get_url_list.immo_links[0]
#         req = requests.get(first_url)
#         read_html_houses = pd.read_html(req.text)
#         data_frame_houses = pd.concat(read_html_houses)

#         keys = data_frame_houses.iloc[:,0]

#         output_file = "real_estate_info.csv"
#         with open(output_file, 'w', newline='') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=keys)
#             writer.writeheader()
#     def get_immo_dict(self): 
#         for root_url in self.get_url_list():
#             req = requests.get(root_url)
#             print(req.status_code)
#             read_html_houses = pd.read_html(req.text)
#             data_frame_houses = pd.concat(read_html_houses)

#             values = data_frame_houses.iloc[:,1]
#             output_file = "real_estate_info.csv"

#             with open(output_file, 'a') as csvfile:
#                 writer_object = csv.writer(csvfile)
#                 writer_object.writerow(values)

#     def replace_empty_with_none(dict_to_clean):
#         for key, value in dict_to_clean.items():
#             if isinstance(value, dict):
#                 replace_empty_with_none(value)
#             elif isinstance(value, str) and not value:
#                 dict_to_clean[key] = None
#         return dict_to_clean



#     def testing_sample_data(csv_file):
#         csv_file = "real_estate_info.csv"
#         data = pd.read_csv(csv_file, delimiter=',', on_bad_lines='skip')
#         return data.head()



# # get_immo_dict(get_url_list("house"))


