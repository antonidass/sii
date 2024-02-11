from pandas_ods_reader import read_ods
from tabulate import tabulate
import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

ods_path = "./shares2.ods"
json_path = "./Nodes.json"
html_path = "./Table.html"
tree_path = "./Tree.json"
# shares_path = "./shares2.ods"


def get_shares_list():
     data = read_ods(ods_path, 1, headers=True)
     arr_shares = data['Компания'].values
     return arr_shares

def get_data_from_ods(ods_path):
    data = read_ods(ods_path, 1, headers=True)
    data.index = data.index + 1
    return data


def get_data_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data


def write_data_to_json(json_path, json_data):
    with open(json_path, "w") as outfile:
        json.dump(json_data, outfile)


def write_data_to_html(data, html_path):
    f = open(html_path, 'w')
    f.write(tabulate(data, headers="keys", tablefmt='html'))


def factorize_data(data, nodes):
	del data['Компания']

	# Факторизация на основе корреляционной матрицы для секторов
	sectors = data['Тип'].str.split(',', 1).str
	data['Тип'] = sectors[0]
	
	themes_list = nodes['Тип']
	themes_corr = nodes['Тип.Корреляция']

	for i in range(len(themes_list)):
		data[themes_list[i]] = data['Тип'].map(lambda e: themes_corr[i][themes_list.index(e)])
	del data['Тип']
	
	crafts = nodes['Акции']
	data['Сектор'], unique = pd.factorize(data['Сектор'], na_sentinel=0)
	data['Сектор'] = np.where((data['Сектор'] == 0), 0, data['Сектор'] / len(crafts))

	ctrs = nodes['Страна']
	data['Страна'], unique = pd.factorize(data['Страна'], na_sentinel=0)
	data['Страна'] = np.where((data['Страна'] == 0), 0, data['Страна'] / len(ctrs))

	ctrs = nodes['Стабильность']
	data['Стабильность'], unique = pd.factorize(data['Стабильность'], na_sentinel=0)
	data['Стабильность'] = np.where((data['Стабильность'] == 0), 0, data['Стабильность'] / len(ctrs))
		
	ctrs = nodes['Наличие дивидендов']
	data['Наличие дивидендов'], unique = pd.factorize(data['Наличие дивидендов'], na_sentinel=0)
	data['Наличие дивидендов'] = np.where((data['Наличие дивидендов'] == 0), 0, data['Наличие дивидендов'] / len(ctrs))
		
	ctrs = nodes['Тип облигации']
	data['Тип облигации'], unique = pd.factorize(data['Тип облигации'], na_sentinel=0)
	data['Тип облигации'] = np.where((data['Тип облигации'] == 0), 0, data['Тип облигации'] / len(ctrs))

	ctrs = nodes['Тип опциона']
	data['Тип опциона'], unique = pd.factorize(data['Тип опциона'], na_sentinel=0)
	data['Тип опциона'] = np.where((data['Тип опциона'] == 0), 0, data['Тип опциона'] / len(ctrs))

	data['Средний возраст владельцев'] = data['Средний возраст владельцев'].values / max(data['Средний возраст владельцев'].values)	

	data['Срок'] = data['Срок'].values / max(data['Срок'].values)
	data['P/E'] = data['P/E'].values / max(data['P/E'].values)
	data['ROE, %'] = data['ROE, %'].values / max(data['ROE, %'].values)
	data['Цена, руб'] = data['Цена, руб'].values / max(data['Цена, руб'].values)
	data['Риск'] = data['Риск'].values / max(data['Риск'].values)

	data.to_excel("after_factorize.xlsx")

	return data



def load_data():
    data = get_data_from_ods(ods_path)
    nodes = get_data_from_json(json_path)
    data_fact = factorize_data(data.copy(deep=True), nodes)

    return data, nodes, data_fact
