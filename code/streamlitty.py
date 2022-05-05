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
mezcal = st.sidebar.checkbox("Mezcal")
gin = st.sidebar.checkbox("Gin")
rum= st.sidebar.checkbox("Rum")

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
	df = []
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
		if mezcal:
			booze_criteria.append("mezcal")
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
with st.container():
	col1,col2=st.columns(2)
	col1.header("""If you aren't feeling our featured cocktail maybe one of these would be more your speed:""")
	alt_sample=df.sample(5)
	alt_1=alt_sample["strdrink"].values[0]
	alt_2=alt_sample["strdrink"].values[1]
	alt_3=alt_sample["strdrink"].values[2]
	alt_4=alt_sample["strdrink"].values[3]
	alt_5=alt_sample["strdrink"].values[4]
	option1=col1.checkbox(f"Option 1: {alt_1}")
	option2=col1.checkbox(f"Option 2: {alt_2}")
	option3=col1.checkbox(f"Option 3: {alt_3}")
	option4=col1.checkbox(f"Option 4: {alt_4}")
	option5=col1.checkbox(f"Option 5: {alt_5}")

	option5 = True

	if option1:
		alt_drink=alt_sample[alt_sample["strdrink"]==alt_1]
	if option2:
		alt_drink=alt_sample[alt_sample["strdrink"]==alt_2]
	if option3:
		alt_drink=alt_sample[alt_sample["strdrink"]==alt_3]
	if option4:
		alt_drink=alt_sample[alt_sample["strdrink"]==alt_4]
	if option5:
		alt_drink=alt_sample[alt_sample["strdrink"]==alt_5]


	
	if option1 or option2 or option3 or option4 or option5:
		alt_name = alt_drink["strdrink"].values[0]
		alt_glass = alt_drink["strglass"].values[0]
		alt_instructions = alt_drink["strinstructions"].values[0]
		alt_image = alt_drink["strdrinkthumb"].values[0]

		alt_ingredients_list = alt_drink["ingredients_list"].values[0].split(",")
		alt_proportions_list = alt_drink["proportions_list"].values[0].split(",")

		col2.write(f"""
			
		Congratulations! You have selected the **{alt_name}**!

		First, you will need to get out a **{alt_glass}**.

		Next, grab the following ingredients:
		"""
		)

		for prop, ing in zip(alt_proportions_list, alt_ingredients_list):
			col2.write(f"* {prop} {ing}")

		col2.write(f"""
			Finally, here are the instructions to make your cocktail!

			{alt_instructions}

			If it looks anything like this, you're probably in good shape!

			""")

		col2.image(alt_image)

		col2.write("Cheers!")
		



