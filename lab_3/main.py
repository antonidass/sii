import os
import itertools
import numpy as np
import pandas as pd
from tabulate import tabulate

from read_write_data import *
from measures import *


ods_path = "./shares2.ods"
json_path = "./Nodes.json"
html_path = "./Table.html"
tree_path = "./Tree_more_cities.json"


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

	data.to_excel("after_factorize.xlsx")

	print(data)

	return data


def get_measures(object1, object2, tree):
	print('Евклидово расстояние:\t\t', Euclidean_measure(object1, object2))
	print('Расстояние городских кварталов:\t', City_block_distance(object1, object2))
	print('Косинусная мера:\t\t', Cosine_measure(object1, object2))
	print('Расстояние Чебышева:\t\t', Chebyshev_measure(object1, object2))
	print('Расстояние Минковского (p=0.5):\t', Minkowski_measure(0.5, object1, object2))
	print('Ассоциативная мера:\t\t', Associative_measure(object1, object2))
	print('Мера Жаккарда:\t\t\t', Jaccard_measure(object1, object2))
	print('Древесная мера:\t', Tree_measure(tree, object1, object2))


def get_correlation(object1, object2):
	correlation = np.corrcoef(object1, object2)[0, 1]
	if abs(correlation) < 0.2:
		print('\nКорреляция (очень слабая): ', correlation)
	elif abs(correlation) < 0.5:
		print('\nКорреляция (слабая): ', correlation)
	elif abs(correlation) < 0.7:
		print('\nКорреляция (средняя): ', correlation)
	elif abs(correlation) < 0.9:
		print('\nКорреляция (высокая): ', correlation)
	else:
		print('\nКорреляция (очень высокая): ', correlation)



def main():
	os.system("clear")

	print(ods_path)

	data = get_data_from_ods(ods_path)
	print(data)

	nodes = get_data_from_json(json_path)
	tree = get_data_from_json(tree_path);
	#print(tabulate(data, headers="keys"))
	#print('\n')

	data_fact = factorize_data(data, nodes)

	write_data_to_html(data_fact, html_path)
	# print(tabulate(data_fact, headers="keys"))

	# 20 и 21 очень похожи яндекс и вк [6, 2, 0] и [6, 2, 0]
	# 2 и 40 очень разные сбер и сталь [8, 1, 0]] и [12, 3, 0]
	# 3 и 6 - средне похожие (акции) магнит и лукойл [8, 1, 0] и [10, 1, 0]
	Id1 = 20
	Id2 = 21

	Object1 = data_fact.iloc[Id1]
	Object2 = data_fact.iloc[Id2]

	# print("Бумага 1:\n", Object1)
	# print("Бумага 2:\n", Object2)

	get_measures(Object1, Object2, tree)
	get_correlation(Object1, Object2)

	matrix1 = get_correlation_matix(data_fact, Euclidean_measure)
	matrix2 = get_correlation_matix(data_fact, City_block_distance)
	matrix3 = get_correlation_matix(data_fact, Cosine_measure)
	matrix4 = get_correlation_matix(data_fact, Chebyshev_measure)
	matrix5 = get_correlation_matix(data_fact, Minkowski_measure)
	matrix6 = get_correlation_matix(data_fact, Associative_measure)
	matrix7 = get_correlation_matix(data_fact, Jaccard_measure)

	plot_matrices(matrix1, 'Евклидово расстояние', \
					matrix2, 'Расстояние городских кварталов', \
					matrix3, 'Косинусная мера', \
					matrix4, 'Расстояние Чебышева', \
					matrix5, 'Расстояние Минковского (p=0.5)', \
					matrix6, 'Ассоциативная мера', \
					matrix7, 'Мера Жаккарда')


if __name__ == "__main__":
	main()
