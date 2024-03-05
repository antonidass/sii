from pandas_ods_reader import read_ods
import random

from main import parser

ods_path = "./shares2.ods"

with open("./shares.txt", encoding='utf-8') as file:
    shares_title = [row.strip() for row in file]

shares = read_ods(ods_path, 1, headers=True)
shares.index = shares.index + 1


def full_list():
    print('\nСписок доступных бумаг:')
    for share in shares_title:
        print(share)


def random_share():
    print('\n', shares.iloc[random.randint(0, 30)], '\n')


def find_share(title):
    num_shares = shares.shape[0]
    for i in range(num_shares):

        if shares.iloc[i]['Компания'].lower() == title.lower():
            print('\n', shares.iloc[i], '\n')
            return

    return -1


def output_all_shares(res_shares):
    for i in (res_shares):
        print('\n', i, '\n')
        print('---------------------\n')


def output_shares(phrase, selected_attributes):
    print(phrase, selected_attributes)
    count = 0
    num_shares = shares.shape[0]
    if (selected_attributes == 'Риск'):
        phrase_word = ' '.join(phrase)
        for i in range(num_shares):
            if phrase_word == "очень низкий":
                if shares.iloc[i][selected_attributes] <= 10:
                    count = 1
                    print('\n', shares.iloc[i], '\n')
                    print('---------------------\n')

            elif phrase_word == "низкий":
                if shares.iloc[i][selected_attributes] >= 11 and shares.iloc[i][selected_attributes] <= 30:
                    count = 1
                    print('\n', shares.iloc[i], '\n')
                    print('---------------------\n')

            elif phrase_word == "не очень низкий":
                if shares.iloc[i][selected_attributes] >= 31 and shares.iloc[i][selected_attributes] <= 40:
                    count = 1
                    print('\n', shares.iloc[i], '\n')
                    print('---------------------\n')

            elif phrase_word == "средний":
                if shares.iloc[i][selected_attributes] >= 41 and shares.iloc[i][selected_attributes] < 50:
                    count = 1
                    print('\n', shares.iloc[i], '\n')
                    print('---------------------\n')

            elif phrase_word == "не очень высокий":
                if shares.iloc[i][selected_attributes] >= 51 and shares.iloc[i][selected_attributes] <= 60:
                    count = 1
                    print('\n', shares.iloc[i], '\n')
                    print('---------------------\n')

            elif phrase_word == "высокий":
                if shares.iloc[i][selected_attributes] >= 61:
                    count = 1
                    print('\n', shares.iloc[i], '\n')
                    print('---------------------\n')
    else:

        for i in range(num_shares):
            if (shares.iloc[i][selected_attributes] and
                    shares.iloc[i][selected_attributes].lower() in set(phrase)):
                count = 1
                print('\n', shares.iloc[i], '\n')
                print('---------------------\n')

    if count == 0:
        print('\nТакого не существует...')


def text_values_share(phrase, tmp_shares, text_fields):
    res_shares = []

    intersection = set(phrase) & text_fields

    print(intersection)

    for i in tmp_shares:
        tmp_text_values = i["Тип"] + " "
        if i["Страна"] is not None:
            tmp_text_values += i["Страна"] + " "
        if i["Сектор"] is not None:
            tmp_text_values += i["Сектор"] + " "
        if i["Тип облигации"] is not None:
            tmp_text_values += i["Тип облигации"] + " "
        if i["Тип опциона"] is not None:
            tmp_text_values += i["Тип опциона"] + " "
        if len(set(parser(tmp_text_values)) &
               intersection) == len(intersection):
            res_shares.append(i)

    if len(res_shares) != 0:
        # print("if len(res_shares) != 0:")
        return res_shares, 1
    return tmp_shares, 0



def distance_share(phrase, tmp_shares):
    res_shares = []

    if ('не' in set(phrase) and 'очень' in set(phrase) and
            ('низко' in set(phrase) or 'низкий' in set(phrase))):

        for i in (tmp_shares):
            if (i['Риск'] >= 31 and
                    i['Риск'] <= 40):
                res_shares.append(i)

    elif ('очень' in set(phrase) and
          ('низкий' in set(phrase) in set(phrase))):
        count = 0
        for i in (tmp_shares):
            if i['Риск'] <= 10:
                res_shares.append(i)


    elif ('не' in set(phrase) and 'очень' in set(phrase) and
          ('высоко' in set(phrase) or 'высокий' in set(phrase))):
        count = 0

        for i in (tmp_shares):
            if (i['Риск'] >= 51 and
                    i['Риск'] <= 60):
                res_shares.append(i)


    elif (len(set(phrase) & {'низко', 'низкий', 'низким'}) != 0):
        count = 0

        for i in (tmp_shares):
            if i['Риск'] <= 30:
                res_shares.append(i)

        if count == 0:
            print('\nТакого не существует...')

    elif (len(set(phrase) & {'средне', 'средний', 'средним'}) != 0):
        count = 0
        num_shares = shares.shape[0]

        for i in (tmp_shares):
            if (i['Риск'] >= 41 and
                    i['Риск'] <= 50):
                res_shares.append(i)


    elif (len(set(phrase) & {'высоко', 'высокий', 'высоким'}) != 0):
        count = 0
        num_shares = shares.shape[0]

        for i in (tmp_shares):
            if (i['Риск'] >= 61):
                res_shares.append(i)

    if len(res_shares) != 0:
        # print("if len(res_shares) != 0:")
        return res_shares, 1
    return res_shares, 0


def get_by_age(phrase, tmp_shares):
    res_shares = []
    selected_attributes = "Средний возраст владельцев"
    for i in (tmp_shares):
        if 'молодой' in set(phrase):
            if i[selected_attributes] < 25:
                res_shares.append(i)
        elif 'взрослый' in set(phrase):
            if i[selected_attributes] >= 25 and i[selected_attributes] < 50:
                res_shares.append(i)
        elif ('пожилой' in set(phrase) or 'старый' in set(phrase)):
            if i[selected_attributes] >= 50:
                res_shares.append(i)
    if len(res_shares) != 0:
        return res_shares, 1
    return tmp_shares, 0

def get_by_pe(phrase, tmp_shares):
    res_shares = []
    selected_attributes = "P/E"
    for i in (tmp_shares):
        if 'низкий' in set(phrase):
            if i[selected_attributes] < 5:
                res_shares.append(i)
        elif 'средний' in set(phrase):
            if i[selected_attributes] >= 5 and i[selected_attributes] < 10:
                res_shares.append(i)
        elif ('высокий' in set(phrase)):
            if i[selected_attributes] >= 10:
                res_shares.append(i)
    if len(res_shares) != 0:
        return res_shares, 1
    return tmp_shares, 0

def get_by_duration(phrase, tmp_shares):
    res_shares = []
    selected_attributes = "Срок"
    for i in (tmp_shares):
        if 'короткий' in set(phrase) or 'маленький' in set(phrase) or 'краткосрок' in set(phrase):
            if i[selected_attributes] <= 3:
                res_shares.append(i)
        elif 'средний' in set(phrase) or 'среднесрок' in set(phrase):
            if i[selected_attributes] > 3  and i[selected_attributes] <= 6:
                res_shares.append(i)
        elif ('долгий' in set(phrase)) or 'долгосрок' in set(phrase) or 'длительный' in set(phrase):
            if i[selected_attributes] > 6:
                res_shares.append(i)
    if len(res_shares) != 0:
        return res_shares, 1
    return tmp_shares, 0

def get_by_earn(phrase, tmp_shares):
    res_shares = []
    selected_attributes = "ROE, %"
    for i in (tmp_shares):
        if 'низкий' in set(phrase) or 'маленький' in set(phrase) or 'никзо' in set(phrase):
            if i[selected_attributes] <= 10:
                res_shares.append(i)
        elif 'средний' in set(phrase) or 'средне' in set(phrase):
            if i[selected_attributes] >= 10  and i[selected_attributes] <= 20:
                res_shares.append(i)
        elif ('высокий' in set(phrase)) or 'высоко' in set(phrase) or 'большой' in set(phrase):
            if i[selected_attributes] >= 20:
                res_shares.append(i)
    if len(res_shares) != 0:
        return res_shares, 1
    return tmp_shares, 0