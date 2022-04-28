from bs4 import BeautifulSoup
import pandas as pd
from pandas import json_normalize
import requests
import os

if __name__ == "__main__":
    BASE_DIR = "data"
    CSV_PATH = os.path.join(BASE_DIR, "raw_data.csv")
    os.makedirs(BASE_DIR, exist_ok=True)
    
# Code for search by Alcoholic or not
url = "http://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Alcoholic"
response = requests.get(url)
response.raise_for_status()
response_json = response.json()

df1 = json_normalize(response_json["drinks"])


# Code for search by letter
url2 = "http://www.thecocktaildb.com/api/json/v1/1/search.php?f=b"
response2 = requests.get(url2)
response2.raise_for_status()
response2_json = response2.json()

df2 = json_normalize(response2_json["drinks"])


# Code for search by name
url3 = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s=bloody_mary"
response3 = requests.get(url3)
response3.raise_for_status()
response3_json = response3.json()

df3 = json_normalize(response3_json["drinks"])