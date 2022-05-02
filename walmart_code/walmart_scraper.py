import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

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


# the actual file is on a different branch so ill replace this github link with the csv once this is there
url_file = 'https://raw.githubusercontent.com/ElliottMetzler/the-manhattan-project/get_data/data/ingredients.csv'
ingredients = pd.read_csv(url_file, header=None)


cookie = 'U=e33b391aebc7946c7f4ae8b7b120d8e5; s=b09113a20b79b2bdde3523b9467cdd73'
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
    """ Takes the ingredient searches and outputs the first option's price/oz"""
    soup = searches[0]
    ingredient = searches[1]
    prices = []
    price_dict = {}
        for s in range(len(soup)):
        page_results = s.find('div', {'class': 'flex flex-wrap justify-start items-center lh-title mb2 mb1-m'})
        for p in page_results:
            price_oz = p.find('div', {'class': 'f7 f6-l gray mr1'}).text
            price_dict[ingredient[s]] = price_oz
    return price_dict
