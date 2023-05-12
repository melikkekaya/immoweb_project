import requests, re, json, csv, certifi
import pandas as pd
from bs4 import BeautifulSoup


root_url = "https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/10459437"

req = requests.get(root_url)
print(req.status_code)
soup = BeautifulSoup(req.content, 'html.parser')

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

# m = json.dumps(dict1, indent=4)
# print(m)

# for key, value in dict1.items():
#     print(f"{key} ----> {value}")

# with open("test1.json", "w") as f:
#       json.dump(dict1, f,indent=4)

# import pandas as pd
# df = pd.read_json('test1.json')
# df.to_csv('test1.csv', index = None)


# with open('test3.csv', 'w') as f:
#     for key in dict1.keys():
#         f.write("%s,%s\n"%(key,dict1[key]))

csv_columns = [key for key in dict1.keys()]
# print (csv_columns)

# dict_data = [
# {'No': 1, 'Name': 'Alex', 'Country': 'India'},
# {'No': 2, 'Name': 'Ben', 'Country': 'USA'},
# {'No': 3, 'Name': 'Shri Ram', 'Country': 'India'},
# {'No': 4, 'Name': 'Smith', 'Country': 'USA'},
# {'No': 5, 'Name': 'Yuva Raj', 'Country': 'India'},
# ]
# csv_file = "TEST.csv"
# try:
#     with open(csv_file, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
#         for data in dict1:
#             writer.writerow(data)
# except IOError:
#     print("I/O error")

# with open('test5.csv', 'w') as f:
#         writer = csv.DictWriter(f, fieldnames=csv_columns)
#         writer.writeheader()
#         for key in dict1.keys():
#                 f.write(str(dict1[key]))

output_file = 'output2.csv'

# Open the file in write mode and create a CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    for key, value in dict1.items():
        print(key, "-------", value)
        # if type(details) is str:
        #         csvfile.write(str(details))
        # if type(details) is dict:
        #         writer.writerow({**details})
