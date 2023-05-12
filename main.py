import requests, re, json
from bs4 import BeautifulSoup

root_url = "https://www.immoweb.be/en/search/"
estate_types = ['house', 'apartment']
max_page = 1  # Set the maximum page number to 333

def get_url_list():
    for estate in estate_types:
        page = 1
        while page <= max_page:
            url = f"{root_url}{estate}/for-sale?countries=BE&page={page}&orderBy=relevance"
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')
            card_results = soup.find_all('article', class_='card--result')
            immo_links = []
            for article in card_results:
                link = article.find('a', class_='card__title-link')
                if link:
                    immo_links.append(link['href'])
            page += 1
    return(immo_links)

def get_immo_dict(immo_links):
    for i,link in enumerate(immo_links):
        req = requests.get(link)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        script_tags = soup.find_all('script')
        second_script = script_tags[1]
        script_content = second_script.string
        new_script_content = script_content.split('"classified": ')[1]
        new_new_cont = new_script_content.split(""",
                                    "customer": """)[0]
        dict1 = json.loads(new_new_cont)
        # print(type(dict1))
        # m = json.dumps(dict1, indent=4)
        return dict1

def replace_empty_with_none(dict_to_clean):
    for key, value in dict_to_clean.items():
        if isinstance(value, dict):
            replace_empty_with_none(value)
        elif isinstance(value, str) and not value:
            dict_to_clean[key] = None
    return dict_to_clean

print(replace_empty_with_none(get_immo_dict(get_url_list())))
print("Scraping completed.")