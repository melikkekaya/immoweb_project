import requests, re, json, pandas
from bs4 import BeautifulSoup


root_url = "https://www.immoweb.be/en/classified/villa/for-sale/hotton/6990/10552972"

req = requests.get(root_url)
print(req.status_code)
soup = BeautifulSoup(req.text, 'html.parser')

script_tags = soup.find_all('script')
second_script = script_tags[1]

script_content = second_script.string

new_script_content = script_content.split('"classified": ')[1]
new_new_cont = new_script_content.split(""",
                                    "customer": """)[0]
dict1 = eval(new_new_cont)
print(type(dict1))

real_estate_info = {
        "id":dict1["id"],
        "type":dict1["type"]
}

m = json.dumps(dict1, indent=4)
print(m)
# with open("neeeee.json", "w") as f:
#         json.dump(dict1, f,indent=4)

