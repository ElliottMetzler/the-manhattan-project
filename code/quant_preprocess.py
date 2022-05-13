import pandas as pd
import numpy as np
from database import engine
from ingredient_map import create_ingredient_map
import os


# Functions
def query_data():
    """Query Database and return Data Frame with relevant columns"""
    query = """
    select
        strdrink,
        stringredient1,
        stringredient2,
        stringredient3,
        stringredient4,
        stringredient5,
        stringredient6,
        stringredient7,
        stringredient8,
        stringredient9,
        stringredient10,
        stringredient11,
        stringredient12,
        strmeasure1_clean,
        strmeasure2_clean,
        strmeasure3_clean,
        strmeasure4_clean,
        strmeasure5_clean,
        strmeasure6_clean,
        strmeasure7_clean,
        strmeasure8_clean,
        strmeasure9_clean,
        strmeasure10_clean,
        strmeasure11_clean,
        strmeasure12_clean
        
    from 
        all_cocktails
    ;
        """

    return pd.read_sql_query(query, engine)


def query_ingredient_prices():
    """Function queries the database for ingredient prices and returns data frame"""
    query = f"""
    select *
    from ingredient_prices;
    """

    return pd.read_sql_query(query, engine)


def cols_to_lower(df, columns):
    """Convert batch of columns to lowercase"""

    return df[columns].apply(lambda col: col.str.lower())


def get_cols_list(df, starts_with_criteria):
    """Get a list of columns based on criteria, returns list"""
    return [col for col in df.columns if col.startswith(starts_with_criteria)]


def shape_data_long(df, list_of_cols, col_start_string, col_end_string, new_name):
    """Reshapes ingredients or measurements in long format"""
    return (
        df[["strdrink"] + list_of_cols]
        .melt(id_vars="strdrink", value_vars=list_of_cols)
        .assign(
            ingred_num=lambda df_: df_["variable"]
            .str.replace(col_start_string, "")
            .str.replace(col_end_string, "")
            .astype("int")
        )
        .drop("variable", axis=1)
        .rename({"value": new_name}, axis=1)
    )


def merge_long(table_1, table_2):
    """Merges ingredients and measurements table and returns a long format dataframe"""
    return (
        table_1.merge(table_2, on=["strdrink", "ingred_num"])
        .sort_values(["strdrink", "ingred_num"])
        .drop("ingred_num", axis=1)
        .dropna()
        .reset_index(drop=True)
    )


def pivot_wide(df):
    """Takes long format dataframe and pivots wide so that each column is a unique ingredient and each row is a drink. Values are the amount included in each drink in ounces"""
    return (
        df.pivot_table(
            index="strdrink", columns="ingredient", values="amount", aggfunc=np.sum
        )
        .fillna(0)
        .reset_index()
    )


def recode_ingredients(df, dictionary):
    """Accepts the dataframe and a dictionary to recode the ingredients and applies"""
    return df.assign(ingredient=lambda df_: df_["ingredient"].replace(dictionary))


def calculate_row_sum(df):
    """Function takes in a dataframe, calculates the row sum of numeric columns, and returns a dataframe"""
    return df.assign(
        row_sum=lambda df_: df_.select_dtypes(include=np.number).sum(axis=1)
    )


def get_prop_cols(df):
    """Function takes in dataframe, gets columns for calculating proportion"""
    return [col for col in df.columns if (col != "strdrink") and (col != "row_sum")]


def calculate_row_prop(df, prop_cols):
    """Function takes in dataframe, calculates proportions for columns, returns dataframe"""

    return df[prop_cols].apply(lambda col: col / df["row_sum"])


def query_and_reshape_long():
    """Function queries the database and reshapes the data in long format with three columns - drink, ingredient, and amount in ounces"""
    df = query_data()
    ingred_cols = get_cols_list(df, "stringredient")
    measure_cols = get_cols_list(df, "strmeasure")

    df[ingred_cols] = cols_to_lower(df, ingred_cols)

    ingredient_long = shape_data_long(
        df, ingred_cols, "stringredient", "", "ingredient"
    )

    measure_long = shape_data_long(df, measure_cols, "strmeasure", "_clean", "amount")

    return merge_long(ingredient_long, measure_long)


def recode_long_data(df):
    """Function takes the long format data and recodes the ingredients"""

    ingredient_dict = create_ingredient_map()
    return recode_ingredients(df, ingredient_dict)


def query_and_preprocess_data():
    """Function performs full preprocessing: Queries the database, recodes incredients, reshapes in wide format with a column for each ingredient and a row for each drink. Values are the proportion of that drink that is made up of that ingredient (rows sum to 1)"""

    df = query_and_reshape_long()

    recoded_long = recode_long_data(df)

    combined_wide = pivot_wide(recoded_long)

    w_rowsum = calculate_row_sum(combined_wide)

    prop_cols = get_prop_cols(w_rowsum)
    w_rowsum[prop_cols] = calculate_row_prop(w_rowsum, prop_cols)

    return w_rowsum.drop("row_sum", axis=1)


if __name__ == "__main__":
    print(price_and_abv_preprocessed())

    sample = price_and_abv_preprocessed()
    sample.to_csv("data/Sample_of_price_and_abv_preprocessed.csv")
