import requests, re
from bs4 import BeautifulSoup

root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=relevance"
req = requests.get(root_url)
print(req.status_code)
soup = BeautifulSoup(req.content, 'html.parser')
print(soup.prettify())