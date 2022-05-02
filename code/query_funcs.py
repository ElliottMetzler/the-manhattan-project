import pandas as pd
from database import engine


num_ingredients = 3

def query_table_1(liquor, num_ingredients):
	"""Function accepts a liquor and a number of ingredients, queries the database using these values, and returns a dataframe for use on streamlit"""
	liquor = str.lower(liquor)

	query = f"""
	select
	    strdrink,
	    stralcoholic,
	    strglass,
	    strinstructions,
	    total_ingredients,
	    
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
	    
	    strmeasure1,
	    strmeasure2,
	    strmeasure3,
	    strmeasure4,
	    strmeasure5,
	    strmeasure6,
	    strmeasure7,
	    strmeasure8,
	    strmeasure9,
	    strmeasure10,
	    strmeasure11,
	    strmeasure12,
	    
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
	where 
	    total_ingredients <= {num_ingredients} and
	    (lower(stringredient1) = '{liquor}' or
	    lower(stringredient2) = '{liquor}' or
	    lower(stringredient3) = '{liquor}')
	order by
	    total_ingredients desc
	;
	"""

	cols = ["strdrink",
	            "stralcoholic",
	            "strglass",
	            "strinstructions",
	            "total_ingredients",
	            "stringredient1",
	            "stringredient2",
	            "stringredient3"]

	rename_map = {
	    "strdrink" : "Drink Name",
	    "strglass" : "Glass Type",
	    "strinstructions" : "Instructions",
	    "total_ingredients" : "Total Ingredients Required",
	    "stringredient1" : "Ingredient 1",
	    "stringredient2" :"Ingredient 2",
	    "stringredient3" : "Ingredient 3"
	}

	df = pd.read_sql_query(query, engine)[cols].rename(rename_map,axis=1)

	return df