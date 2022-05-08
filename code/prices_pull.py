import pandas as pd
from pandas import json_normalize
import requests
import json
import csv
import os
import re
params = {
    'api_key':'4F60666AD7F14FE49237DE1B9E2FB925',
    'type':'search',
    'sort_by': 'best_seller',
}
INGRED_PATH = 'https://raw.githubusercontent.com/ElliottMetzler/the-manhattan-project/main/data/ingredients_data_raw.csv'
OUT_DIR = "data"
JSON_PATH = os.path.join(OUTPUT_DIR, 'items.txt')

###notes:
# have done indexes0:3, salt(find the index), and 200:296 - total: 100
# need to buy the membership or get more emails to get more5



def load_ingredients(path):
    """Loads the list of ingredients to a list"""
    #i'm gonna change the path to the file that we have and the function will be less dumb

    ingredients = pd.read_csv(INGRED_PATH, header = None)[200:296]
    return ingredients[0].values.tolist()



def get_item_jsons(params):
    """Loops though a list of ingredients and outputs a list of jsons."""

    json_list = []
    ingredients = load_ingredients(INGRED_PATH)
    for i in ingredients:
        params['search_term'] = i
        result = requests.get('https://api.bluecartapi.com/request',
                                      params)
        json_list.append(json.dumps(result.json()))
    return json_list


def json_to_text(jsons, path):
    """Takes the list of jsons and writes them to a text file."""

    f = open(path, "w+")
    for i in jsons:
        f.write(i + "\n")
    f.close()




if __name__ == '__main__':

    json_to_text(jsons, JSON_PATH)

