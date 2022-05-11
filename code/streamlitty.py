import streamlit as st
import pandas as pd
from database import engine
from streamlit_query_functions import main_query
from streamlit_query_functions import get_ingredients_list
from streamlit_query_functions import calculate_drink_prices 

# Import comprehensive list of ingredients
ingredients_list = get_ingredients_list()
ingredients_list.insert(0, "N/A")

# Import Drink Prices
prices = calculate_drink_prices()


# Functions
def gen_ingredient_selectbox():
	"""Function Creates a broad ingredient selectbox"""
	prompt = f"Other Ingredient Selection:"
	return st.sidebar.selectbox(prompt, ingredients_list)

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
	"""Function takes in a drink (row of dataframe) and extracts info as tuples"""
	name = df["strdrink"].values[0]
	glass = df["strglass"].values[0]
	instructions = df["strinstructions"].values[0]
	image = df["strdrinkthumb"].values[0]
	cost = df["cost"].values[0]

	return name, glass, instructions, image, cost

def extract_list_drink_info(df):
	"""Function takes in a drink (row of dataframe) and extracts the lists as tuples"""
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
alt_ingredient = gen_ingredient_selectbox()


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
			name, glass, instructions, image, cost = extract_singleton_drink_info(featured_drink)
			ingredients_list, proportions_list = extract_list_drink_info(featured_drink)

			col2.write(f"""
			Congratulations! You have selected the **{name}**!
			First, you will need to get out a **{glass}**.
			Next, grab the following ingredients:
			"""
			)

			for prop, ing in zip(proportions_list, ingredients_list):
				col2.write(f"* {prop} {ing}")

			col2.write(f"""
				Finally, here are the instructions to make your cocktail!
				{instructions}

				Making this at home would only cost you about ${cost} per drink! That's a steal!

				If it looks anything like this, you're probably in good shape!
				""")

			col2.image(image)

			col2.write("Cheers!")
		else:
			col2.write("""There are no unique cocktails that follow your drink specifications. Try changing the maximum number of ingredients, selecting a different liquor, or choosing a different specified ingredient.""")

#######################################
# Secondary Container - Alternate Drinks
#######################################

with st.container():
	alt_sample=[]
	alt_1=[]
	alt_2=[]
	alt_3=[]
	alt_4=[]
	alt_5=[]
	
	if button:
		if len(combine["strdrink"])>5:
			alt_sample=combine.sample(5)
		else:
			alt_sample=combine

		if len(alt_sample["strdrink"])==1:
			st.header("""There are no alternative drinks with this selection of ingredients, liquor, or number of ingredients.""")
		if len(alt_sample["strdrink"])>1:
			st.header("""If you aren't feeling our featured cocktail maybe one of these would be more your speed:""")

		if len(alt_sample["strdrink"])>=1:
			if alt_sample["strdrink"].values[0]!=featured_drink["strdrink"].values[0]:
				alt_1=alt_sample["strdrink"].values[0]
				alt_drink_1=alt_sample[alt_sample["strdrink"]==alt_1]
				ingredients_list_1 = alt_drink_1["ingredients_list"].values[0].split(",")
				proportions_list_1 = alt_drink_1["proportions_list"].values[0].split(",")
				with st.expander(f"{alt_1}"):
					st.write(f"""So the {name} wasn't up you alley? Well, hopefully the {alt_1} is better suited for you.
					You'll need a **{alt_drink_1["strglass"].values[0]}**,
					and the following ingredients:
					""")

					for prop, ing in zip(proportions_list_1, ingredients_list_1):
						st.write(f"* {prop} {ing}")

					st.write(f"""
					To make a {alt_1} follow these instructions:

					{alt_drink_1["strinstructions"].values[0]}

					When it costs only ${alt_drink_1["cost"].values[0]} per drink, why ever go to a bar again?
					""") 

		if len(alt_sample["strdrink"])>=2:
			if alt_sample["strdrink"].values[1]!=featured_drink["strdrink"].values[0]:
				alt_2=alt_sample["strdrink"].values[1]
				alt_drink_2=alt_sample[alt_sample["strdrink"]==alt_2]
				ingredients_list_2 = alt_drink_2["ingredients_list"].values[0].split(",")
				proportions_list_2 = alt_drink_2["proportions_list"].values[0].split(",")
				with st.expander(f"{alt_2}"):
					st.write(f"""Yeah, I'm not a fan of the {name} either. A {alt_2} is a much better choice.
					Get out a **{alt_drink_2["strglass"].values[0]}**,
					and these ingredients:
					""")

					for prop, ing in zip(proportions_list_2, ingredients_list_2):
						st.write(f"* {prop} {ing}")
					st.write(f"""
					Once you follow these instructions, you'll have the perfect {alt_2}.

				{alt_drink_2["strinstructions"].values[0]}

				You'll pay a lot more than ${alt_drink_2["cost"].values[0]} per drink at bar. So just kick your feet up and relax with a {alt_2}.
				""")

		if len(alt_sample["strdrink"])>=3:
			if alt_sample["strdrink"].values[2]!=featured_drink["strdrink"].values[0]:
				alt_3=alt_sample["strdrink"].values[2]
				alt_drink_3=alt_sample[alt_sample["strdrink"]==alt_3]
				ingredients_list_3 = alt_drink_3["ingredients_list"].values[0].split(",")
				proportions_list_3 = alt_drink_3["proportions_list"].values[0].split(",")
				with st.expander(f"{alt_3}"):
					st.write(f"""I should have known that you don't like {name}. Well that's what the alternative drinks are for! I hope you'll like a {alt_3}
					For this one you need a **{alt_drink_3["strglass"].values[0]}** and these ingredients:
					""")
					for prop, ing in zip(proportions_list_3, ingredients_list_3):
						st.write(f"* {prop} {ing}")
					st.write(f"""
					A {alt_3} isn't too hard to make! Just follow these instructions:

					{alt_drink_3["strinstructions"].values[0]}

					${alt_drink_3["cost"].values[0]} per drink? Wow, that's a cheap and delicious cocktail!
					""")

		if len(alt_sample["strdrink"])>=4:
			if alt_sample["strdrink"].values[3]!=featured_drink["strdrink"].values[0]:
				alt_4=alt_sample["strdrink"].values[3]
				alt_drink_4=alt_sample[alt_sample["strdrink"]==alt_4]
				instructions_4 = alt_drink_4["strinstructions"].values[0]
				ingredients_list_4 = alt_drink_4["ingredients_list"].values[0].split(",")
				proportions_list_4 = alt_drink_4["proportions_list"].values[0].split(",")
				with st.expander(f"{alt_4}"):
					st.write(f"""Now we're talking! My favorite cocktail: {alt_4}! No one likes a {name} anyways, 
					we should really get that out of our database.
					{alt_4} are simple you'll need a **{alt_drink_4["strglass"].values[0]}** and these exact ingredients:
					""")
					for prop, ing in zip(proportions_list_4, ingredients_list_4):
						st.write(f"* {prop} {ing}")
					st.write(f"""
					With those ingredients just follow these steps, and presto a {alt_4}!

					{alt_drink_4["strinstructions"].values[0]}

					At home is always cheaper and when its only ${alt_drink_4["cost"].values[0]} per drink, the addage continues to hold!
					""")

		if len(alt_sample["strdrink"])>=5:
			if alt_sample["strdrink"].values[4]!=featured_drink["strdrink"].values[0]:
				alt_5=alt_sample["strdrink"].values[4]
				alt_drink_5=alt_sample[alt_sample["strdrink"]==alt_5]
				ingredients_list_5 = alt_drink_5["ingredients_list"].values[0].split(",")
				proportions_list_5 = alt_drink_5["proportions_list"].values[0].split(",")
				with st.expander(f"{alt_5}"):
					st.write(f"""This is your last choice you have! You better like a {alt_5}, it's definitely better than a {name}
					First you will have to find a **{alt_drink_5["strglass"].values[0]}** and these ingredients:
					""")
					for prop, ing in zip(proportions_list_5, ingredients_list_5):
						st.write(f"* {prop} {ing}")
					st.write(f"""
					No need to just throw the ingredients together. Follow these steps and you'll have a {alt_5}!

					{alt_drink_5["strinstructions"].values[0]}

					${alt_drink_5["cost"].values[0]} per drink? Imagine ordering that at a bar it would cost double maybe even triple that!
					""")

with st.container():
	st.write("""
	All data is sourced from the [Cocktail Database](https://www.thecocktaildb.com/). This dashboard was created with the free to use platform [Streamlit](https://streamlit.io/). For any inquiries on the coding or the structure of this project connect to our [GitHub](https://github.com/ElliottMetzler/the-manhattan-project). Enjoy your drinks!
	""")