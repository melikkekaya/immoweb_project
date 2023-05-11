import requests, re
from bs4 import BeautifulSoup

root_url = "https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page=1&orderBy=relevance"
req = requests.get(root_url)
print(req.status_code)
soup = BeautifulSoup(req.content, 'html.parser')

card_results = soup.find_all('article', class_='card--result')

href_links = []

for article in card_results:
    link = article.find('a', class_='card__title-link')
    if link:
        href_links.append(link['href'])

for i,link in enumerate(href_links,1):
    print(i, link)