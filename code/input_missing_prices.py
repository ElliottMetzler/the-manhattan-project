import os
import pandas as pd
import numpy as np
#verify:
#cornstarch, cognac, grain alcohol, bitters, champagne, egg, frangelico
#look at the type of herbs in the list

IN_PATH = os.path.join("data", "ingredient_prices_raw.csv")
OUTPUT_DIR = "data"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "ingredient_prices_clean.csv")

def clean_prices(IN_PATH):

    df = pd.read_csv(IN_PATH)
    df = df.transpose()
    # df.loc[:"butter"] = 0.31
    # df.loc[:"advocaat"] = 0.81
    # df["erin cream"] = 0.394
    # df["flavored rum"] = 0.5
    # df["pernod"] = 1.14
    # df["water"] = 0.05
    # df["liqueur"] = 1
    # df["drambuie"] = 1.09
    # df["aquavit"] = 1.02
    # df["galliano"] = 1.1
    # df["ice"] = 0.018
    # df["bourbon"] = 1.1
    # df["vermouth"] = 1.2
    # df["scotch"] = 2.3
    # df["pisco"] = 1.49
    # df["whiskey"] = 0.57
    # df['glycerine'] = 0.75
    # df["everclear"] = 0.909
    # df["shnapps"] = 0.394
    # df["olive brine"] = 0.4
    # df["sherry"] = 0.242
    # df["sugar"] = 0.53
    # df["sarsaparilla"] = 0.149
    # df["ricard"] = 1.18
    # df["dry vermouth"] = 1.2
    # df["cachaca"] = 0.515
    # df["jagermeister"] = 0.907
    # df["aperitif"] = 0.985
    # df["absinthe"] = 2.05
    # df["dubonnet rouge"] = 0.787
    # df["pisang ambon"] = 0.772
    # df["frangelico"] = 0.803
    # df["sweet and sour"] = 0.115
    # df["cherry heering"] = 1.18
    # df["beer"] = 0.1
    # df["herb"] = 2
    # df["coffee"] = 0.26
    # df["sambuca"] = 0.985
    # df["zima"] = 0.12
    # df["baileys"] = 0.907
    # df["brandy"] = 0.394
    # df["fruit"] = 0.33
    # df["coffee"] = 0.45
    # df["sugard"] = np.nan
    # df["rum"] = 0.5
    l = df.values.tolist()[0]
    df.columns = l
    df.drop
    df.to_csv(OUTPUT_PATH)


if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok = True)
    clean_prices(IN_PATH)

