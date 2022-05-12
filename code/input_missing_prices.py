import os
import pandas as pd
import numpy as np

DIR = "data"
IN_PATH = os.path.join(DIR, "ingredient_prices_raw.csv")
OUTPUT_PATH = os.path.join(DIR, "ingredient_prices_clean.csv")

def final_prices(path):
    index = ["ingredient", "price"]
    df = pd.read_csv(IN_PATH, dtype = str)
    df = df.transpose()
    df["index"] = index
    df.set_index("index", inplace=True,drop=True)
    columns = df.loc["ingredient",:].tolist()
    df.columns = columns
    df.drop("ingredient")
    df.loc["price", "butter"] = 0.31
    df.loc["price","advocaat"] = 0.81
    df.loc["price", "erin cream"] = 0.394
    df.loc["price","flavored rum"] = 0.5
    df.loc["price","pernod"] = 1.14
    df.loc["price","water"] = 0.05
    df.loc["price","liqueur"] = 1
    df.loc["price","drambuie"] = 1.09
    df.loc["price","aquavit"] = 1.02
    df.loc["price","galliano"] = 1.1
    df.loc["price","ice"] = 0.018
    df.loc["price","bourbon"] = 1.1
    df.loc["price","vermouth"] = 1.2
    df.loc["price","scotch"] = 2.3
    df.loc["price","pisco"] = 1.49
    df.loc["price","whiskey"] = 0.57
    df.loc["price",'glycerine'] = 0.75
    df.loc["price","everclear"] = 0.909
    df.loc["price","schnapps"] = 0.394
    df.loc["price","olive brine"] = 0.4
    df.loc["price","sherry"] = 0.242
    df.loc["price","sugar"] = 0.53
    df.loc["price","sarsaparilla"] = 0.149
    df.loc["price","ricard"] = 1.18
    df.loc["price","dry vermouth"] = 1.2
    df.loc["price","cachaca"] = 0.515
    df.loc["price","jagermeister"] = 0.907
    df.loc["price","aperitif"] = 0.985
    df.loc["price","absinthe"] = 2.05
    df.loc["price","dubonnet rouge"] = 0.787
    df.loc["price","pisang ambon"] = 0.772
    df.loc["price","frangelico"] = 0.803
    df.loc["price","sweet and sour"] = 0.115
    df.loc["price","cherry heering"] = 1.18
    df.loc["price","beer"] = 0.1
    df.loc["price","herb"] = 2
    df.loc["price","coffee"] = 0.26
    df.loc["price","sambuca"] = 0.985
    df.loc["price","zima"] = 0.12
    df.loc["price","baileys"] = 0.907
    df.loc["price","brandy"] = 0.394
    df.loc["price","fruit"] = 0.33
    df.loc["price","coffee"] = 0.45
    df.loc["price","sugard"] = 0.53
    df.loc["price","rum"] = 0.5
    df.loc["price","gin"] = 0.788
    df.loc["price", "port"] = 0.788
    df = df.transpose()
    df.to_csv(path, index=False, header=False)


if __name__ == "__main__":

    os.makedirs(DIR, exist_ok = True)
    final_prices(OUTPUT_PATH)

