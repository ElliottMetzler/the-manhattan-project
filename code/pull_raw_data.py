from pandas import json_normalize
import requests
import pandas as pd
import os
import string

BASE_DIR = "data"
DATA_OUT_PATH = os.path.join(BASE_DIR, "drinks_data_raw.csv")
INGREDIENTS_OUT_PATH = os.path.join(BASE_DIR, "ingredients_data_raw.csv")
ALPHA = list(string.ascii_lowercase)
NUM = list(string.digits)
NUM.extend(ALPHA)
NUM.remove("0")
NUM.remove("8")


def create_raw_data(BASE_URL):
    """Creates a url for each character of the NUM list and append the url to a list. Go through the list of urls and for each, requests the drinks, check if the url exists, returns a JSON response, normalize it by opening the results whenever it reads "drinks", then attach it to a list. Goes through list of results and separate the appended JSONs into separate rows. Creates a dataframe with the list. Split each row relating to one JSON result into separate drinks, then creates a new dataframe. Remove the JSON result index from the dataframe and give new index for all drinks."""

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
    """Sends a request to search all the ingredients in the database. Return a JSON with the results. Normalize the JSON by opening the file whenever it reads "drinks". Creates a dataframe with the results. Lowercase all the ingredient's names. Return the finished dataframe"""

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
        "http://www.thecocktaildb.com/api/json/v1/1/search.php?f="
    )
    raw_data.to_csv(DATA_OUT_PATH, index=False)

    ingredients = create_ingredients_data(
        "http://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"
    )
    ingredients.to_csv(INGREDIENTS_OUT_PATH, index=False, header=False)
