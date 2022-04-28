from bs4 import BeautifulSoup
from pandas import json_normalize
import requests
import pandas as pd
import os
import string
import json

if __name__ == "__main__":
    BASE_DIR = "data"
    INGREDIENTS_PATH = os.path.join(BASE_DIR, "ingredients.csv")
    os.makedirs(BASE_DIR, exist_ok=True)


BASE_URL = ("http://www.thecocktaildb.com/api/json/v1/1/list.php?i=list")
response = requests.get(BASE_URL)
response.raise_for_status()
response_json = response.json()
ingredients_frame = json_normalize(response_json["drinks"])

ingredients_frame["strIngredient1"] = ingredients_frame["strIngredient1"].str.lower()

ingredients_frame.to_csv(INGREDIENTS_PATH, index=False)