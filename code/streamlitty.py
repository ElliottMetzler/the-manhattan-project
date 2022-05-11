import streamlit as st
import pandas as pd
from streamlit_query_functions import main_query
from streamlit_query_functions import get_ingredients_list
from streamlit_query_functions import calculate_drink_prices 

# Import comprehensive list of ingredients
ingredients_list = get_ingredients_list()
ingredients_list.insert(0, "N/A")

# Import Drink Prices
prices = calculate_drink_prices()


# Functions
def gen_booze_criteria(vodka, whiskey, tequila, gin, rum):
	"""Function accepts the flags for checkboxes and returns a list of associated alcohols"""
	booze_criteria = []
	if vodka:
		booze_criteria.append("vodka")
	if whiskey:
		booze_criteria.append("whiskey")
	if tequila:
		booze_criteria.append("tequila")
	if gin:
		booze_criteria.append("gin")
	if rum:
		booze_criteria.append("rum")

	return booze_criteria

def gen_booze_mask(df, booze_criteria):
	"""Function accepts the data and the criteria and generates a mask to filter"""
	if len(booze_criteria) > 0:
		booze_mask = df["ingredients_list"].str.contains("|".join(booze_criteria))
	else:
		booze_mask = pd.Series([True] * len(df.index))

	return booze_mask

def gen_alt_ingredient_mask(df, alt_ingredient):
	"""Function accepts the data and the alt_ingredient selected and generates a mask to filter"""
	if alt_ingredient != "N/A":
		alt_ingredient_mask = df["ingredients_list"].str.contains(alt_ingredient)
	else:
		alt_ingredient_mask = pd.Series([True] * len(df.index))

	return alt_ingredient_mask

def extract_singleton_drink_info(df):
	"""Function takes in a drink (row of dataframe) and extracts info"""
	name = df["strdrink"].values[0]
	glass = df["strglass"].values[0]
	instructions = df["strinstructions"].values[0]
	image = df["strdrinkthumb"].values[0]
	cost = df["cost"].values[0]

	return name, glass, instructions, image, cost

def extract_list_drink_info(df):
	"""Function takes in a drink (row of dataframe) and extracts the lists split on the commas"""
	ingredients_list = df["ingredients_list"].values[0].split(",")
	proportions_list = df["proportions_list"].values[0].split(",")

	return ingredients_list, proportions_list


###########################################################
# Streamlit Code
###########################################################

st.set_page_config(layout="wide")
st.header("The Manhattan Project")

#######################################
# Side Bar - Search Parameters
#######################################

# Refresh Button
st.sidebar.write("""Once you select all of your drink specifications click here:""")
button=st.sidebar.button("Find My Drink")

# Ingredient Count Slider
st.sidebar.write("""
	# Ingredients:
	First, select the *maximum* number of ingredients you'd like in your cocktail""")
num_ingredients_tot = st.sidebar.slider("", 2, 12)

# Main Booze Options Checkboxes
st.sidebar.write("""
	# Main Liquors:
	Next, select some of the main booze options you have handy or would like to use in your cocktail.""")
vodka = st.sidebar.checkbox("Vodka")
whiskey = st.sidebar.checkbox("Whiskey")
tequila = st.sidebar.checkbox("Tequila")
gin = st.sidebar.checkbox("Gin")
rum = st.sidebar.checkbox("Rum")

# Other Ingredient Dropdown
st.sidebar.write("""
	# Other Ingredient:
	Finally, select another ingredient you'd like to include in your cocktail""")
alt_ingredient = st.sidebar.selectbox("", ingredients_list)


#######################################
# Main Container - 2 columns
#######################################
with st.container():

	col1, col2 = st.columns(2)

	#######################################
	# Column 1 - Page Welcome Message
	#######################################	

	col1.header("Welcome to our Page")
	col1.write("""
		Hello! Welcome to The Manhattan Project. This webpage is designed to help fuel Friday night. We get it, you've had a long week, you don't want to go to the store, and you sure as hell don't want to think too hard about what you want to drink to unwind tonight. That's where we come in. 
		With our site, you can search through a vast database of cocktails and concoctions using a variety of search parameters and settings to find exactly what you're looking for - whether thats a night in with a movie and a bowl of popcorn, a night out with some strangers, or a Saturday morning tailgate.
		How to use: First, you will use the side panel on to select a search setting. We currently support a few options. You can search by glass type, which is often indicative of the type of drink (i.e. shot glass or punch bowl ought to produce a nice party). Alternatively, you can search by an ingredient you have on hand and would like to use up, with a filter for the number of ingredients in the cocktail. We also support a combination of the two previous search options. Finally, we can generate a completely random drink.
		The panel to the right will display the featured result based on your search. Below, we also list other cocktails that fit the search parameters (if they exist), and allow you to select if you'd like to view another option.
		""")

	#######################################
	# Column 2 - Featured Drink Result
	#######################################

	if button:
		col2.header("Featured Drink Result")

		df = main_query(num_ingredients_tot)

		booze_criteria = gen_booze_criteria(vodka, whiskey, tequila, gin, rum)
		booze_mask = gen_booze_mask(df, booze_criteria)
		alt_ingredient_mask = gen_alt_ingredient_mask(df, alt_ingredient)

		combine = df[booze_mask & alt_ingredient_mask].merge(prices, how = "left", on = "strdrink")

		if len(combine["strdrink"])>0:

			featured_drink = combine.sample(1)
			feat_name, feat_glass, feat_instructions, feat_image, feat_cost = extract_singleton_drink_info(featured_drink)
			feat_ingredients_list, feat_proportions_list = extract_list_drink_info(featured_drink)

			col2.write(f"""
			Congratulations! You have selected the **{feat_name}**!
			First, you will need to get out a **{feat_glass}**.
			Next, grab the following ingredients:
			"""
			)

			for prop, ing in zip(feat_proportions_list, feat_ingredients_list):
				col2.write(f"* {prop} {ing}")

			col2.write(f"""
				Finally, here are the instructions to make your cocktail!
				{feat_instructions}

				Making this at home would only cost you about ${feat_cost} per drink! That's a steal!

				If it looks anything like this, you're probably in good shape!
				""")

			col2.image(feat_image)

			col2.write("Cheers!")
		else:
			col2.write("""There are no unique cocktails that follow your drink specifications. Try changing the maximum number of ingredients, selecting a different liquor, or choosing a different specified ingredient.""")

#######################################
# Second Container - Alternate Drinks
#######################################

with st.container():

	if button:
		if len(combine["strdrink"]) > 5:
			alt_sample = combine[combine["strdrink"] != feat_name].sample(5)
		else:
			alt_sample = combine[combine["strdrink"] != feat_name]

		if len(alt_sample["strdrink"]) == 0: # If no drinks, display this message
			st.header("""There are no alternative drinks with this selection of ingredients, liquor, or number of ingredients.""")

		if len(alt_sample["strdrink"]) > 0: # If any drinks, display this message 
			st.header("""If you aren't feeling our featured cocktail maybe one of these would be more your speed:""")

		if len(alt_sample["strdrink"])>= 1: # If 1 or more alternatives, do this

			# Extract the drink and the information
			alt1_drink = alt_sample.iloc[[0]]
			alt1_name, alt1_glass, alt1_instructions, alt1_image, alt1_cost = extract_singleton_drink_info(alt1_drink)
			alt1_ingredients_list, alt1_proportions_list = extract_list_drink_info(alt1_drink)

			# Write the output
			with st.expander(f"{alt1_name}"):
				st.write(f"""So the {feat_name} wasn't up you alley? Well, hopefully the **{alt1_name}** is better suited for you.
				You'll need a **{alt1_glass}**,
				and the following ingredients:
				""")

				for prop, ing in zip(alt1_proportions_list, alt1_ingredients_list):
					st.write(f"* {prop} {ing}")

				st.write(f"""
				To make a {alt1_name} follow these instructions:

				{alt1_instructions}

				When it costs only ${alt1_cost} per drink, why ever go to a bar again?
				""") 

		if len(alt_sample["strdrink"])>=2:

			# Extract the drink and the information
			alt2_drink = alt_sample.iloc[[1]]
			alt2_name, alt2_glass, alt2_instructions, alt2_image, alt2_cost = extract_singleton_drink_info(alt2_drink)
			alt2_ingredients_list, alt2_proportions_list = extract_list_drink_info(alt2_drink)

			# Write the expander
			with st.expander(f"{alt2_name}"):
				st.write(f"""Yeah, I'm not a fan of the {feat_name} either. A {alt2_name} is a much better choice.
				Get out a **{alt2_glass}**,
				and these ingredients:
				""")
				for prop, ing in zip(alt2_proportions_list, alt2_ingredients_list):
					st.write(f"* {prop} {ing}")
				st.write(f"""
				Once you follow these instructions, you'll have the perfect {alt2_name}.

			{alt2_instructions}

			You'll pay a lot more than ${alt2_cost} per drink at bar. So just kick your feet up and relax with a {alt2_name}.
			""")

		if len(alt_sample["strdrink"])>=3:

			# Extract the drink and information
			alt3_drink = alt_sample.iloc[[2]]
			alt3_name, alt3_glass, alt3_instructions, alt3_image, alt3_cost = extract_singleton_drink_info(alt3_drink)
			alt3_ingredients_list, alt3_proportions_list = extract_list_drink_info(alt3_drink)

			# Write the expander
			with st.expander(f"{alt3_name}"):
				st.write(f"""I should have known that you don't like {feat_name}. Well that's what the alternative drinks are for! I hope you'll like a {alt3_name}
				For this one you need a **{alt3_glass}** and these ingredients:
				""")

				for prop, ing in zip(alt3_proportions_list, alt3_ingredients_list):
					st.write(f"* {prop} {ing}")

				st.write(f"""
				A {alt3_name} isn't too hard to make! Just follow these instructions:

				{alt3_instructions}

				${alt3_cost} per drink? Wow, that's a cheap and delicious cocktail!
				""")

		if len(alt_sample["strdrink"])>=4:

			# Extract the drink and information
			alt4_drink = alt_sample.iloc[[3]]
			alt4_name, alt4_glass, alt4_instructions, alt4_image, alt4_cost = extract_singleton_drink_info(alt4_drink)
			alt4_ingredients_list, alt4_proportions_list = extract_list_drink_info(alt4_drink)

			# Write the expander
			with st.expander(f"{alt4_name}"):
				st.write(f"""Now we're talking! My favorite cocktail: {alt4_name}! No one likes a {feat_name} anyways, 
				we should really get that out of our database.
				{alt4_name} are simple you'll need a **{alt4_glass}** and these exact ingredients:
				""")

				for prop, ing in zip(alt4_proportions_list, alt4_ingredients_list):
					st.write(f"* {prop} {ing}")

				st.write(f"""
				With those ingredients just follow these steps, and presto a {alt4_name}!

				{alt4_instructions}

				At home is always cheaper and when its only ${alt4_cost} per drink, the adage continues to hold!
				""")

		if len(alt_sample["strdrink"])>=5:

			# Extract the drink and information
			alt5_drink = alt_sample.iloc[[4]]
			alt5_name, alt5_glass, alt5_instructions, alt5_image, alt5_cost = extract_singleton_drink_info(alt5_drink)
			alt5_ingredients_list, alt5_proportions_list = extract_list_drink_info(alt5_drink)

			# Write the expander
			with st.expander(f"{alt5_name}"):
				st.write(f"""This is your last choice you have! You better like a {alt5_name}, it's definitely better than a {feat_name}
				First you will have to find a **{alt5_glass}** and these ingredients:
				""")
				for prop, ing in zip(alt5_proportions_list, alt5_ingredients_list):
					st.write(f"* {prop} {ing}")

				st.write(f"""
				No need to just throw the ingredients together. Follow these steps and you'll have a {alt5_name}!

				{alt5_instructions}

				${alt5_cost} per drink? Imagine ordering that at a bar it would cost double maybe even triple that!
				""")

#######################################
# Third Container - Acknowledgements
#######################################

with st.container():
	st.write("""
	All data is sourced from the [Cocktail Database](https://www.thecocktaildb.com/). This dashboard was created with the free to use platform [Streamlit](https://streamlit.io/). For any inquiries on the coding or the structure of this project connect to our [GitHub](https://github.com/ElliottMetzler/the-manhattan-project). Enjoy your drinks!
	""")