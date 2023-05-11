import requests
from bs4 import BeautifulSoup
"house/for-sale?countries=BE&priceType=SALE_PRICE&page=1&orderBy=relevance"
"https://www.immoweb.be/en/search/house/for-sale?countries=BE&priceType=SALE_PRICE&page=333&orderBy=relevance"
root_url = "https://www.immoweb.be/en/search/"
estate_types = ['house', 'apartment']
max_page = 333  # Set the maximum page number to 333
immo_link = []
for estate in estate_types:
    page = 1
    while page <= max_page:
        url = f"{root_url}{estate}/for-sale?countries=BE&page={page}&orderBy=relevance"
        req = requests.get(url)
        print("Page: ", page)
        print("Status Code:", req.status_code)

        soup = BeautifulSoup(req.content, 'html.parser')
        card_results = soup.find_all('article', class_='card--result')

        href_links = []

        for article in card_results:
            link = article.find('a', class_='card__title-link')
            if link:
                href_links.append(link['href'])

        for i, link in enumerate(href_links, 1):
            immo_link = immo_link.append(link)
            print(i, link)


        page += 1

print("Scraping completed.")