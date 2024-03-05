import pymorphy3
import re

from answer import *
from shares import *

morph = pymorphy3.MorphAnalyzer()

attributes = [["Бумага", "Бумага", "\nНапиши название."],
              ["Тип", "Тип", "\nУкажи тип."],
              ["Страна", "Страна", "\nУкажи страну."],
              ["Сектор", "Сектор", "\nУкажи сектор."],
              ["Срок", "Срок", "\nУкажи срок на который хотите приобрести бумагу (краткосрок, среднесрок, долгосрок)."],
              ["Риск", "Риск", "\nУкажи желаемый риск (очень низкий, низкий, не очень низкий, средний, не очень высокий, высокий)."]]

selected_attributes = ''

step = 0
scenarios = -1


def get_text_values():
    res_shares = shares.iloc

    text_values = ""

    for i in res_shares:
        text_values += i["Тип"] + " "
        if i["Страна"] is not None:
            text_values += i["Страна"] + " "
        if i["Сектор"] is not None:
            text_values += i["Сектор"] + " "
        if i["Тип облигации"] is not None:
            text_values += i["Тип облигации"] + " "
        if i["Тип опциона"] is not None:
            text_values += i["Тип опциона"] + " "

    return set(parser(text_values[:-1]))


def handle(phrase):
    global step, scenarios, attributes, selected_attributes

    if len(set(phrase) & {'давать', 'привет', 'добрый', 'здравствуй', 'здравствуйте'}) != 0:
        welcome()
        return

    if len(set(phrase) & {'пока', 'нет'}) != 0:
        bye()
        exit(0)

    if (len(set(phrase) & {'какой', 'вывести', 'показать', 'написать', 'перечислить', 'список', 'подсказать'}) != 0
            and len(set(phrase) & {'всё', 'все', 'перечень', 'каталог', 'список'}) != 0
            and len(set(phrase) & {'бумага'}) != 0):
        full_list()
        return
    
    if (len(set(phrase) & {'случайный', 'любой', 'какойнибудь', 'рандомный', 'какиенибудь'}) != 0):
        random_share()
        return
    

    count_terms_worked = 0
    res_shares = shares.iloc

    res_status = 1

    if (len(set(phrase) & {'молодой', 'старый', 'пожилой', 'взрослый'}) != 0):
        res_shares, status = get_by_age(phrase, res_shares)
        res_status *= status
        count_terms_worked += 1

    if len((set(phrase) & {'низко', 'низкий', 'средне', 'средний', 'высоко', 'высокий', 'очень', 'не'}) and (set(phrase) & {'риск'})) != 0:
        res_shares, status = distance_share(phrase, res_shares)
        res_status *= status
        count_terms_worked += 1

    if len((set(phrase) & {'низко', 'низкий', 'средне', 'средний', 'высоко', 'высокий'}) and (set(phrase) & {'P/E', 'pe', 'пинаи'})) != 0:
        res_shares, status = get_by_pe(phrase, res_shares)
        res_status *= status
        count_terms_worked += 1
    
    if len((set(phrase) & {'короткий', 'средний', 'долгий', 'длительный'}) and (set(phrase) & {'срок'})) != 0 or \
        len((set(phrase) & {'краткосрок', 'долгосрок', 'среднесрок'})) != 0:
        res_shares, status = get_by_duration(phrase, res_shares)
        res_status *= status
        count_terms_worked += 1

    if len((set(phrase) & {'низко', 'низкий', 'маленький', 'средне', 'средний', 'высоко', 'большой', 'высокий'}) and (set(phrase) & {'доходность'})) != 0:
        res_shares, status = get_by_earn(phrase, res_shares)
        res_status *= status
        count_terms_worked += 1

    if len(set(phrase) & get_text_values()) != 0:
        res_shares, status = text_values_share(phrase, res_shares, get_text_values())
        res_status *= status
        count_terms_worked += 1

    if count_terms_worked > 0:
        if res_status == 1:
            output_all_shares(res_shares)
        else:
            print("ТАКИХ НЕ НАЙДЕНО!!!!!")
        more()
        return

    if len(set(phrase) & {'какой', 'вывести', 'показать', 'найти', 'подсказать'}) != 0 or (
            len(set(phrase) & {'какой', 'вывести', 'показать', 'найти', 'подсказать'}) != 0
            and len(set(phrase) & {'бумага'}) != 0) or scenarios >= 3:
        if scenarios == -1:
            scenarios = 3

        if step == 0:
            print('\nПоказать бумагу по названию?')
            string = input()
            string_parser = parser(string)

            if ('да') in string_parser:
                step = 2
                scenarios = 4

                print('\nЧто за бумага?')
                share_title = input()
                print("share title = ", share_title)

                step = 0
                scenarios = -1

                share = find_share(share_title)
                if share == -1:
                    not_found()
                else:
                    more()

            elif 'нет' in string_parser:
                step = 2
                scenarios = 5

                print('\nПо какому критерию будем искать?')
            else:
                step = 0
                scenarios = -1

                print(string)
                share = find_share(share_title)
                if share == -1:
                    not_found()
                else:
                    more()
            return

        elif step == 2:
            if scenarios == 5:
                attr = ''
                for i in range(len(attributes)):

                    if attributes[i][1].lower() in set(phrase):
                        attr = attributes[i][0]
                        selected_attributes = attributes[i][0]
                        print(attributes[i][2])
                        step = 3
                        scenarios = 5

                if attr == '':
                    print('\nУверен, что не опечатался?')

        elif step == 3:
            step = 0
            scenarios = -1
            if len((set(phrase) & {'подсказать', 'бумага'})) != 0:
                print("Что посоветовать?")
            else:
                output_shares(phrase, selected_attributes)
                more() 

    else:
        not_found()
        more()

    return


def parser(s):
    phrase = re.sub(r'[^\w\s]', '', s.lower()).split()
    norm_phrase = list()
    for word in phrase:
        norm_phrase.append(morph.parse(word)[0].normal_form)
    return norm_phrase


def main():
    welcome()

    while True:
        phrase = input()
        norm_phrase = parser(phrase)
        # print(norm_phrase)
        handle(norm_phrase)


if __name__ == "__main__":
    main()
