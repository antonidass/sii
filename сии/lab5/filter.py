from read_write_data import load_data, get_data_from_ods

def init_shares(data, num_shares):
	shares = []

	for i in range(num_shares):
		shares.append(data.iloc[i])

	return shares


def get_share_id_by_name(share_name):
	data = get_data_from_ods("./shares2.ods")
	idx = -1
	num_shares = data.shape[0]
	print("IN FIND = ", data['Компания'])
	for i in range(num_shares):
		cur_share = data.iloc[i]
		if cur_share['Компания'] == share_name:
			idx = i
			break
	return idx


def get_share_by_name(data, name):
	res_share = None

	num_shares = data.shape[0]
	for i in range(num_shares):
		cur_share = data.iloc[i]
		if cur_share['Компания'] == name:
			res_share = cur_share
			break

	return res_share


def get_shares_by_contry(full_shares, ctr):
	res_shares = []

	for share in full_shares:
		if share['Страна'] == ctr:
			res_shares.append(share)

	return res_shares

def get_shares_by_risk(full_shares, risk):
	res_shares = []
	for share in full_shares:
		if risk == "Низкий":
			if share['Риск'] < 30:
				res_shares.append(share)
		elif risk == "Средний":
			if share['Риск'] >= 31 and share['Риск'] < 60:
				res_shares.append(share)
		elif risk == "Высокий":
			if share['Риск'] >= 61 and share['Риск'] <= 100:
				res_shares.append(share)
	return res_shares


def get_shares_by_div(full_shares, have_divs):
	res_shares = []

	div = "Нет"
	if have_divs:
		div = "Да"

	for share in full_shares:
		if share['Наличие дивидендов'] == div:
			res_shares.append(share)

	return res_shares


def define_similar_contry(contry):
	similar_contry = contry

	if contry == "США": similar_contry = "Китай"
	if contry == "Россия": similar_contry = "Беларусь"
	if contry == "Казахстан": similar_contry = "Россия"
	if contry == "Беларусь": similar_contry = "Казахстан"
	if contry == "Китай": similar_contry = "США"

	return similar_contry


def get_shares_by_another_filter(data, contry, have_divs, risk):
	shares = init_shares(data, data.shape[0])

	if contry != 'Страна':
		contry = define_similar_contry(contry)
		shares = get_shares_by_contry(shares, contry)

	if have_divs != None:
		shares = get_shares_by_div(shares, have_divs)

	if risk != 'Риск':
		shares = get_shares_by_risk(shares, risk)

	return shares


def find_shares_by_filters(name, contry, have_divs, risk):
	
	print("params = ", name, contry, have_divs, risk)
	data, nodes, data_fact = load_data()
	another_filter = False

	if name and name != "":
		share = get_share_by_name(data, name)
		if type(share) == type(None):
			return None, False
		
		shares = [share]
		return shares, another_filter

	shares = init_shares(data, data.shape[0])
	print(len(shares))
	if contry != 'Страна' and contry != None:
		shares = get_shares_by_contry(shares, contry)
	print(len(shares))

	if have_divs != None:
		shares = get_shares_by_div(shares, have_divs)
	print(len(shares))

	if risk != 'Риск':
		shares = get_shares_by_risk(shares, risk)
	print(len(shares))

	if len(shares) == 0:
		another_filter = True
		shares = get_shares_by_another_filter(data, contry, have_divs, risk)

	return shares, another_filter
