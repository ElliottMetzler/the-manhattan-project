import pandas as pd
from database import engine


def main_query(num_ingredients):
	"""Function accepts a number of ingredients, queries the database using these values, and returns a dataframe for use on streamlit"""
	# liquor1 = str.lower(liquor1)

	query = f"""
	select
	    strdrink,
	    stralcoholic,
	    strglass,
	    strinstructions,
	    total_ingredients,

	    strdrinkthumb,
	    
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
	    total_ingredients <= {num_ingredients}
	order by
		total_ingredients desc
	;
	"""

	cols = [
	"strdrink",
	"strglass",
      "strinstructions",
      "total_ingredients",
      "proportions_list",
     "ingredients_list",
     "strdrinkthumb"]

	ingredient_cols = [
	    "stringredient1",
	    "stringredient2",
	    "stringredient3",
	    "stringredient4",
	    "stringredient5",
	    "stringredient6",
	    "stringredient7",
	    "stringredient8",
	    "stringredient9",
	    "stringredient10",
	    "stringredient11",
	    "stringredient12"
	]

	raw_prop_cols = [
	    "strmeasure1",
	    "strmeasure2",
	    "strmeasure3",
	    "strmeasure4",
	    "strmeasure5",
	    "strmeasure6",
	    "strmeasure7",
	    "strmeasure8",
	    "strmeasure9",
	    "strmeasure10",
	    "strmeasure11",
	    "strmeasure12"
	]


	df = (
		pd.
    	read_sql_query(query,engine).
	    assign(ingredients_list = lambda df_: df_[ingredient_cols].
	          apply(lambda x: ", ".join(x[x.notnull()].str.lower()), axis=1),
	          proportions_list = lambda df_: df_[raw_prop_cols].
	          apply(lambda x: ", ".join(x[x.notnull()]), axis=1))
	    [cols]
	)

	"""
	criteria = (
		df["ingredients_list"].str.contains(liquor1)
	)

	one_drink = df[criteria].sample(1)
	"""
	return df

def get_ingredients_list():
	"""Function accepts no arguments and returns a comprehensive, unique, lowercase list of ingredients"""

	query = f"""
	select
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
	    stringredient12
	from
		all_cocktails

	"""
	df = pd.read_sql_query(query, engine)

	list_ = []

	for col in df.columns:
		as_list = df[col].tolist()

		list_ += as_list

	list_lower = [x.lower() for x in list_ if x is not None]

	return sorted(list(set(list_lower)))



# Testing area
if __name__ == "__main__":

	print(main_query(3))
	# print(get_ingredients_list())