from make_raw_csv import create_raw_data
import os
import pandas as pd

if __name__ == "__main__":
    BASE_DIR = "data"
    NO_HEADER_PATH = os.path.join(BASE_DIR, "no_header_complete_raw_data.csv")
    WITH_HEADER_PATH = os.path.join(BASE_DIR, "header_complete_raw_data.csv")
    os.makedirs(BASE_DIR, exist_ok=True)
    HEADER_PATH = os.path.join(BASE_DIR, "headers_only.csv")

raw_data = create_raw_data("http://www.thecocktaildb.com/api/json/v1/1/search.php?f=")

raw_data["NIngredients"] = raw_data[["strIngredient1","strIngredient2","strIngredient3","strIngredient4","strIngredient5","strIngredient6","strIngredient7","strIngredient8","strIngredient9","strIngredient10","strIngredient11","strIngredient12"]].count(axis='columns')


raw_data = raw_data.drop(raw_data.columns[[2, 10, 12, 14, 15, 29, 30, 31, 44, 45, 46]], axis=1)

raw_data.to_csv(NO_HEADER_PATH, index=False, header=False)

raw_data.to_csv(WITH_HEADER_PATH, index=False)

headers = pd.DataFrame(raw_data.columns.values)

headers.to_csv(HEADER_PATH, header = ["column names"], index=False)