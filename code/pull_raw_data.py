from pandas import json_normalize
import requests
import pandas as pd
import os
import string

BASE_DIR = "data"
DATA_OUT_PATH = os.path.join(BASE_DIR, "drinks_data_raw.csv")
INGREDIENTS_OUT_PATH = os.path.join(BASE_DIR, "ingredients_data_raw.csv")

COCKTAIL_KEY = "INSERT_API_KEY"

ALPHA = list(string.ascii_lowercase)
NUM = list(string.digits)
NUM.extend(ALPHA)
NUM.remove("0")
NUM.remove("8")


def create_raw_data(BASE_URL):
    """Takes a base url, creates a list of urls, then for each url it get drinks and returns a dataframe."""

    page_links = []

    for n in NUM:
        url = "{}{}".format(BASE_URL, n)
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

    return raw_data


def create_ingredients_data(BASE_URL):
    """Takes a base url and get the list of ingredients from it, then creates a dataframe."""

    response = requests.get(BASE_URL)
    response.raise_for_status()
    response_json = response.json()
    ingredients_frame = json_normalize(response_json["drinks"])
    ingredients_frame["strIngredient1"] = ingredients_frame[
        "strIngredient1"
    ].str.lower()

    return ingredients_frame


if __name__ == "__main__":

    os.makedirs(BASE_DIR, exist_ok=True)

    raw_data = create_raw_data(
        f"http://www.thecocktaildb.com/api/json/v2/{COCKTAIL_KEY}/search.php?f="
    )
    raw_data.to_csv(DATA_OUT_PATH, index=False)

    ingredients = create_ingredients_data(
        f"http://www.thecocktaildb.com/api/json/v2/{COCKTAIL_KEY}/list.php?i=list"
    )
    ingredients.to_csv(INGREDIENTS_OUT_PATH, index=False, header=False)
