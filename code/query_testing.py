import pandas as pd
from database import engine


# Just a proof of concept script for how we will query out from the database

query_1 = """
select
	strdrink,
	strinstructions
from
	all_cocktails;
"""


df = pd.read_sql_query(query_1, engine)

print(df.head())
