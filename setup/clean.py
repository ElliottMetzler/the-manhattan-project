import pandas as pd
import numpy as np
import re
import os


def add_drop_columns(in_path):
    """Drop extraneous columns with few to no observations. Add a total ingredient count column and 12 new ingredient measurement columns with commas, parentheses, and new line characters removed. Add 1 oz for entries where ingrdient is specified but measurement is not. Replace commas in instructions columns with periods. Replace new line characters in the instructions, and image attribution columns with space."""

    cols = ["strDrinkAlternate","strInstructionsES","strInstructionsFR","strInstructionsZH-HANS",
        "strInstructionsZH-HANT","strIngredient13","strIngredient14","strIngredient15","strMeasure13",
        "strMeasure14","strMeasure15"]

    cols1 = ["strIngredient1","strIngredient2","strIngredient3","strIngredient4","strIngredient5","strIngredient6",
            "strIngredient7","strIngredient8","strIngredient9","strIngredient10","strIngredient11","strIngredient12"]

    cols2 = ["strMeasure1","strMeasure2","strMeasure3","strMeasure4","strMeasure5","strMeasure6","strMeasure7",
             "strMeasure8","strMeasure9","strMeasure10","strMeasure11","strMeasure12"]
    
    cols3 = ["strInstructions","strInstructionsDE","strInstructionsIT"]
    
    cols4 = ["strImageAttribution"]
    
    df = (
            pd.read_csv(in_path, index_col=None)
            .drop(cols, axis=1)
            .dropna(subset=cols2, how="all", axis=0)
            .assign(total_ingredients=lambda df: df[cols1].count(axis='columns'))

             )
    
    for col1, col2 in zip(cols1, cols2):
        df[col2] = df[col2].mask(df[col1].notna() & df[col2].isna(), "1 oz")

    df[pd.Index(cols2) + "_clean"] = df[cols2].apply(lambda col: col.str.replace(r"\(|\)|,|\r\n|\n", ""))   
    
    df[pd.Index(cols3)] = df[cols3].apply(lambda col: col.str.replace(",",".")).replace(r"\r\n|\n", " ")

    df[pd.Index(cols4)] = df[cols4].apply(lambda col: col.str.replace("\r\n"," "))


    return df

def extract_columns(dataframe):
    """Extract cleaned ingredient measurement columns as a dataframe."""
    
    cols = ["strMeasure1_clean","strMeasure2_clean","strMeasure3_clean","strMeasure4_clean","strMeasure5_clean",
             "strMeasure6_clean","strMeasure7_clean","strMeasure8_clean","strMeasure9_clean","strMeasure10_clean",
             "strMeasure11_clean","strMeasure12_clean"]
    
    df1 = (
           dataframe.iloc[:, [df.columns.get_loc(c) for c in cols]]
           .fillna(0)
           .astype(str)
              )
    
    return df1

def create_units_list(dataframe):
    """Remove all numbers and create a list of unique values of units of measurements"""

    all_values = list(np.unique(dataframe.values))

    units_list = [] 

    for unit in all_values:
        units_list.append(re.sub("[^a-zA-Z ]","",unit).strip())

    units_list = list(set(units_list))
    
    return units_list
    
def create_dict():
    """Create a dictionary for converting measurments units to ounces."""
    convert_dict = {
     '':1,
     'oz light':1,
     'oz hot':1,
     'oz':1,
     'oz white or':1,
     'oz Hazlenut':1,
     'oz cold':1,
     'oz Green Ginger':1,
     'oz Muscatel':1,
     'oz whole':1,
     'oz pure':1,
     'oz dry':1,
     'oz instant':1,
     'oz sweetened':1,
     'oz chopped bittersweet or semisweet':1,
     'oz skimmed':1,
     'mlfl oz':1,
     'oz frozen':1,
     'oz double':1,
     'oz lemon':1,
     'oz sweet':1,
     'oz Mexican':1,
     'oz finely chopped dark':1,
     'oz unsweetened':1,
     'oz fine':1,
     'oz Chilled':1,
     'oz Bacardi':1,
     'oz Stoli':1,
     'oz plain':1,
     'oz white':1,
     'oz blue':1,
     'oz Jamaican':1,
     'oz Blended':1,
     'oz cream':1,
     'oz chilled':1,
     'oz red':1,
     'oz Grape':1,
     'oz light or dark':1,
     'Add  oz':1,
     'Fill to top':1,
     'top up with':1,
     'for topping':1,
     'Top it up with':1,
     'Top up with':1,
     'Top':1,
     'top up':1,
     'Fill to top with':1,
     'to fill':1,
     'Fill with':1,
     'fill':1,
     'Shot':1.5,
     'shot Jamaican':1.5,
     'shot Bacardi':1.5,  
     'shot':1.5,
     'shots':1.5,
     'tsp dried':0.166667,
     'tsp crushed':0.166667,
     'tsp':0.166667,
     'tsp sweetened':0.166667,
     'tsp superfine':0.166667,
     'tsp dried and chopped':0.166667,
     'tsp Tropical':0.166667,
     'tsp ground':0.166667,
     'tsp grated':0.166667,
     'tsp powdered':0.166667,
     'tsp instant':0.166667,
     'tsp ground roasted':0.166667,
     'tbsp':0.5,
     'tblsp chopped':0.5,
     'tblsp green':0.5,
     'tblsp hot':0.5,
     'tblsp':0.5,
     'tblsp ground':0.5,
     'tblsp instant':0.5,
     'tblsp fresh chopped':0.5,
     'tblsp fresh':0.5,
     'tablespoons':0.5,
     'ml pure':0.033814,
     'ml white':0.033814,
     'ml frozen':0.033814,
     'ml':0.033814,
     'Add  ml':0.033814,
     'cL':0.33814,
     'cl':0.33814,
     'cl hot':0.33814,
     'cl cold':0.33814,
     'cl Smirnoff':0.33814,
     'dl':3.3814,
     'dl Schweppes':3.3814,
     'L':33.814,
     'L Jamaican':33.814,
     'cups white':8,
     'cup boiling':8,
     'cup mild':8,
     'cup plain':8,
     'cup granulated':8,
     'cup superfine':8,
     'Cup':8,
     'cup iced':8,
     'cup black':8,
     'cup cold':8,
     'cups':8,
     'cup pure':8,
     'cup hot':8,
     'cups fresh':8,
     'cups cold':8,
     'cup instant':8,
     'cup':8,
     'cups hot':8,
     'cup Thai':8,
     'cup fruit':8,
     'Add  cup':8,
     'cup crushed':8,
     'cup skimmed':8,
     'cups boiling':8,
     'glass crushed':8,
     'glass cold':8,
     'glass strong black':8,   
     'full glass':8,
     'Full Glass':8,
     'glass':8,
     'Around rim put pinch':0.010,
     'pinches':0.010,
     'pinch':0.010,
     'Pinch':0.010,
     'oneinch':0.554113,
     'inch':0.554113,
     'inch strips':0.554113, 
     'drops yellow':0.0016907,
     'drops':0.0016907,
     'drop green':0.0016907,
     'drop':0.0016907,
     'drops blue':0.0016907,
     'drop yellow':0.0016907,
     'About  drops':0.0016907,
     'drops red':0.0016907,
     'pint':16,
     'pint Jamaican':16,
     'pint sweet or dry':16,  
     'pint hard':16,
     'Dashes':0.021,
     'Dash':0.021,
     'dashes':0.021,
     'dash':0.021,
     'can frozen':13.5,
     'can sweetened':13.5,
     'cans':13.5,
     'can':13.5,
     'gal Tropical Berry':153.722, 
     'gal':153.722,
     'quart':32,
     'quart black':32,
     'qt':32,
     'lb':16,
     'lb frozen':16,
     'slice':0.5,
     'Slice':0.5,
     'part':1,
     'part Bass pale':1,
     'parts':1,
     'Juice of  wedge':1,
     'wedges':1, 
     'wedge':1,
     'Wedges':1,
     'Sprig':0.08,
     'Large Sprig':0.08,
     'sprigs':0.08, 
     'splash':0.2,
     'Add splash':0.2,
     'splashes':0.2,
     'jiggers':1.5, 
     'jigger':1.5,
     'piece textural':1,
     'piece':1,
     'pieces':1,
     'chunk dried':1,
     'chunks':1,
     'Fresh':0.2, 
     'Fresh leaves':0.2,
     'fresh':0.2,
     'cubes':4, 
     'cube':4,
     'Ground':0.33,
     'ground':0.33,
     'crushed':0.33,
     'cracked':0.33,
     'Whole':0.5,
     'whole':0.5,
     'whole green':0.5, 
     'About  bottle':25.4,
     'bottle':25.4,
     'bottles':25.4,
     'large bottle':25.4,
     'small bottle':12.07,     
     'mikey bottle':12,
     'bottle Boone Strawberry Hill':25.4,
     'sticks':0.1,
     'stick':0.1,
     'twist of':0.07, 
     'Twist of':0.07,
     'packages':0.5,
     'package':0.5,
     'Garnish':0.05,
     'Garnish with':0.05,
     'garnish':0.2,    
     'gr':0.035274,
     'kg chopped':35.274,
     'fifth':0.2,
     'Chopped':0.0705479,
     'if needed':1,
     'or':1,
     'scoops':2.66664,
     'fifth Smirnoff red label':5,
     'pods':1,   
     'handful':0.5,
     'Juice of':1,
     'A little bit of':1,
     'to taste':0.166667,
     'By taste':0.166667,
     'Rimmed':0.166667, 
     'measures':1.5, 
     'Chilled':0.5,
     'frozen':3.6,
     'Strong cold':0.5, 
     'Turkish apple':1,
     'long strip':0.07, 
     'Coarse':0.010,
     'or lime':0.5,   
     'ripe':0.4,
     'Bacardi':0.5,
     'Float Bacardi':0.5,
     'spoons':0.5,
     'Add':4,
     'lots':6,  
     'Squeeze':1,
     'Unsweetened':0.5,
     'mini':3,
     'Claret':0.5,   
     'seltzer water':1,
     'black':0.5,
     'Grated':0.2, 
     'beaten':0.63,
     'orange':20,  
     'very sweet':0.07,
     'large':2.5,
     'Over':4,

            }
    return convert_dict

def frac_to_dec_converter(num_strings):
    """Take a list of strings that contains fractions and convert them into floats."""
    
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
    """Divide string list into readable pattern for regex."""
    
    str_pattern = ""
    for string in str_list:
        str_pattern += f"{string}|" 
    return str_pattern

def unit_unify(list_of_texts, unit_dict):
    """Take a list of strings that contains measurement units, and converts them into ounces."""
    
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
            
            hyphen_pattern = re.compile(r'(?!(?<=\d)-\d)-')
            amount = (re.sub(hyphen_pattern, "", amount))
            
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

def convert_columns(dataframe, unit_dict):
    """Convert units within each measurement column."""
    
    for i in dataframe.columns:
            dataframe[i] = unit_unify(dataframe[i], unit_dict)

    return dataframe

def create_csv(dataframe, path1, path2):
    """Combine converted columns with the original dataframe. Return dataframe as two csv files: a csv without headers and a csv of header names."""
    
    df2 = df.assign(**df1).fillna(df)
    
    df2.to_csv(path1, index=False, header=False)
    
    
    headers = pd.DataFrame(df2.columns.values)

    headers.to_csv(path2, header = ["column names"], index=False)


if __name__ == "__main__":
    BASE_DIR = "data"
    IN_PATH = os.path.join(BASE_DIR, "raw_data.csv")
    NO_HEADER_PATH = os.path.join(BASE_DIR, "clean_data_no_header.csv")
    HEADER_PATH = os.path.join(BASE_DIR, "headers.csv")
    os.makedirs(BASE_DIR, exist_ok=True)
    
    df = add_drop_columns(IN_PATH)
    df1 = extract_columns(df)
    units_list = create_units_list(df1)
    convert_dict = create_dict()
    dataframe = convert_columns(df1, convert_dict)
    create_csv(dataframe, NO_HEADER_PATH, HEADER_PATH)
