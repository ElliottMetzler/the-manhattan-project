import pandas as pd
from quant_preprocess import query_and_preprocess_data

df = query_and_preprocess_data()


def summmary_of_oz(df):
   
    return df.describe().transpose().sort_values('mean',
                                ascending = False).head(10)

def create_dummies(df):
    
    headers = df.columns[1:]
    d = {'strdrink': df['strdrink'].values.tolist()}
    for e in range(0, len(headers)):
        d[headers[e]] = (df[str(headers[e])] > 0).astype(int).values.tolist()
    return pd.DataFrame.from_dict(d)
    

# still working on this, i dont want to have to make two dicts
def summary_of_usage():
    
    dum_df = create_dummies(df)
    headers = df.columns[1:].values.tolist()
    data = dum_df.describe().transpose().sort_values('mean', 
                                    ascending=False).head(10)
    data['total'] = ''
    
    for e in headers:
        data.loc[e, data['total']] = dum_df.transpose().loc[[e]].sum(axis=1)
        
    return data
    