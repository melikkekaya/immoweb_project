import requests, re, json
from bs4 import BeautifulSoup

root_url = "https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page=1&orderBy=relevance"
req = requests.get(root_url)
print(req.status_code)
soup = BeautifulSoup(req.content, 'html.parser')

card_results = soup.findall('article', class_='card--result')

href_links = []

for article in card_results:
    link = article.find('a', class_='card__title-link')
    if link:
        href_links.append(link['href'])

#lists all the links
# for i,link in enumerate(href_links,1):
#     print(i, link)


#RETRIEVING INFO FROM EACH LINK
list_of_property_info = []

for link in href_links:


    request = requests.get(link)
    #retrieving info from each datalayer
    data = re.findall("window.dataLayer =(.+?);\n", request.text, re.S)
    #print(request.text)


    if data:
        list_of_property_info.append(json.loads(data[0]))


    # if ls:
    #     #first bracket for position in list, second for the classified(the property)
    #     #third bracket for property dict (info inside property)
    #     print(ls[0]['classified'])
# for property in list_of_property_info:
#     #[index in list][index of?][property is defined as classified][key of property dict]
#     print(list_of_property_info[0][0]["classified"])

new_prop_list =[]
for property in list_of_property_info:
    #print(f"THIS IS PROPERTY INFO : {property[0]['classified']}")
    new_prop_list.append(property[0]['classified'])

print(new_prop_list)
 

import pandas
#EXCEL USES ; AS DELIMITERS, THATS WHY IT WAS NOT WORKING LOL
df = pandas.DataFrame(new_prop_list)
df.to_csv("property7.csv", index = False, sep=";")