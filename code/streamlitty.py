import streamlit as st
import pandas as pd
from database import engine
from streamlit_query_functions import main_query
from streamlit_query_functions import get_ingredients_list

# Import comprehensive list of ingredients
ingredients_list = get_ingredients_list()
ingredients_list.insert(0, "N/A")

# Functions
def gen_ingredient_selectbox():
	"""Function Creates a broad ingredient selectbox"""
	prompt = f"Other Ingredient Selection:"
	return st.sidebar.selectbox(prompt, ingredients_list)


def gen_ingredients_slider():
	"""Function accepts no parameters and creates a slider"""
	prompt = f"Select the maximum number of ingredients you would like in your cocktail"

	return st.sidebar.slider("", 2, 12)


###########################################################
# Streamlit Code
###########################################################

st.set_page_config(layout="wide")

st.header("The Manhattan Project")

col1, col2 = st.columns(2)

#######################################
# Side Bar Selections
#######################################
st.sidebar.write("""Once you select all of your drink specifications click here:""")
button=st.sidebar.button("Find My Drink")

# First, select the number of ingredients with a min of 2
st.sidebar.write("""
	# Ingredients:
	First, select the *maximum* number of ingredients you'd like in your cocktail""")
num_ingredients_tot = gen_ingredients_slider()

# Select some main Boozes as ingredients
st.sidebar.write("""
	# Main Liquors:
	Next, select some of the main booze options you have handy or would like to use in your cocktail.""")

vodka = st.sidebar.checkbox("Vodka")
whiskey = st.sidebar.checkbox("Whiskey")
tequila = st.sidebar.checkbox("Tequila")
gin = st.sidebar.checkbox("Gin")
rum=st.sidebar.checkbox("Rum")

# Next, select another ingredient

st.sidebar.write("""
	# Other Ingredient:
	Finally, select another ingredient you'd like to include in your cocktail""")
alt_ingredient = gen_ingredient_selectbox()


#######################################
# First Column
#######################################
with st.container():
	col1.header("Welcome to our Page")

	col1.write("""
		Hello! Welcome to The Manhattan Project. This webpage is designed to help fuel Friday night. We get it, you've had a long week, you don't want to go to the store, and you sure as hell don't want to think too hard about what you want to drink to unwind tonight. That's where we come in. 
		With our site, you can search through a vast database of cocktails and concoctions using a variety of search parameters and settings to find exactly what you're looking for - whether thats a night in with a movie and a bowl of popcorn, a night out with some strangers, or a Saturday morning tailgate.
		How to use: First, you will use the side panel on to select a search setting. We currently support a few options. You can search by glass type, which is often indicative of the type of drink (i.e. shot glass or punch bowl ought to produce a nice party). Alternatively, you can search by an ingredient you have on hand and would like to use up, with a filter for the number of ingredients in the cocktail. We also support a combination of the two previous search options. Finally, we can generate a completely random drink.
		The panel to the right will display the featured result based on your search. Below, we also list other cocktails that fit the search parameters (if they exist), and allow you to select if you'd like to view another option.
		""")

	#######################################
	# Second Column
	#######################################
	df=[]
	if button:
		col2.header("Featured Drink Result")

		# Query Database and filter based on criteria
		df = main_query(num_ingredients_tot)

		# Create Contains (Or) based on Main Boozes
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

		# If none are selected, don't filter
		if len(booze_criteria) > 0:
			booze_mask = df["ingredients_list"].str.contains("|".join(booze_criteria))
		else:
			booze_mask = pd.Series([True] * len(df.index))

		# If N/A is selected, don't filter
		if alt_ingredient != "N/A":
			alt_ingredient_mask = df["ingredients_list"].str.contains(alt_ingredient)
		else:
			alt_ingredient_mask = pd.Series([True] * len(df.index))

		# Perform data filtering
		df = df[booze_mask & alt_ingredient_mask]

		# Sample a random drink from the list
		if len(df["strdrink"])>0:
			featured_drink = df.sample(1)

			name = featured_drink["strdrink"].values[0]
			glass = featured_drink["strglass"].values[0]
			instructions = featured_drink["strinstructions"].values[0]
			image = featured_drink["strdrinkthumb"].values[0]

			ingredients_list = featured_drink["ingredients_list"].values[0].split(",")
			proportions_list = featured_drink["proportions_list"].values[0].split(",")

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
				If it looks anything like this, you're probably in good shape!
				""")

			col2.image(image)

			col2.write("Cheers!")
		else:
			col2.write("""There are no unique cocktails that follow your drink specifications. Try changing the maximum number of ingredients, selecting a different liquor, or choosing a different specified ingredient.""")
with st.container():
	alt_sample=[]
	alt_1=[]
	alt_2=[]
	alt_3=[]
	alt_4=[]
	alt_5=[]
	if button:
		if len(df["strdrink"])>5:
			alt_sample=df.sample(5)
		else:
			alt_sample=df

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
					""")

with st.container():
	st.write("""
	All data is sourced from the [Cocktail Database](https://www.thecocktaildb.com/). This dashboard was created with the free to use platform [Streamlit](https://streamlit.io/). For any inquiries on the coding or the structure of this project connect to our [GitHub](https://github.com/ElliottMetzler/the-manhattan-project). Enjoy your drinks!
	""")