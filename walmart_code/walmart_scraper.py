import pandas as pd
import requests
from bs4 import BeautifulSoup

sq = 'salt'
url = 'https://www.walmart.com/search?q=+sq'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
'Accept': '*/*',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Origin': 'https://www.walmart.com',
'Connection': 'keep-alive',
'Referer': 'https://www.walmart.com/',
'Cookie': 's=93a1e136612fc2a290edf2020a2bc2f8; U=e33b391aebc7946c7f4ae8b7b120d8e5',
'TE': 'trailers',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'cross-site'}

def get_wm_search(query):
    url = "https://www.walmart.com/search?q="+sq
    page = requests.get(url, headers=header)
    if page.status_code == 200:
        return page
    else:
        return "Error"

def get_prod_link(soup):
    link_list = []
    link = soup.find_all('div', {'class': 'sans-serif mid-gray relative flex flex-column w-100'})
    for l in link:
        link_list.append('https://www.walmart.com'+l.a['href'])
    return link_list



response = get_wm_search('salt')
soup = BeautifulSoup(response.content)
links = get_prod_link(soup)
