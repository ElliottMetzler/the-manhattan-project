import streamlit as st
import pandas as pd
from database import engine
from query_funcs import main_query
from query_funcs import get_ingredients_list

# Import comprehensive list of ingredients
ingredients_list = get_ingredients_list()

# Functions
def gen_ingredient_selectbox(num):
	"""Function accepts a number and creates a selectbox"""
	prompt = f"Ingredient Selection {num}"
	return st.sidebar.selectbox(prompt, ingredients_list)


def gen_ingredients_slider():
	"""Function accepts no parameters and creates a slider"""
	prompt = f"Select the maximum number of ingredients you would like in your cocktail"

	return st.sidebar.slider(prompt, 2, 12)

def gen_ingredient_selection_slider(total_ingredients):
	"""Function accepts a total ingredients parameter which specifies how many incredients in the cocktail. and creates slider for the number of ingredients the user would like to say they have handy"""

	# Can't input more desired ingredients than total in cocktail
	# Max at three desired ingredients.
	max_ = min(total_ingredients, 3)

	prompt = f"Select how many ingredients you would like to use to filter your cocktail query"
	return st.sidebar.slider(prompt, 1, max_)


###########################################################
# Streamlit Code
###########################################################

st.set_page_config(layout="wide")

st.header("The Manhattan Project")

col1, col2 = st.columns(2)

#######################################
# Side Bar Selections
#######################################

# First, select the number of ingredients with a min of 2
num_ingredients_tot = gen_ingredients_slider()
# Next, select an ingredient
ingredient_1 = gen_ingredient_selectbox(1)

#######################################
# First Column
#######################################

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

col2.header("Featured Drink Result")

df = main_query(num_ingredients_tot)
df = df[df["ingredients_list"].str.contains(ingredient_1)]

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


#######################################
# Archive
#######################################

"""
# Next, select the number of ingredients you'd like to use in your filter
num_ingredients_filter = gen_ingredient_selection_slider(num_ingredients_tot)

# Depending on the output, generate a number of select boxes
# Also generate the masks to filter the output
if num_ingredients_filter == 1:
	ingredient_1 = gen_ingredient_selectbox(1)

elif num_ingredients_filter == 2:
	ingredient_1 = gen_ingredient_selectbox(1)
	ingredient_2 = gen_ingredient_selectbox(2)

else:
	ingredient_1 = gen_ingredient_selectbox(1)
	ingredient_2 = gen_ingredient_selectbox(2)
	ingredient_3 = gen_ingredient_selectbox(3)
"""