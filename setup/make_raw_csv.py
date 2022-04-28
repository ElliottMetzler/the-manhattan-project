from bs4 import BeautifulSoup
from pandas import json_normalize
import requests
import pandas as pd
import os
import string
import json

if __name__ == "__main__":
    BASE_DIR = "data"
    CSV_PATH = os.path.join(BASE_DIR, "raw_data.csv")
    CSV_PATH1 = os.path.join(BASE_DIR, "complete_raw_data.csv")
    os.makedirs(BASE_DIR, exist_ok=True)
    

BASE_URL = ("http://www.thecocktaildb.com/api/json/v1/1/search.php?f=")

ALPHA = list(string.ascii_lowercase)

page_links = []

for n in ALPHA:
    url = '{}{}'.format(BASE_URL, n)
    page_links.append(url)
    
try1 = []
for url in page_links:
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()
    try1.append(response_json["drinks"])
    

normalize = json_normalize(try1)
df = pd.DataFrame(normalize)
raw_data = pd.DataFrame(df.stack().apply(pd.Series))

raw_data.to_csv(CSV_PATH)


BASE_URL2 = ("http://www.thecocktaildb.com/api/json/v1/1/search.php?f=")

NUM = list(string.digits)
NUM.extend(ALPHA)
NUM.remove("0")
NUM.remove("8")

page_links2 = []

for n in NUM:
    url2 = '{}{}'.format(BASE_URL2, n)
    page_links2.append(url2)
    
try2 = []
for url in page_links2:
    response1 = requests.get(url)
    response1.raise_for_status()
    response1_json = response1.json()
    try2.append(response1_json["drinks"])


normalize1 = json_normalize(try2)
df1 = pd.DataFrame(normalize1)
raw_data1 = pd.DataFrame(df1.stack().apply(pd.Series))

raw_data1.reset_index(drop=True, inplace=True)

raw_data1.to_csv(CSV_PATH1)