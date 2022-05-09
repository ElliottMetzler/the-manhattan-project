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


measurements = ["oz", "ml", "lb", "l", "ounces", "g"]
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9","0", "."]
IN_FILE_PATH = os.path.join("..//data", "items.txt")
OUTPUT_DIR = "data"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'ingredient_prices.csv')


def load_ingredients():

    df = query_and_reshape_long()
    recoded = recode_long_data(df)
    summary = (
        recoded[["ingredient", "amount"]].groupby("ingredient").agg(["mean", "sum"])
    )
    return summary.index.values.tolist()


def read_txt_as_json():

    j_list = []
    with open(IN_FILE_PATH) as text:
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


def get_products_best_seller():

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


def get_products_best_match():

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
        if (len(product_dict[i]) == 0):
            del product_dict[i]
        else:
            for n in range(0,3):
                if (len(product_dict[i][n]) !=5):
                    del product_dict[i]
                    break
    return product_dict


def set_index(dictionary):
    index = ['price', 'measurement', 'units', 'description']
    df = pd.DataFrame(dictionary)
    df['index'] = index
    df = df.set_index('index')
    return df


def load_best_match_batch():

    l1 = load_ingredients()
    rough_dict = get_products_best_seller()
    best_seller_dict = drop_bad_products(rough_dict)
    df = set_index(best_seller_dict)
    df = drop_wrong_item(df)
    l2 = df.columns.values.tolist()
    best_match_batch = set(l1).difference(set(l2))
    return list(best_match_batch)


def drop_wrong_item(df):

    df.drop("tonic water", axis=1, inplace= True)
    df.drop("butter", axis=1, inplace= True)
    df.drop("cornstarch", axis=1, inplace= True)
    df.drop("cognac", axis=1, inplace= True)
    df.drop("flavored rum", axis=1, inplace= True)
    df.drop("flavored vodka", axis=1, inplace= True)
    df.drop("fruit", axis=1, inplace= True)
    df.drop("ice cream", axis=1, inplace= True)
    df.drop("fruit juice", axis=1, inplace= True)
    df.drop("grain alcohol", axis=1, inplace= True)
    df.drop("hot sauce", axis=1, inplace= True)
    df.drop("milk", axis=1, inplace= True)
    df.drop("whiskey", axis=1, inplace= True)
    df.drop("sugar", axis=1, inplace= True)
    df.drop("spice", axis=1, inplace= True)
    df.drop("soda", axis=1, inplace= True)
    df.drop("sherry", axis=1, inplace= True)
    df.drop("prosecco", axis=1, inplace= True)
    df.drop("olive brine", axis=1, inplace= True)
    df.drop("nut", axis=1, inplace= True)
    df.drop("mix", axis=1, inplace= True)
    df.drop("herb", axis=1, inplace=True)
    df.drop("sarsaparilla", axis=1, inplace=True)
    df.drop("ice", axis=1, inplace=True)
    df.drop("dry vermouth", axis=1, inplace=True)
    df.drop("water", axis=1, inplace=True)
    df.drop("erin cream", axis=1, inplace= True)


    return df


def convert_prices(data):
    ingreds = data.columns.values.tolist()
    a = {}
    for i in ingreds:
        a.setdefault(i, [])
        p = []
        m = []
        u = []
        for n in range(len(data.iloc[0][i])):
            p.append(float(data.iloc[0][i][n]))
            m.append(float(data.iloc[1][i][n]))
            u.append(data.iloc[2][i][n])
        a[i].append(p)
        a[i].append(m)
        a[i].append(u)
    df = pd.DataFrame(a)
    ingreds = df.columns.values.tolist()
    for i in ingreds:
        price = []
        average = []
        for n in range(len(data.iloc[0][i])):
            p = df.iloc[0][i][n]
            m = df.iloc[1][i][n]
            u = df.iloc[2][i][n]
            if u == "ounces":
                price.append(p/m)
                continue
            if u == "oz":
                price.append(p/m)
                continue
            if u == "ml":
                price.append(p/(m*0.033814))
                continue
            if (u  == "l") and (m <= 2):
                price.append(p/(m*33.814))
                continue
            else:
                continue
        a[i] = (sum(price)/len(price))
    return pd.DataFrame(a, index=[0])





if __name__ == "__main__":

    os.makedirs(OUT_DIR, exist_ok=True)
    product_dict_bs = get_product_best_seller()
    product_dict_bs = drop_bad_products(product_dict)
    df1 = set_index(product_dict_bs)
    df1 = drop_wrong_item(df1)
    to_csv(product_df, OUT_FILE_PATH)
