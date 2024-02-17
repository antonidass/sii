from recommend import *
from filter import get_share_id_by_name
from read_write_data import get_data_from_json, write_data_to_json

array_likes = []
array_dislikes = []

def get_recommend_shares():
	like_shares, dislike_shares, shares = recommend(array_likes, array_dislikes)
	return like_shares, dislike_shares, shares


def add_like(share_name):
	like_share_id = get_share_id_by_name(share_name)
	array_likes.append(like_share_id)
	like_shares, dislike_shares, shares = recommend(array_likes, array_dislikes)
	return like_shares, dislike_shares, shares

def remove_like(share_name):
	like_share_id = get_share_id_by_name(share_name)
	if like_share_id in array_likes:
		array_likes.remove(like_share_id)
	like_shares, dislike_shares, shares = recommend(array_likes, array_dislikes)
	return like_shares, dislike_shares, shares

def add_dislike(share_name):
	dislike_share_id = get_share_id_by_name(share_name)
	array_dislikes.append(dislike_share_id)
	like_shares, dislike_shares, shares = recommend(array_likes, array_dislikes)
	return like_shares, dislike_shares, shares

def remove_dislike(share_name):
	like_share_id = get_share_id_by_name(share_name)
	array_dislikes.remove(like_share_id)
	like_shares, dislike_shares, shares = recommend(array_likes, array_dislikes)
	return like_shares, dislike_shares, shares
