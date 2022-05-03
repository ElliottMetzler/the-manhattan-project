import streamlit as st
import pandas as pd
from database import engine
from query_funcs import query_table_1

# Booze List for selector (need to expand this)
boozes = [
	"Vodka",
	"Gin",
	"Whiskey",
	"Bourbon",
	"Rye",
	"Scotch",
	"Tequila",
	"Mezcal",
	"White Rum",
	"Golden Rum",
	"Dark Rum",
	"Brandy",
	"Cognac",
	"Amaretto"]

# Streamlit Code

# Add a selectbox to the sidebar:
primary_booze_selection = st.sidebar.selectbox(
	"What kind of booze do you have handy?",
	boozes
)

# Add a slider to the sidebar:
num_ingredients_selection = st.sidebar.slider(
	"Select the Number of Ingredients Available",
	2, 10
)


HEADER_1 = "# My First Drink"
st.write(HEADER_1)

first_drink = query_table_1(primary_booze_selection,num_ingredients_selection)

name = first_drink["strdrink"].values[0]
glass = first_drink["strglass"].values[0]
instructions = first_drink["strinstructions"].values[0]
ingredients_list = first_drink["ingredients_list"].values[0]
proportions_list = first_drink["proportions_list"].values[0]

st.write(f"""
	
Congratulations! You have selected the **{name}**!

First, you will need to get out a **{glass}** and the following ingredients: {ingredients_list}.

Here are the instructions to make the drink:

{instructions}


Cheers!
"""
)

