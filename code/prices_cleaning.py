import pandas as pd
from pandas import json_normalize
import requests
import json
import csv
import os
import re
from quant_preprocess import query_and_preprocess_data
from quant_preprocess import query_and_reshape_long
from quant_preprocess import recode_long_data


# if the measurement is 750, its in ml
# if the measurement is 12, its in oz

measurements = ["oz", "ml", "lb", "l", "ounces", "g"]
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]
IN_FILE_PATH = os.path.join("..//data", "items.txt")
OUTPUT_DIR = "data"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "ingredient_prices.csv")


def load_ingredients():

    df = query_and_reshape_long()
    recoded = recode_long_data(df)
    summary = (
        recoded[["ingredient", "amount"]].groupby("ingredient").agg(["mean", "sum"])
    )
    return summary.index.values.tolist()


def read_txt_as_json():

    j_list = []
    with open("..//data//item_jsons.txt") as text:
        json_list = [line.rstrip("\n") for line in text]
        for j in json_list:
            j_list.append(json.loads(j))
        return j_list


def split(word):

    return [char for char in word]


def set_index(product_dict):

    index = ["price", "measurement", "units", "description"]
    df = pd.DataFrame(product_dict)
    df["index"] = index
    df.set_index("index")
    return df


def get_product_info():

    j_list = read_txt_as_json()
    product_dict = {}
    for j in j_list:
    # iterating through each json
        amount_temp = []
        units_temp = []
        price_temp = []
        desc_temp = []
        ingredient = j["request_parameters"]["search_term"]
        product_dict.setdefault(ingredient, [])
        if "search_results" not in j:
            continue
        else:
            results = j["search_results"]
            i = 0
            for r in results[0:5]:
            # I decided to pick the first 5 products, still unsure if I'll stick with it
                n_temp = []
                m_temp = []
                title = r["product"]["title"]
                chars = split(title)
                title_list = title.split()
                price = r["offers"]["primary"]["price"]
                price_temp.append(price)
                desc_temp.append(title)
                for c in reversed(range(len(chars))):
                # Going through a list in reverse of individual characters in the description
                # This was the best way to pull out the measurements
                    if (chars[c] not in ("".join(numbers))) and (len(n_temp) > 0):
                        break
                    if c == 0:
                        amount_temp.append("NA")
                    if chars[c] not in ("".join(numbers)):
                        continue
                    else:
                        for n in numbers:
                            if n == chars[c]:
                                n_temp.append(chars[c])
                amount_temp.append(("".join(n_temp))[::-1])
                for t in reversed(range(len(title_list))):
                # Going through the list in reverse of words in the description
                # This is actually really bad, I'm trying to fix it
                    for m in measurements:
                        if len(m_temp) > 0:
                            break
                        if t == 0:
                            units_temp.append("NA")
                        if m not in (title_list[t].lower()):
                            continue
                        else:
                            m_temp.append(m)
                units_temp.append(m_temp)
            product_dict[ingredient].append(price_temp)
            product_dict[ingredient].append(amount_temp)
            product_dict[ingredient].append(units_temp)
            product_dict[ingredient].append(desc_temp)
    return product_dict


def drop_bad_products(product_dict):

    ingredients = load_ingredients()
    for i in ingredients:
        if len(product_dict[i]) == 0:
            del product_dict[i]
        else:
            for n in range(0, 3):
                if len(product_dict[i][n]) != 5:
                    del product_dict[i]
                    break
    return set_idex(product_dict)


def to_csv(df, path):

    df.to_csv(path)


if __name__ == "__main__":

    os.makedirs(OUT_DIR, exist_ok=True)
    product_dict = get_product_info()
    product_df = drop_bad_products(product_dict)
    to_csv(product_df, OUT_FILE_PATH)
