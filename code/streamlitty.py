import streamlit as st
import pandas as pd
from database import engine

# full_query = """
# select *
# from all_cocktails;
# """

# full_df = pd.read_sql_query(full_query, engine)

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
add_slider = st.sidebar.slider(
	"Select the Number of Ingredients Available",
	0, 10
)

st.write(f"You Chose {primary_booze_selection} for your booze and {add_slider} for your ingredient count.")


query1 = f"""
select 
	strdrink,
	strinstructions
from all_cocktails
where stringredient1 = '{primary_booze_selection}';
"""

df = pd.read_sql_query(query1, engine)
st.write(df)

st.write(HEADER_2)