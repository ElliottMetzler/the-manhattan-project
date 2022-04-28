import pandas as pd
import numpy as np
import re
import os

if __name__ == "__main__":
    BASE_DIR = "data"
    IN_PATH = os.path.join(BASE_DIR, "raw_data.csv")
    OUT_PATH = os.path.join(BASE_DIR, "parsed_data.csv")
    os.makedirs(BASE_DIR, exist_ok=True)

"""Extract ingredient measurement columns from the csv as a dataframe."""

df = (
    pd.read_csv(IN_PATH, index_col=None, header=None)
    .iloc[:, 32:47]
    .fillna(0)
    .astype(str)
     )

"""Remove all numbers and create a list of unique values of units of measurements"""

all_values = list(np.unique(df.values))

no_numbers = [] 

for unit in all_values:
    no_numbers.append(re.sub("[^a-zA-Z ]","",unit).strip())
    
no_numbers = list(set(no_numbers))

def make_conversion_dict(str_list):
    """Creates dictionary keys from list items"""

    conversion_dict = {}

    for string in str_list:
        conversion_dict[string] = None

    return conversion_dict


"""Create a dictionary converting all units of measurement to ounces."""

liquid_units = {"":1,
                "oz":1,
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
                "Smirnoff red label":25.3605,
                "Juice of":1,
                "Fresh":1
                
               }

def frac_to_dec_converter(num_strings):
    """Takes a list of strings that contains fractions and convert them into floats."""
    
    result = []

    for frac_str in num_strings:
        try:
            converted = float(frac_str)
        except ValueError:
            num, denom = frac_str.split('/')
            try:
                leading, num = num.split(' ')
                total = float(leading)
            except ValueError:
                total = 0
            frac = float(num) / float(denom)
            converted = total + frac

        result.append(converted)
        
    return result

def make_pattern(str_list):
    """Divides string list into readable pattern for regex."""
    str_pattern = ""
    for string in str_list:
        str_pattern += f"{string}|" 
    return str_pattern

def unit_unify(list_of_texts):
    """Takes a list of strings that contains liquid units, and converts them into fluid ounces."""
    str_pattern = make_pattern(no_numbers)
    pattern = fr"(^[\d -/]*)({str_pattern})"


    new_list = []
     
    for text in list_of_texts:
        re_result = re.search(pattern, text)
        
        if re_result:
            amount = re_result.group(1).strip()
            if not amount:
                amount = "1.0"
            unit = re_result.group(2).strip()

            if "-" in amount:
                ranged = True
            else:
                ranged = False
            
            amount = re.sub(r"(\d) (/\d)",r"\1\2",amount) 
            amount = amount.replace("-","+").replace(" ","+").strip()
            amount = re.sub(r"[+]+","+",amount)
            amount_in_dec = frac_to_dec_converter(amount.split("+"))
            amount = np.sum(amount_in_dec)
            
            if ranged:
                to_oz = (amount*liquid_units[unit])/2
            else:
                to_oz = amount*liquid_units[unit]

            new_list.append(str(round(to_oz,2)))

        else:
            new_list.append(text)
            
    return new_list

"""Convert units within each measurement column and save results to a csv."""

for i in df.columns:
    df[i] = unit_unify(df[i])
    
df.to_csv(OUT_PATH, index=False, header=False)