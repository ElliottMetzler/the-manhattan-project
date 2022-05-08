import pandas as pd
from pandas import json_normalize
import requests
import json
import csv
import os
import re


IN_FILE_PATH(****)
OUT_DIR = "data"
OUT_PATH = os.path.join(OUTPUT_DIR, 'ingredient_prices.csv')



def read_txt_as_json():
    
    
    j_list = []
    
    with open("..//data//item_jsons.txt") as text:
        
        json_list = [line.rstrip("\n") for line in text]

        for j in json_list:
            j_list.append(json.loads(j))
        
        return j_list


 def get_product_info():
        
        j_list = read_txt_as_json()
        product_dict = {}
        measurements = [" oz", "ml", " lb", " l", " ounces", " gal"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9","0", "."]
    
        for j in j_list:

            amount_temp = []
            units_temp = []
            price_temp = []
            l = []
            ingredient = j["request_parameters"]["search_term"]
            key = ingredient
            product_dict.setdefault(key, [])
            results = j["search_results"]

            for r in results:

                numbers_temp = []
                title = r["product"]["title"]
                if (ingredient in title.lower()):

                    price = r["offers"]["primary"]["price"]
                    print(price)

                    price_temp.append(price)
                    print(price_temp)

                    print(title)

                    for m in measurements:
                        if m in title.lower():
                            units_temp.append(m.strip())                                

                    for t in title[-15:-1]:
                        for n in numbers:
                            if t == n:
                                numbers_temp.append(n)
                            else:
                                continue

                    amount_temp.append(''.join(numbers_temp))


            product_dict[key].append(price_temp)
            product_dict[key].append(amount_temp)
            product_dict[key].append(units_temp)


            print(price_temp)
            print(units_temp)
            print(amount_temp)

            print(product_dict)
        return product_dict


def to_csv(price_dict, path):
""" Takes the list of (ingredient, price/oz) tuples and writes them to a csv"""
#this is from my old scraper so just a placeholder

    with open(OUT_PATH, 'w+') as out_file:
        csv_writer = csv.writer(out_file)
        header = ['ingredient', 'price_per_oz']
        csv_writer.writerow(header)
        csv_writer.writerows(price_dict)


if __name__ == '__main__':

    os.makedirs(OUT_DIR, exist_ok = True)
    to_csv(item_dict, OUT_PATH)
