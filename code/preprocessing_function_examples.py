import pandas as pd
from quant_preprocess import query_and_preprocess_data
from quant_preprocess import query_and_reshape_long
from quant_preprocess import recode_long_data


# Guide to the key functions here:

# query_and_reshape_long: this will query the database and return a long format dataframe. Specifically, there are three columns: (1) strdrink (drink name), (2) ingredient, (3) amount (in ounces). For example of output, see below

df = query_and_reshape_long()
print("="*75)
print("Sample Output of query_and_reshape_long")
print("="*75)
print(df.head(10))

# recode_long_data: this will take the output of query_and_reshape_long and recode the ingredients according to the mapping I drafted in "ingredient_map.py" Same long format, just fewer rows and simpler ingredients.

recoded = recode_long_data(df)
print("="*75)
print("Sample Output of calling recode_long_data on output from query_and_reshape_long")
print("="*75)
print(recoded.head(10))

# query_and_preprocess_data: This is the original one - it takes the long data that has been recoded and first pivots wide so that each column is an ingredient then calculates the proportions for each row. Thus, each row will sum to 1 and each value is the percentage of that cocktail that is made up of that ingredient

df = query_and_preprocess_data()
print("="*75)
print("Sample Output of query_and_preprocess_data")
print("="*75)
print(df.head(10))