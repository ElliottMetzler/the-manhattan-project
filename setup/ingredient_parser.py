import pandas as pd
import numpy as np
import re
import os

if __name__ == "__main__":
    BASE_DIR = "data"
    CSV_PATH = os.path.join(BASE_DIR, "raw_data.csv")
    os.makedirs(BASE_DIR, exist_ok=True)

'''Extract ingredient measurement columns from the csv as a dataframe.'''

df = (
    pd.read_csv(CSV_PATH, header=None)
    .iloc[:, 33:47]
     )

'''Remove all numbers and create a list of unique values of units of measurements'''

all_values = list(np.unique(df.values))

no_numbers = [] 

for unit in all_values:
    no_numbers.append(re.sub("[^a-zA-Z ]","",unit).strip())
    
no_numbers = list(set(no_numbers))

'''Create a dictionary converting all units of measurement to ounces.'''

liquid_units = {"oz":1,
                "ml":0.033814,
                "cl":0.33814,
                "tsp":0.166667,
                "teaspoon":0.166667,
                "teaspoons":0.166667,
                "tea spoon":0.166667,
                "tbsp":0.5,
                "tablespoon":0.5,
                "tablespoons":0.5,
                "table spoon":0.5,
                "cup":8,
                "cups":8,
                "qt":0.03125,
                "quart":0.03125,
                "quarts":0.03125,
                "drop":0.0016907,
                "drops":0.0016907,
                "shot":1.5,
                "shots":1.5,
                "cube":1,
                "cubes":1,
                "dash":0.03125,
                "dashes":0.03125,
                "l":33.814,
                "L":33.814,
                "liters":33.814,
                "Liters":33.814,
                "wedge":0.125,
                "wedges":0.125,
                "pint":16,
                "pints":16,
                "slice":0.50721,
                "slices":0.50721,
                "twist of":0.0705479,
                "top up":1,
                "small bottle":7,
               }

