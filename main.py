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
        property = property.set_index("id")
        property = property.loc[:, ~property.columns.duplicated()].copy()
        
        return property
    

        # df_prop = df_prop.loc[:, ~df_prop.columns.duplicated()].copy()

        # data_prop.append(df_prop)

        # return data_prop
        # list_of_property_info = []
        # window_data = re.findall("window.dataLayer =(.+?);\n", req.text, re.S)
        # if window_data:
        #     list_of_property_info.append(json.loads(window_data[0])[0]['classified'])
        
        # original_dict = list_of_property_info[0]

        # for i in df_one_property.index:
        #     original_dict[df_one_property[0][i]] = df_one_property[1][i]

        #     df_dict = pd.DataFrame([original_dict])
    except Exception as e:
        print(type(e))
        return e

if __name__ == "__main__":
    search_links = get_search_url_list(end_page=334)

    urls = list(itertools.chain.from_iterable(thread_map(get_urls_from_search_page, search_links)))

    with requests.Session() as session:
        properties = pd.concat(df for df in thread_map(partial(get_property, session=session), urls) 
                               if isinstance(df, pd.DataFrame))

    properties.to_csv("properties.csv")





# # start = perf_counter()


# # # df_list = []
# # # with ThreadPoolExecutor() as pool:
# # #     final = list(pool.map(get_one_property_info,all_immo_links))
# # #     print(final)
# # #     for result in final:
# # #         df_list.append(result)
# # # full_data = pd.concat(df_list)
# # # full_data.to_csv("new.csv")


# # end=perf_counter()
# # pool_time = end-start
# # print("pool_time: ", pool_time)

# # df = (get_one_property_info('https://www.immoweb.be/en/classified/house/for-sale/jehay/4540/10564525'))
# # print(df.tail())

# # # all_urls = get_url_list()
# # # with ThreadPoolExecutor() as pool:
# # #     pool.map(all_get_one_property_info, all_urls)

# # #     properties = pd.concat(properties)


# # # properties.to_csv("immoweb_properties_data.csv")

# #     # living_area = original_dict.get('Living area')
# #     # living_area_value = living_area.split(' ', 1)[0] if living_area is not None else None

# #     # surface_of_plot = original_dict.get('Surface of the plot')
# #     # surface_of_plot_value = surface_of_plot.split(' ', 1)[0] if surface_of_plot is not None else None
    
# #     # new_dict = {
# #     # "Id": original_dict.get('id'),
# #     # 'Locality': url_one_property.split("/")[-3],
# #     # 'Type of property': original_dict['type'],
# #     # 'Subtype of property': original_dict['subtype'],
# #     # 'Price':original_dict['price'],
# #     # 'Type of sale': original_dict['transactionType'],
# #     # 'Number of rooms': original_dict.get('Bedrooms'),
# #     # 'Living Area': living_area_value,
# #     # 'Fully equipped kitchen': original_dict['kitchen']['type'],
# #     # 'Furnished': True if original_dict.get('Furnished', '').lower() == 'yes' else False,
# #     # 'Open fire': True if int(original_dict['How many fireplaces?']) >= 1 else False,
# #     # 'Terrace': False if original_dict['outdoor']['terrace']['exists'].lower() != 'true' else True,
# #     # 'Garden': False if int(original_dict['outdoor']['garden']['surface'] or 0) < 1 else True,
# #     # 'Surface area of the plot of land': surface_of_plot_value,
# #     # 'Number of facades': original_dict['Number of frontages'],
# #     # "Swimming pool": original_dict['wellnessEquipment']['hasSwimmingPool'],
# #     # "State of the building": original_dict['Building condition'],
# #     # "Url": url_one_property
# #     # }
    
# #     # with open(self.all_data_file, 'a') as file:
# #     #     file.write(','.join(str(x) for x in original_dict.values()))
# #     #     file.write('\n') 
        

# # # def all_get_collective_data(self):
    
# # #     try:
# # #         with ThreadPoolExecutor() as pool:
# # #             main = Immoweb()
# # #             m = list(pool.map(self.all_get_one_property_info, main.get_url_list()[0]))
# # #     except:
# # #         print("Error occured: ")

# # def all_get_collective_data(self):
# #     list_of_urls = self.get_url_list()[0]
# #     print(len(list_of_urls))
# #     main_df_list = []

# #     with ThreadPoolExecutor() as pool:
# #         datas = list(pool.map(self.all_get_one_property_info,list_of_urls))
# #         for data in datas:
# #             main_df_list.append(data)
# #     main_df = pd.concat(main_df_list)
# #     main_df.to_csv("aaaaaa3_test.csv")
    
    


# # #     def all_get_collective_data(self):
    
# # #         # try:
# # #             # with ThreadPoolExecutor() as pool:
# # #             #     with open ("url_list.txt","r") as file:
# # #             #         # for i in file:
# # #             #         #     self.all_get_one_property_info(file.readline(i))
# # #             #         #     print(i)
# # #             #         #     print(file.readline(i))
# # #             #         m = list(pool.map(self.all_get_one_property_info, file.readlines))
        
# # #         with open("url_list9.txt", "r") as file:
# # #             for index,i in enumerate(file):
# # #                 self.all_get_one_property_info(i)
# # #             # return (map(self.all_get_one_property_info, file))
# # #         # except:
# # #         #     print("Error occured: ")
# # # # main = Immoweb()
# # # # # print(len(main.get_collective_data()))  
# # # # main.get_collective_data()

# # # main = Immoweb()
# # # a=(main.all_get_one_property_info("https://www.immoweb.be/en/classified/house/for-sale/jehay/4540/10564525"))
# # # a.to_csv("aaaaaa2_test.csv")

# # if __name__ == "__main__":

# #     start = perf_counter()

# #     # with open("url_list9.txt", 'a') as file:
# #     #     for i in main.get_url_list()[0]:
# #     #         file.write(str(i)+'\n')
# #     # main.all_get_collective_data()
# #     end=perf_counter()
# #     pool_time = end-start
# #     print("pool_time: ", pool_time)