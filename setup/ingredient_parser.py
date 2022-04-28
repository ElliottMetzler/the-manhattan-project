import pandas as pd
import numpy as np
import re
import os


def extract_columns(in_path):
    """Extract ingredient measurement columns from the csv as a dataframe and remove commas and paranthesis."""
    df = (
        pd.read_csv(in_path, index_col=None, header=None)
        .iloc[:, 32:47]
        .fillna(0)
        .astype(str)
         )
    for col in df.columns:
        df[col]=df[col].str.replace(r"\(|\)|,", "")
        
    return df
    
def create_units_list(dataframe):
    """Remove all numbers and create a list of unique values of units of measurements"""

    all_values = list(np.unique(dataframe.values))

    units_list = [] 

    for unit in all_values:
        units_list.append(re.sub("[^a-zA-Z ]","",unit).strip())

    units_list = list(set(units_list))
    
    return units_list


def append_dict_value(unit_list):
    """Creates a dictionary for converting measurments units to ounces."""
    
    dict_value_list = [1, 0.0705479, 1, 8, 1, 8, 1, 0.125, 0.033814, 1, 1, 3.3814, 1, 0.0016907, 0.5, 12, 1.5, 8, 0.033814, 0.035, 8, 0.5, 0.105822, 0.166667, 0.5, 1, 0.0016907, 12, 8, 0.5, 0.125, 8, 8, 0.166667, 3.2, 0.2, 1, 0.26, 0.33814, 0.035274, 0.010, 1, 12, 12.6803, 6, 6, 0.2, 1, 33.814, 1, 33.814, 8, 0.166667, 1, 1, 0.50721, 0.33814,0.50721, 6, 0.554113, 1.5, 1, 0.375, 0.166667, 0.010, 8, 1, 8, 0.03125, 1, 1, 1, 1, 1, 5, 1, 0.166667, 1, 0.166667, 8, 1, 0.03125, 12, 0.31, 0.0705479, 7.5, 1.5, 1, 1, 0.035, 8, 0.105822, 128, 8, 8, 1, 1, 0.01, 0.010, 0.01, 1, 0.166667, 0.03125, 8, 0.125, 1.5, 3, 2, 1, 0.010, 1, 0.166667, 1, 0.26, 3, 1, 0.033814, 0.333333, 8, 1, 16, 0.0016907, 0.5, 8, 0.0705479, 8, 0.5, 6, 0.5, 8, 1, 1, 1, 0.166667, 1.5, 0.125, 1, 1, 0.2, 16, 0.166667, 3.3814, 0.5, 3, 8, 33.814, 1, 1, 8, 7, 1, 1, 1, 0.03125, 1, 8, 1, 1, 1.5, 2, 0.5, 0.033814, 0.166667, 1, 1, 1, 5.08, 0.31, 1.5, 0.33814, 0.5, 1.5, 5, 0.01, 1, 1, 14, 0.03125, 12, 25.4, 1, 0.0705479, 1]

    convert_dict = dict(zip(unit_list, dict_value_list))
    return convert_dict


def frac_to_dec_converter(num_strings):
    """Takes a list of strings that contains fractions and convert them into floats."""
    
    result_list = []

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

        result_list.append(converted)
        
    return result_list

def make_pattern(str_list):
    """Divides string list into readable pattern for regex."""
    
    str_pattern = ""
    for string in str_list:
        str_pattern += f"{string}|" 
    return str_pattern

def unit_unify(list_of_texts, unit_dict):
    """Takes a list of strings that contains liquid units, and converts them into fluid ounces."""
    
    str_pattern = make_pattern(units_list)
    pattern = fr"(^[\d -/]*)({str_pattern})"


    new_list = []
     
    for text in list_of_texts:
        re_result = re.search(pattern, text)
        
        if re_result:
            amount = re_result.group(1).strip()
            unit = re_result.group(2).strip()
            
            if not amount:
                amount = "1"

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
                to_oz = (amount*unit_dict[unit])/2
            else:
                to_oz = amount*unit_dict[unit]

            new_list.append(str(round(to_oz,2)))

        else:
            new_list.append(text)
            
    return new_list

def convert_columns(dataframe, unit_dict, out_path):
    """Convert units within each measurement column and save results to a csv."""

    for i in dataframe.columns:
        dataframe[i] = unit_unify(dataframe[i], unit_dict)

    dataframe.to_csv(out_path, index=False, header=False)


if __name__ == "__main__":
    BASE_DIR = "data"
    IN_PATH = os.path.join(BASE_DIR, "raw_data1.csv")
    OUT_PATH = os.path.join(BASE_DIR, "parsed_data.csv")
    os.makedirs(BASE_DIR, exist_ok=True)
    
    df = extract_columns(IN_PATH)
    units_list = create_units_list(df)
    convert_dict = append_dict_value(units_list)
    convert_columns(df, convert_dict, OUT_PATH)
