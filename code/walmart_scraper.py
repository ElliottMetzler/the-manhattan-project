import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import os
import re


# the actual file is on a different branch so ill replace this github link with the csv once this is there
INGRED_PATH = 'https://raw.githubusercontent.com/ElliottMetzler/the-manhattan-project/get_data/data/ingredients.csv'
OUT_DIR = "data"
JSON_PATH = os.path.join(OUT_DIR, 'items.txt')
OUT_PATH = os.path.join(OUTPUT_DIR, 'ingredient_prices.csv')


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
'Accept': '*/*',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Origin': 'https://www.walmart.com',
'Connection': 'keep-alive',
'Referer': 'https://www.walmart.com/',
'Cookie': 'U=e33b391aebc7946c7f4ae8b7b120d8e5; s=b09113a20b79b2bdde3523b9467cdd73',
'TE': 'trailers',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'cross-site'}


def load_ingredients(path):
    """ Loads the list of ingredients to a dataframe """

    ingredients = pd.read_csv(INGRED_PATH, header = None)
    return ingredients[0:50]



def get_wm_search(query):
""" Takes a word and returns the search page on Walmart's website"""

    url = "https://www.walmart.com/search?q="+query
    page = requests.get(url, headers=header)
    if page.status_code == 200:
        return page
    else:
        return "Error"


def get_item_searches(ingredients):
    """ Takes the list of ingredients and makes a list of soups."""

    queries = []
    search_list = []
    llist = []
    for i in ingredients:
        response = get_wm_search(i)
        soup = BeautifulSoup(response.content)
        search_list.append(soup)
        queiries.append(i)
    return llist.extend([search_list, queiries])



def get_page_prices(searches):
    """ Takes the ingredient searches and outputs the first option's price/oz. Outputs (ingredient, price) tuples."""

    soup_list = searches[0]
    ingredient_list = searches[1]
    price_list = []
    price_dict = {}
        for s in range(len(soup_list)):
        page_results = soup_list[s].find('div', {'class': 'flex flex-wrap justify-start items-center lh-title mb2 mb1-m'})
        for p in page_results:
            price_oz = p.find('div', {'class': 'f7 f6-l gray mr1'}).text
            price_dict[ingredient_list[s]] = price_oz
    return price_dict


def to_csv(price_dict, path):
""" Takes the list of (ingredient, price/oz) tuples and writes them to a csv"""

    with open(OUTPUT_PATH, 'w+') as out_file:
        csv_writer = csv.writer(out_file)
        header = ['ingredient', 'price_per_oz']
        csv_writer.writerow(header)
        csv_writer.writerows(price_dict)


if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok = True)
    ingredients = load_ingredients(INGRED_PATH)
    ingredient_llist = get_item_searches(ingredients)
    price_dict = get_page_prices(ingredient_llist)
    to_csv(price_dict, OUTPUT_PATH)



