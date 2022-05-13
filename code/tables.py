import pandas as pd
import numpy as np
from database import engine
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
import subprocess
from ingredient_map import create_ingredient_map
import quant_preprocess as qp
import os
import dataframe_image as dfi


INPUT_PATH = os.path.join("data", "ingredient_prices_clean.csv")
TABLE_DIR = "tables"
FIGURE_DIR = "figures"
ABV_DATA = os.path.join("data", "ABV_data.csv")



liquors = ["brandy","gin","tequila","vodka","whiskey","flavored rum","flavored vodka","cognac","bourbon","rum","scotch","grain alcohol"]




def save_plot(figure_obj, output_directory, output_file_name):
    """Function takes in a figure, the output directory and file name and saves the figure"""

    path = os.path.join(output_directory, output_file_name)
    figure_obj.savefig(path)

def create_dummies():
    """"Creates dummy variables for ingredients"""

    df = qp.query_and_preprocess_data()
    headers = df.columns[1:]
    d = {'strdrink': df['strdrink'].values.tolist()}
    for e in range(0, len(headers)):
        d[headers[e]] = (df[str(headers[e])] > 0).astype(int).values.tolist()
    return pd.DataFrame.from_dict(d)


def price_and_abv_preprocessed():
    """Function combines the cocktails, prices, and abv data to prepare it for analysis"""

    ABV_DATA = os.path.join("data", "ABV_data.csv")
    df = qp.query_and_reshape_long()
    recoded = qp.recode_long_data(df)

    ingredient_prices = qp.query_ingredient_prices()
    abv_data = pd.read_csv(ABV_DATA)

    combined = (
        recoded
        .merge(ingredient_prices, how = "left", on = "ingredient")
        .merge(abv_data, how = "left", on = "ingredient")
        .fillna(0)
        .assign(
            ounces_alcohol = lambda df_: df_["amount"] * df_["abv_percent"])
        .groupby("strdrink")
        .agg({
            "ingredient":"count",
            "amount": "sum",
            "price":"sum",
            "ounces_alcohol": "sum"})
        .assign(
            weighted_abv = lambda df_: df_["ounces_alcohol"] / df_["amount"],
            oz_alc_per_dollar = lambda df_: df_["ounces_alcohol"] / df_["price"])
        .rename(columns  = {
            "ingredient" : "num_ingredients",
            "amount": "total_ounces",
            "price" : "cost"
            })
        )

    return combined



def ols_model():

    data = drop_all_zero_dummies()
    df = price_and_abv_preprocessed()
    ols_model = data.merge(df,how="left",on="strdrink")

    return ols_model



def summmary_of_oz():
    """"Creates summary table for ingredients in ounces"""

    df = qp.query_and_preprocess_data()
    df = df.describe().transpose().sort_values('mean',
                                ascending = False).head(10)
    df = df[["mean"]]
    return df




def summary_of_usage():

    os.makedirs(TABLE_DIR, exist_ok=True)

    filename = os.path.join(TABLE_DIR,'usage.tex')
    pdffile = os.path.join(TABLE_DIR, 'usage.pdf')
    outname = os.path.join(TABLE_DIR, 'usage.png')

    dum_df = create_dummies()
    data = dum_df.describe().transpose().sort_values('mean',
                                    ascending=False).head(10)
    data = data[["mean"]]
    data = data.rename(columns={"mean":"Proportion of Drinks"})
    data.index.name = "Ingredient"

    dfi.export(data,(os.path.join(TABLE_DIR, "usage.png")))

def get_amount_table():


    df = qp.query_data()
    ingred_cols = qp.get_cols_list(df, "stringredient")
    measure_cols = qp.get_cols_list(df, "strmeasure")
    df[ingred_cols] = qp.cols_to_lower(df, ingred_cols)
    ingredient_long = qp.shape_data_long(
            df, ingred_cols, "stringredient", "", "ingredient"
        )
    measure_long = qp.shape_data_long(df, measure_cols, "strmeasure", "_clean", "amount")
    combined_long = qp.merge_long(ingredient_long, measure_long)
    ingredient_dict = qp.create_ingredient_map()
    recoded_long = qp.recode_ingredients(combined_long, ingredient_dict)
    combined_wide = qp.pivot_wide(recoded_long)
    return combined_wide


def drop_big_drinks():


    df = get_amount_table()
    df = df.set_index("strdrink")
    df = df.transpose()
    for d in df:
        if (df.sum(axis=0)[d] < 2.5) or (df.sum(axis=0)[d] > 15):
            df = df.drop(d,axis=1)
    return df.columns.values.tolist()



def number_of_ingredients():

    ingreds = []
    drinks = drop_big_drinks()
    data = create_dummies()
    data = data.set_index("strdrink")
    data = data.transpose()[drinks]
    return data.sum(axis=0).tolist()


def prices_list():

    df_prices = pd.read_csv(INPUT_PATH, header=None)
    df_prices = df_prices.sort_values(0, ascending=True)
    df_prices = df_prices.transpose()
    prices = df_prices.loc[1].values.tolist()
    return prices



def combine_prices_ingredients():

    ingredients = get_amount_table()
    ingredients = ingredients.transpose()
    ingredients =  ingredients.drop(labels="strdrink",axis=0)
    prices = prices_list()
    ingredients["prices"] = prices
    return ingredients



def get_ingredient_cost():
    df = get_amount_table()
    drinks = df["strdrink"].values.tolist()
    df = combine_prices_ingredients()
    for i in range(0,627):
        df[i] = df[i]*df["prices"]
    df= df.transpose()
    df = df.drop(labels = "prices", axis = 0)
    df["strdrink"] = drinks
    df = df.transpose()
    return df


def drop_all_zero_dummies():

    liquors = ["brandy","gin","tequila","vodka","whiskey","flavored rum","flavored vodka","cognac","bourbon","rum","scotch","grain alcohol"]
    small_drinks = drop_big_drinks()
    data = create_dummies().set_index("strdrink").transpose()
    data = data[small_drinks].transpose()
    data = data[liquors].replace(0, np.nan)
    data = data.dropna(how='all', axis=0)
    data = data.replace(np.nan, 0)

    return data
    