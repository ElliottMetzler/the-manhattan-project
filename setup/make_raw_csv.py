from pandas import json_normalize
import requests
import pandas as pd
import string

def create_raw_data(BASE_URL):

    ALPHA = list(string.ascii_lowercase)
    NUM = list(string.digits)
    NUM.extend(ALPHA)
    NUM.remove("0")
    NUM.remove("8")

    page_links = []

    for n in NUM:
        url = '{}{}'.format(BASE_URL, n)
        page_links.append(url)
    
    list_of_pages = []
    for url in page_links:
        response = requests.get(url)
        response.raise_for_status()
        response_json = response.json()
        list_of_pages.append(response_json["drinks"])


    normalize = json_normalize(list_of_pages)
    df = pd.DataFrame(normalize)
    raw_data = pd.DataFrame(df.stack().apply(pd.Series))

    raw_data.reset_index(drop=True, inplace=True)
    
    return raw_data
