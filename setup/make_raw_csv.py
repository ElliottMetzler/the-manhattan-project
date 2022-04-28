from pandas import json_normalize
import requests
import pandas as pd
import os
import string
import json

if __name__ == "__main__":
    BASE_DIR = "data"
    NO_HEADER_PATH = os.path.join(BASE_DIR, "no_header_complete_raw_data.csv")
    WITH_HEADER_PATH = os.path.join(BASE_DIR, "header_complete_raw_data.csv")
    os.makedirs(BASE_DIR, exist_ok=True)
    HEADER_PATH = os.path.join(BASE_DIR, "headers_only.csv")

BASE_URL = ("http://www.thecocktaildb.com/api/json/v1/1/search.php?f=")

ALPHA = list(string.ascii_lowercase)
NUM = list(string.digits)
NUM.extend(ALPHA)
NUM.remove("0")
NUM.remove("8")

page_links = []

for n in NUM:
    url = '{}{}'.format(BASE_URL, n)
    page_links.append(url)
    
list_of_pages = []
for url in page_links:
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()
    list_of_pages.append(response_json["drinks"])


normalize = json_normalize(list_of_pages)
df = pd.DataFrame(normalize)
raw_data = pd.DataFrame(df.stack().apply(pd.Series))

raw_data.reset_index(drop=True, inplace=True)

raw_data.to_csv(NO_HEADER_PATH, index=False, header=False)

raw_data.to_csv(WITH_HEADER_PATH, index=False)

headers = pd.DataFrame(raw_data.columns.values)

headers.to_csv(HEADER_PATH, header = ["column names"], index=False)