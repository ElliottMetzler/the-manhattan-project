import pandas as pd
from pandas import json_normalize
import requests
import json
import os
from quant_preprocess import query_and_preprocess_data
from quant_preprocess import query_and_reshape_long
from quant_preprocess import recode_long_data

params = {
    "api_key": "4F60666AD7F14FE49237DE1B9E2FB925",
    "type": "search",
    "sort_by": "best_seller",
}

OUTPUT_DIR = "data"
JSON_PATH = os.path.join(OUTPUT_DIR, "items.txt")


def load_ingredients():
    """Loads the list of ingredients to a list"""

    df = query_and_reshape_long()
    recoded = recode_long_data(df)
    summary = (
        recoded[["ingredient", "amount"]].groupby("ingredient").agg(["mean", "sum"])
    )
    return summary.index.values.tolist()


def get_item_jsons(params):
    """Loops though a list of ingredients and outputs a list of jsons."""

    json_list = []
    ingredients = load_ingredients()
    for i in ingredients:
        params["search_term"] = i
        result = requests.get("https://api.bluecartapi.com/request", params)
        json_list.append(json.dumps(result.json()))
    return json_list


def json_to_text(jsons, path):
    """Takes the list of jsons and writes them to a text file."""

    f = open(path, "w+")
    for i in jsons:
        f.write(i + "\n")
    f.close()


if __name__ == "__main__":

    jsons = get_item_jsons(params)
    json_to_text(jsons, JSON_PATH)
