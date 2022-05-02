import streamlit as st
import pandas as pd
from database import engine
from query_funcs import query_table_1

# Booze List for selector
boozes = ["Gin",
	"Vodka",
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

HEADER_1 = "# My Drinks Table"
HEADER_2 = "# My Drinks Analysis"

st.write(HEADER_1)

# Add a selectbox to the sidebar:
primary_booze_selection = st.sidebar.selectbox(
	"What kind of booze ya got?",
	boozes
)

# Add a slider to the sidebar:
num_ingredients_selection = st.sidebar.slider(
	"Select the Number of Ingredients Available",
	1, 10
)

# Add drink output table  using function from query_funcs.
table_1_df = query_table_1(primary_booze_selection,num_ingredients_selection)

st.dataframe(table_1_df,
	width = 1600,
	height = 1000)


st.write(HEADER_2)