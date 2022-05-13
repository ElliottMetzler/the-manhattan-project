import pandas as pd
from pandas import json_normalize
import requests
import json
import os
from quant_preprocess import query_and_reshape_long
from quant_preprocess import recode_long_data
from prices_clean import load_best_match_batch

params = {"api_key": "INSERT_API_KEY", "type": "search"}

OUTPUT_DIR = "data"
JSON_PATH_BS = os.path.join(OUTPUT_DIR, "items_best_seller.txt")
JSON_PATH_BM = os.path.join(OUTPUT_DIR, "items_best_match.txt")


def load_ingredients():
    """Loads the list of ingredients to a list"""

    df = query_and_reshape_long()
    recoded = recode_long_data(df)
    summary = (
        recoded[["ingredient", "amount"]].groupby("ingredient").agg(["mean", "sum"])
    )
    return summary.index.values.tolist()


def get_item_jsons_best_seller(params):
    """Loops though a list of ingredients and outputs a list of jsons for best seller results."""

    json_list = []
    ingredients = load_ingredients()
    params["sort_by"] = "best_seller"
    for i in ingredients:
        params["search_term"] = i
        result = requests.get("https://api.bluecartapi.com/request", params)
        json_list.append(json.dumps(result.json()))
    return json_list


def get_item_jsons_best_match(params):
    """Loops though a list of ingredients and outputs a list of jsons for best match results."""

    json_list = []
    ingredients = load_best_match_batch()
    params["sort_by"] = "best_match"
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

    jsons_bs = get_item_jsons_best_seller(params)
    json_to_text(jsons_bs, JSON_PATH_BS)

    jsons_bm = get_item_jsons_best_match(params)
    json_to_text(jsons_bm, JSON_PATH_BM)
