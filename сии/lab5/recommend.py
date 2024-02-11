import os
import itertools
import numpy as np
import pandas as pd
from tabulate import tabulate

from read_write_data import load_data
from measures import *

limit = 6

# Получить массив близости с входной бумагой
def get_measures_for_share(data_fact, rating, array_rating, array_disrating):
	share = data_fact.iloc[rating]
	measures = []
	num_shares = data_fact.shape[0]
	for i in range(num_shares):
		if (i in array_rating or i in array_disrating):
			continue
		cur_share = data_fact.iloc[i]
		measure = Minkowski_measure(0.5, share, cur_share)
		measures.append([measure, i])
	measures.sort()
	return measures

# Получаем массив мер для всех лайков (берем минимальную меру)
def get_measures_by_rating(data_fact, array_rating, array_disrating):
	measures = []
	for rating in array_rating:
		cur_measures = get_measures_for_share(data_fact, rating, array_rating, array_disrating)
		if (not measures):
			measures = cur_measures
		else:
			for i in range(len(measures)):
				if measures[i][0] > cur_measures[i][0]:
					measures[i] = cur_measures[i]
	return measures

def match_data_with_fact_data(data, measures):
	shares = []
	for i in range(len(measures)-1):
		cur_idx = measures[i][1]
		next_idx = measures[i+1][1]
		if cur_idx == next_idx:
			continue
		shares.append(data.iloc[cur_idx])
	shares.append(data.iloc[len(measures)-1])
	return shares

def recommend(array_likes, array_dislikes):
	data, nodes, data_fact = load_data()

	like_measures = get_measures_by_rating(data_fact, array_likes, array_dislikes)
	dislike_measures = get_measures_by_rating(data_fact, array_dislikes, array_likes)
	
	like_shares = []
	for like in array_likes:
		like_share = data.iloc[like]
		like_shares.append(like_share)

	dislike_shares = []
	for dislike in array_dislikes:
		dislike_share = data.iloc[dislike]
		dislike_shares.append(dislike_share)

	if len(like_measures) == 0:
		if dislike_measures:
			dislike_max_measure = dislike_measures[-1]
			for i in range(len(dislike_measures)):
				dislike_measures[i][0] = dislike_max_measure[0] - dislike_measures[i][0]	
			shares = match_data_with_fact_data(data, list(reversed(dislike_measures)))
			return like_shares, dislike_shares, shares

	if (len(dislike_measures) > 0):
		res_measures = []
		for i in range(len(like_measures)):
			for j in range(len(dislike_measures)):
				if like_measures[i][1] == dislike_measures[j][1]:
					if like_measures[i][0] <= dislike_measures[j][1]:
						res_measures.append(like_measures[i])
		shares = match_data_with_fact_data(data, res_measures)
		return like_shares, dislike_shares, shares

	shares = match_data_with_fact_data(data, like_measures)
	return like_shares, dislike_shares, shares