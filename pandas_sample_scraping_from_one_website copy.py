import requests, re, json, csv, certifi
import pandas as pd
from bs4 import BeautifulSoup

root_url = "https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/10459437"
req = requests.get(root_url)
print(req.status_code)

read_html_houses = pd.read_html(req.text)
data_frame_houses = pd.concat(read_html_houses)

print(data_frame_houses)
# keys = data_frame_houses.iloc[:,0]
# values = data_frame_houses.iloc[:,1]

# output_file = "aaaaaaa1.csv"
# with open(output_file, 'w', newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=keys)
#     writer.writeheader()
# with open(output_file, 'a') as csvfile:
#     writer_object = csv.writer(csvfile)
#     writer_object.writerow(values)
