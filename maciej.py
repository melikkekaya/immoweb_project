

import requests, re
from bs4 import BeautifulSoup

root_url = "https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page=1&orderBy=relevance"
req = requests.get(root_url)
print(req.status_code)
soup = BeautifulSoup(req.content, 'html.parser')

card_results = soup.findall('article', class='card--result')

href_links = []

for article in cardresults:
    link = article.find('a', class='card__title-link')
    if link:
        href_links.append(link['href'])

for i,link in enumerate(href_links,1):
    print(i, link)


#Need to import csv module
import csv
#TEMPORARY NAME
properties_list=[]




# Open a file in write mode.
with open('file.csv', 'w') as property:
    # Write all the dictionary keys in a file with commas separated.
    property.write(','.join(properties_list[0].keys()))
    property.write('\n') # Add a new line
    for row in properties_list:
        # Write the values in a row.
        property.write(','.join(str(x) for x in row.values()))
        #is it a blank space?
        #property.write('\n') # Add a new line



#locality,property_type,property_sub_type,price,sale_type,number_of_rooms,living_area,
#fully_equipped_kitchen,furnished,open_fire,terrace,garden,land_surface,land_plot_surface,facades
#swimming_pool,building_state



#Terrace/garden, specify area if yes

#with panda
import pandas

df = pandas.DataFrame(properties_list)
df.to_csv("property.csv", index = False)

import requests, re
from bs4 import BeautifulSoup

root_url = "https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page=1&orderBy=relevance"
req = requests.get(root_url)
print(req.status_code)
soup = BeautifulSoup(req.content, 'html.parser')

card_results = soup.findAll('article', class_='card--result')

href_links = []

for article in card_results:
    link = article.find('a', class_='card__title-link')
    if link:
        href_links.append(link['href'])

#for i,link in enumerate(href_links,1):
 #   print(i, link)

req = requests.get(href_links[0])
#print(href_links[0])
soup = BeautifulSoup(req.text,'html.parser')
print(soup)
temp_var = None
for element in soup.findAll('window.dataLayer'):
    print(element)
    break