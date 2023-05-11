import requests, re, json
from bs4 import BeautifulSoup

root_url = "https://www.immoweb.be/en/classified/apartment/for-sale/deinze/9800/10560241"
req = requests.get(root_url)
print(req.status_code)
soup = BeautifulSoup(req.content, 'html.parser')

# house_info = soup.find_all('classified')
# print(house_info)


# house_info = soup.find('script')["window.dataLayer"]

# script_text = soup.find_all("script", "dataLayer")[0]
# print(script_text)
# for i in script_text:
#     print(i)
# json_data = json.loads(script_text[:script_text.find(";")])
# href_links = []

# for article in house_info:
#     print(article.get_text())
# #     link = article.find('a', class_='card__title-link')
#     if link:
#         href_links.append(link['href'])

# # for i,link in enumerate(href_links,1):
# #     print(i, link)


# # print(json_data)

# house_info = soup.find('script')["window.dataLayer"]
# house_info = soup.find_all('script')[1].string

# print(type(house_info))
# # Extract the JavaScript code from the script tag
# # javascript_code = house_info.string

# # Execute the JavaScript code to access window.dataLayer
# # data_layer = {}
# # exec(house_info, {}, data_layer)

# # Access the values in the window.dataLayer object
# # print((house_info).json())

# data_layer = {}
# exec(house_info, {}, data_layer)
# print(data_layer['data'])


script_tags = soup.find_all('script')

# Access the second script tag (index 1)
second_script = script_tags[1]

# Extract the content within the script tag
script_content = second_script.string

# # Remove leading/trailing whitespaces and semicolons
script_content = script_content.strip().rstrip(';').split("=")[1]

script_content = re.sub(r"\n", "", script_content)
# script_content = re.sub(r"\", "", script_content)
script_content = re.sub(r"^\s+", "", script_content)
# print(script_content)


# Parse the script content as JSON
# data_layer = json.loads(script_content)

# Access the list within the dataLayer
# info_list = data_layer[0]

with open("test4.json", "w") as f:
    json.dump(script_content, f)