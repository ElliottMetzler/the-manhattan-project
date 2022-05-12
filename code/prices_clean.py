import pandas as pd
import numpy as np
import json
import os
from quant_preprocess import query_and_reshape_long
from quant_preprocess import recode_long_data

# not on walmart:
# cherry heering, absinthe, mix, baileys,
# port, zima, ice, bourbon, cognac, galliano,
# ricard, fruit, sweet and sour
# off estimates: butter,


measurements = ["oz", "ml", "lb", "l", "ounces", "g"]
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]
DIR = "data"
IN_FILE_PATH_BS = os.path.join(DIR, "items_best_seller.txt")
IN_FILE_PATH_BM = os.path.join(DIR, "items_best_match.txt")
OUTPUT_PATH = os.path.join(DIR, "ingredient_prices_raw.csv")


def load_ingredients():

    df = query_and_reshape_long()
    recoded = recode_long_data(df)
    summary = (
        recoded[["ingredient", "amount"]].groupby("ingredient").agg(["mean", "sum"])
    )
    return summary.index.values.tolist()


def load_best_match_batch():

    l1 = load_ingredients()
    rough_dict = get_products_best_seller()
    best_seller_dict = drop_bad_products_bs(rough_dict)
    df = set_index(best_seller_dict)
    df = drop_wrong_item(df)
    l2 = df.columns.values.tolist()
    best_match_batch = set(l1).difference(set(l2))
    return list(best_match_batch)


def read_txt_as_json(file):

    j_list = []
    with open(file) as text:
        json_list = [line.rstrip("\n") for line in text]
        for j in json_list:
            j_list.append(json.loads(j))
        return j_list


def split(word):

    return [char for char in word]


def drop_wrong_item(df):

    if len(df.iloc[0]) == 41:
        df.drop("sherry", axis=1, inplace=True)
        df.drop("sugar", axis=1, inplace=True)
        df.drop("ricard", axis=1, inplace=True)

    elif len(df.iloc[0]) == 42:
        df.drop("tonic water", axis=1, inplace=True)
        df.drop("butter", axis=1, inplace=True)
        df.drop("cornstarch", axis=1, inplace=True)
        df.drop("cognac", axis=1, inplace=True)
        df.drop("flavored rum", axis=1, inplace=True)
        df.drop("flavored vodka", axis=1, inplace=True)
        df.drop("fruit", axis=1, inplace=True)
        df.drop("ice cream", axis=1, inplace=True)
        df.drop("fruit juice", axis=1, inplace=True)
        df.drop("grain alcohol", axis=1, inplace=True)
        df.drop("hot sauce", axis=1, inplace=True)
        df.drop("milk", axis=1, inplace=True)
        df.drop("whiskey", axis=1, inplace=True)
        df.drop("sugar", axis=1, inplace=True)
        df.drop("spice", axis=1, inplace=True)
        df.drop("soda", axis=1, inplace=True)
        df.drop("sherry", axis=1, inplace=True)
        df.drop("prosecco", axis=1, inplace=True)
        df.drop("olive brine", axis=1, inplace=True)
        df.drop("nut", axis=1, inplace=True)
        df.drop("mix", axis=1, inplace=True)
        df.drop("herb", axis=1, inplace=True)
        df.drop("sarsaparilla", axis=1, inplace=True)
        df.drop("ice", axis=1, inplace=True)
        df.drop("dry vermouth", axis=1, inplace=True)
        df.drop("water", axis=1, inplace=True)
        df.drop("erin cream", axis=1, inplace=True)
    return df


def get_products_best_seller():

    j_list = read_txt_as_json(IN_FILE_PATH_BS)
    product_dict = {}
    for j in j_list:
        amount_temp = []
        units_temp = []
        price_temp = []
        desc_temp = []
        ingredient = j["request_parameters"]["search_term"]
        key = ingredient
        product_dict.setdefault(key, [])
        a = "search_results"
        if a not in j:
            continue
        else:
            results = j["search_results"]
            i = 0
            for r in results[0:5]:
                n_temp = []
                m_temp = []
                title = r["product"]["title"]
                chars = split(title)
                title_list = title.split()
                price = r["offers"]["primary"]["price"]
                price_temp.append(price)
                desc_temp.append(title)
                for c in reversed(range(len(chars))):
                    if (chars[c] not in ("".join(numbers))) and (len(n_temp) > 0):
                        break
                    if c == 0:
                        amount_temp.append(np.nan)
                    if chars[c] not in ("".join(numbers)):
                        continue
                    else:
                        for n in numbers:
                            if n == chars[c]:
                                n_temp.append(chars[c])
                amount_temp.append(("".join(n_temp))[::-1])
                for t in reversed(range(len(title_list))):
                    for m in measurements:
                        if len(m_temp) > 0:
                            break
                        if t == 0:
                            units_temp.append(np.nan)
                        if m not in (title_list[t].lower()):
                            continue
                        else:
                            m_temp.append(m)
                units_temp.append("".join(m_temp))
            product_dict[key].append(price_temp)
            product_dict[key].append(amount_temp)
            product_dict[key].append(units_temp)
            product_dict[key].append(desc_temp)
    return product_dict


def get_products_best_match():

    j_list = read_txt_as_json(IN_FILE_PATH_BM)
    product_dict = {}
    for j in j_list:
        amount_temp = []
        units_temp = []
        price_temp = []
        desc_temp = []
        ingredient = j["request_parameters"]["search_term"]
        key = ingredient
        product_dict.setdefault(key, [])
        a = "search_results"
        if a not in j:
            continue
        else:
            results = j["search_results"]
            i = 0
            for r in results[0:2]:
                n_temp = []
                m_temp = []
                title = r["product"]["title"]
                chars = split(title)
                title_list = title.split()
                price = r["offers"]["primary"]["price"]
                price_temp.append(price)
                desc_temp.append(title)
                for c in reversed(range(len(chars))):
                    if (chars[c] not in ("".join(numbers))) and (len(n_temp) > 0):
                        break
                    if c == 0:
                        amount_temp.append(np.nan)
                    if chars[c] not in ("".join(numbers)):
                        continue
                    else:
                        for n in numbers:
                            if n == chars[c]:
                                n_temp.append(chars[c])
                amount_temp.append(("".join(n_temp))[::-1])
                for t in reversed(range(len(title_list))):
                    for m in measurements:
                        if len(m_temp) > 0:
                            break
                        if t == 0:
                            units_temp.append(np.nan)
                        if m not in (title_list[t].lower()):
                            continue
                        else:
                            m_temp.append(m)
                units_temp.append("".join(m_temp))
            product_dict[key].append(price_temp)
            product_dict[key].append(amount_temp)
            product_dict[key].append(units_temp)
            product_dict[key].append(desc_temp)
    return product_dict


def drop_bad_products(product_dict):

    ingredients = list(product_dict.keys())
    for i in ingredients:
        if len(product_dict[i]) == 0:
            del product_dict[i]
        else:
            for n in range(0, 3):
                if len(product_dict[i][n]) != len(product_dict[i][0]):
                    del product_dict[i]
                    break
    return product_dict


def set_index(dictionary):
    index = ["price", "measurement", "units", "description"]
    df = pd.DataFrame(dictionary)
    df["index"] = index
    df = df.set_index("index")
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
            if u == "lb":
                price.append(p / (m * 16))
                continue
            if u == "ounces":
                price.append(p / m)
                continue
            if u == "oz":
                if m == 24:
                    price.append(p / (12 * 24))
                else:
                    price.append(p / m)
                continue
            if ((u == "ml") and (m == 750)) or ((u == "ml") and (m == 375)):
                price.append(p / (m * 0.033814))
                continue
            if (u == "l") and (m <= 2):
                price.append(p / (m * 33.814))
                continue
            else:
                continue
        if len(price) > 0:
            a[i] = sum(price) / len(price)
        else:
            a[i] = np.nan
    return pd.DataFrame(a, index=[0])


def merge_results(df_bs, df_bm):
    dfs = [df_bs, df_bm]
    price_data = pd.concat(dfs)
    l1 = load_ingredients()
    l2 = price_data.columns.values.tolist()
    rest = list(set(l1).difference(set(l2)))
    rest_df = pd.DataFrame(columns=rest)
    price_data = pd.concat([price_data, rest_df], axis=1)
    return price_data


def to_csv(df):
    index = ["best_seller", "best_match"]
    df["index"] = index
    df.set_index("index", inplace=True, drop=True)
    data = df.mean(axis=0, skipna=True)
    data.to_csv(OUTPUT_PATH)


if __name__ == "__main__":
    os.makedirs(DIR, exist_ok=True)
    d_bm = get_products_best_match()
    d_bm = drop_bad_products(d_bm)
    df_bm = set_index(d_bm)
    df_bm = drop_wrong_item(df_bm)
    df_bm = convert_prices(df_bm)
    d_bs = get_products_best_seller()
    d_bs = drop_bad_products(d_bs)
    df_bs = set_index(d_bs)
    df_bs = drop_wrong_item(df_bs)
    df_bs = convert_prices(df_bs)
    df = merge_results(df_bm, df_bs)
    to_csv(df)
