import requests, re, json
from bs4 import BeautifulSoup
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
import pandas
session = requests.Session()


root_url = "https://www.immoweb.be/en/search/"
estate_types = ['house', 'apartment']
max_page = 333  # Set the maximum page number to 333

def get_url_list(estate):
    immo_links = []
    page = 1
    #max_page
    while page <= max_page:
        url = f"{root_url}{estate_types[0]}/for-sale?countries=BE&page={page}&orderBy=relevance"
        req = session.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        card_results = soup.find_all('article', class_='card--result')
        for article in card_results:
            link = article.find('a', class_='card__title-link')
            if link:
                immo_links.append(link['href'])
                
        
        
        page += 1
    print("Retrieving urls completed")
       
    return immo_links

def get_immo_dict(link):
    req = session.get(link)
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




#MAIN 
start_time = perf_counter()
#official
# immo_links = []
# with ThreadPoolExecutor() as executor:
#     for estate in estate_types:
#         immo_links.extend(executor.submit(get_url_list, estate).result())


# #print(immo_links[0])
# immo_dicts = []
# with ThreadPoolExecutor() as executor:
#     for link in immo_links:
#         result = executor.submit(get_immo_dict, link).result()
#         result = replace_empty_with_none(result)
#         immo_dicts.append(result)
#         print(link)

#TESTS MAIN
list_of_property_info = []
list_of_urls = get_url_list('house')
for link in list_of_urls:


    request = session.get(link)
    #retrieving info from each datalayer
    data = re.findall("window.dataLayer =(.+?);\n", request.text, re.S)
    #print(request.text)


    if data:
        list_of_property_info.append(json.loads(data[0]))
print("Phase 2 completed")

new_prop_list =[]
for property in list_of_property_info:
    #print(f"THIS IS PROPERTY INFO : {property[0]['classified']}")
    new_prop_list.append(property[0]['classified'])

#print(new_prop_list)

# with open('immo_dump.json', 'w') as outfile:
#     json.dump(immo_dicts, outfile, indent=4)



# import pandas
# #EXCEL USES ; AS DELIMITERS, THATS WHY IT WAS NOT WORKING LOL
df = pandas.DataFrame(new_prop_list)
df.to_csv("20_pages_new_prop.csv", index = False, sep=";")

print("Scraping completed.")
print(f"\nTime spent inside the loop: {perf_counter() - start_time} seconds.")

#Une exception s'est produite : KeyError
# 'classified'
#   File "C:\Users\Maciej\workspace\immoweb\immoweb_project\maciej.py", line 94, in <module>
#     new_prop_list.append(property[0]['classified'])
#                          ~~~~~~~~~~~^^^^^^^^^^^^^^
# KeyError: 'classified'

# len(new_prop_list)4765
#20 pages Time spent inside the loop: 91.2587817000458 seconds.
#20 pages with formatting list Time spent inside the loop: 84.99270110001089 seconds
#WITHOUT SESSION Time spent inside the loop: 736.7734905999969 seconds.
#WITH SESSION Time spent inside the loop: 715.2603850000014 seconds.
#WITH POOL Time spent inside the loop: 859.5627824999974 seconds.

card_results = soup.find_all('article', class_='card--result')

for article in card_results:
    link = article.find('a', class_='card__title-link')
    if link:
        href_links.append(link['href'])

#lists all the links
# for i,link in enumerate(href_links,1):
#     print(i, link)



# #print(immo_links[0])
# immo_dicts = []
# with ThreadPoolExecutor() as executor:
#     for link in immo_links:
#         result = executor.submit(get_immo_dict, link).result()
#         result = replace_empty_with_none(result)
#         immo_dicts.append(result)
#         print(link)

#TESTS MAIN
list_of_property_info = []
list_of_urls = get_url_list('house')
for link in list_of_urls:


    request = session.get(link)
    #retrieving info from each datalayer
    data = re.findall("window.dataLayer =(.+?);\n", request.text, re.S)
    #print(request.text)


    if data:
        list_of_property_info.append(json.loads(data[0]))
print("Phase 2 completed")

#RETRIEVING INFO FROM EACH LINK
# list_of_property_info = []

# for link in immo_link:


#     request = session.get(link)
#     #retrieving info from each datalayer
#     data = re.findall("window.dataLayer =(.+?);\n", request.text, re.S)
#     #print(request.text)


#     if data:
#         list_of_property_info.append(json.loads(data[0]))


# #     # if ls:
# #     #     #first bracket for position in list, second for the classified(the property)
# #     #     #third bracket for property dict (info inside property)
# #     #     print(ls[0]['classified'])
# # # for property in list_of_property_info:
# # #     #[index in list][index of?][property is defined as classified][key of property dict]
# # #     print(list_of_property_info[0][0]["classified"])


# new_prop_list =[]
# for property in list_of_property_info:
#     #print(f"THIS IS PROPERTY INFO : {property[0]['classified']}")
#     new_prop_list.append(property[0]['classified'])

#print(new_prop_list)

# with open('immo_dump.json', 'w') as outfile:
#     json.dump(immo_dicts, outfile, indent=4)


# import pandas
# #EXCEL USES ; AS DELIMITERS, THATS WHY IT WAS NOT WORKING LOL
df = pandas.DataFrame(new_prop_list)
df.to_csv("20_pages_new_prop.csv", index = False, sep=";")

print("Scraping completed.")
print(f"\nTime spent inside the loop: {perf_counter() - start_time} seconds.")

#Une exception s'est produite : KeyError
# 'classified'
#   File "C:\Users\Maciej\workspace\immoweb\immoweb_project\maciej.py", line 94, in <module>
#     new_prop_list.append(property[0]['classified'])
#                          ~~~~~~~~~~~^^^^^^^^^^^^^^
# KeyError: 'classified'

# len(new_prop_list)4765
#20 pages Time spent inside the loop: 91.2587817000458 seconds.
#20 pages with formatting list Time spent inside the loop: 84.99270110001089 seconds
#WITHOUT SESSION Time spent inside the loop: 736.7734905999969 seconds.
#WITH SESSION Time spent inside the loop: 715.2603850000014 seconds.
#WITH POOL Time spent inside the loop: 859.5627824999974 seconds.




#lists all the links
# for i,link in enumerate(href_links,1):
#     print(i, link)


#RETRIEVING INFO FROM EACH LINK
# list_of_property_info = []

# for link in immo_link:


#     request = session.get(link)
#     #retrieving info from each datalayer
#     data = re.findall("window.dataLayer =(.+?);\n", request.text, re.S)
#     #print(request.text)


#     if data:
#         list_of_property_info.append(json.loads(data[0]))


# #     # if ls:
# #     #     #first bracket for position in list, second for the classified(the property)
# #     #     #third bracket for property dict (info inside property)
# #     #     print(ls[0]['classified'])
# # # for property in list_of_property_info:
# # #     #[index in list][index of?][property is defined as classified][key of property dict]
# # #     print(list_of_property_info[0][0]["classified"])

# new_prop_list =[]
# for property in list_of_property_info:
#     #print(f"THIS IS PROPERTY INFO : {property[0]['classified']}")
#     new_prop_list.append(property[0]['classified'])

# # print(new_prop_list)
 


# # print(new_prop_list)
 

# import pandas
# #EXCEL USES ; AS DELIMITERS, THATS WHY IT WAS NOT WORKING LOL
# df = pandas.DataFrame(new_prop_list)
# df.to_csv("property.csv", index = False, sep=";")
