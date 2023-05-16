import requests, json, lxml, re, csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import pandas as pd
from typing import List, Dict

start_time = perf_counter()
header = ["Id", 'Locality', 'Type of property','Subtype of property','Price','Type of sale','Number of rooms','Living Area','Fully equipped kitchen','Furnished','Open fire','Terrace','Garden','Surface area of the plot of land','Number of facades',"Swimming pool","State of the building","Url"]
all_data_file = "all_data2.csv"

#Retrieve all links from a page (url)
def get_from_search_page(search_url):
    req = requests.get(search_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    card_results = soup.find_all('article', class_='card--result')
    immo_links = []
    for article in card_results:
        link = article.find('a', class_='card__title-link')
        if link:
            immo_links.append(link['href'])
    return immo_links

#Creates a list of links
def get_url_list() -> List:
    root_url = "https://www.immoweb.be/en/search/"
    estate_types = ['house', 'apartment']
    all_immo_links = []
    search_links = []

    for estate in estate_types:
        for page in range(1,334): #for testing purpose I changed from 334 to 2
            url = f"{root_url}{estate}/for-sale?countries=BE&page={page}&orderBy=relevance"
            search_links.append(url)
    
    with ThreadPoolExecutor() as pool:
        all_immo_links = list(pool.map(get_from_search_page, search_links))
    return all_immo_links[0]

#Collects all data from a property
def get_one_property_info(url_one_property:str) -> Dict: 
    req = requests.get(url_one_property)
    #print(req.status_code)
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


def clean_data_to_csv(original_dict) -> Dict:
    """
    Take info from get_one_prop_info() as JSON or dict,
    and add them to a CSV for only one property.
    """

    has_fireplace = int(original_dict.get('How many fireplaces?', 0))
    living_area = original_dict.get('Living area')
    living_area_value = living_area.split(' ', 1)[0] if living_area is not None else None

    surface_of_plot = original_dict.get('Surface of the plot')
    surface_of_plot_value = surface_of_plot.split(' ', 1)[0] if surface_of_plot is not None else None

    new_dict = {
        "Id": original_dict.get('id'),
        'Locality': original_dict.get('Neighbourhood or locality'),
        'Type of property': original_dict.get('type'),
        'Subtype of property': original_dict.get('subtype'),
        'Price': original_dict.get('price'),
        'Type of sale': original_dict.get('transactionType'),
        'Number of rooms': original_dict.get('Bedrooms'),
        'Living Area': living_area_value,
        'Fully equipped kitchen': original_dict['kitchen']['type'],
        'Furnished': True if original_dict.get('Furnished', '').lower() == 'yes' else False,
        'Open fire': True if has_fireplace >= 1 else False,
        'Terrace': False if original_dict['outdoor']['terrace']['exists'].lower() != 'true' else True,
        'Garden': False if int(original_dict['outdoor']['garden']['surface'] or 0) < 1 else True,
        'Surface area of the plot of land': surface_of_plot_value,
        'Number of facades': original_dict.get('Number of frontages'),
        "Swimming pool": original_dict['wellnessEquipment']['hasSwimmingPool'],
        "State of the building": original_dict.get('Building condition'),
        "Url": original_dict.get('url')
    }
    print(new_dict)
    return new_dict 
    


def adding_one_line_into_csv(new_dict):
    #new_dict = clean_data_to_csv()
    # with open (all_data_file, "w") as file:
    #     file.write(",".join(new_dict.values()))
    #     file.write("\n")

    #TO FIX VALUES ONLY
    
    with open(all_data_file, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerow(new_dict.values())





def get_collective_data():
    """
    clean_data_to_csv() for all urls from get_url_list() using pool
    """
    # append data frame to CSV file
    # df.to_csv('GFG.csv', mode='a', index=False, header=False)
    #call clean data to csv for each urls
    #collective_data=[]

    all_links = get_url_list()
    #all_links could be replaced directly by all_immo_links


    with ThreadPoolExecutor() as pool:
        

        #collective_data=(pool.map(clean_data_to_csv(),all_links))
        # append data frame to CSV file
        pool.map(adding_one_line_into_csv(),all_links)
        # df.to_csv('appending.csv', mode='a', index=False, header=False)
        
    


#get_collective_data()


#MAIN TEST


#1: we get all the urls
list_of_urls =get_url_list()
#print(list_of_urls)
#success

#2: we retrieve data for each property in given url
#one_property_info = get_one_property_info(list_of_urls[0])#works but it takes only one url
#print(one_property_info)

#there will be a dict of properties data
properties_list=[]



#going through the list of urls
for url in list_of_urls:
    
    #we sanitize the single property
    #cancel the sanitization, need to sanitize function first

    sanitized_property_dict = clean_data_to_csv(get_one_property_info(url))
    
    #appending works
    #properties_list.append(get_one_property_info(url))

    #test adding one in csv
    adding_one_line_into_csv(get_one_property_info(url))


#Time spent inside the loop: 936.6282216000254 seconds.
print("Scraping completed")
print(f"\nTime spent inside the loop: {perf_counter() - start_time} seconds.")




#adding_one_line_into_csv(clean_data_to_csv(get_one_property_info("https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/10459437")))
# get_one_property_info("https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/10459437")



# if __name__ == "__main__":
#     start = perf_counter()
#     print(len(get_url_list()))
#     end=perf_counter()
#     pool_time = end-start
#     print("pool_time: ", pool_time)