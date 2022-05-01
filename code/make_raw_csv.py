from pandas import json_normalize
import requests
import pandas as pd
import os
import string

BASE_DIR = "data"
DATA_OUT_PATH = os.path.join(BASE_DIR, "header_complete_raw_data.csv")
INGREDIENTS_OUT_PATH = os.path.join(BASE_DIR, "ingredients.csv")
ALPHA = list(string.ascii_lowercase)
NUM = list(string.digits)
NUM.extend(ALPHA)
NUM.remove("0")
NUM.remove("8")


def create_raw_data(BASE_URL):
    """INSERT DOCSTRING"""

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
    """INSERT DOCSTRING"""

    response = requests.get(BASE_URL)
    response.raise_for_status()
    response_json = response.json()
    ingredients_frame = json_normalize(response_json["drinks"])

    return ingredients_frame


def create_data_onevariable(dataframe):
    """INSERT DOCSTRING"""

    dataframe["strIngredient1"] = ingredients["strIngredient1"].str.lower()
    dataframe.to_csv(INGREDIENTS_OUT_PATH, index=False, header=False)

    return


def create_data_complete(dataframe):
    """INSERT DOCSTRING"""

    dataframe.to_csv(DATA_OUT_PATH, index=False)

    return


if __name__ == "__main__":

    os.makedirs(BASE_DIR, exist_ok=True)

    raw_data = create_raw_data(
        "http://www.thecocktaildb.com/api/json/v1/1/search.php?f="
    )
    create_data_complete(raw_data)

    ingredients = create_ingredients_data(
        "http://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"
    )
    create_data_onevariable(ingredients)
