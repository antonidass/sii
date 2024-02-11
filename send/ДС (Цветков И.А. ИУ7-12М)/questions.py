# Data
NAME = r'(?P<name>(жим штанга|жим гантель|стандартный отжимание|отжимание с колено|отжиманмить ладонь под себя|мах гантель|французский жим штанга|стандартный подтягивание|подтягивание обратный хват|подтягивание на один рука|подтягивание с лестница|медленный отжимание|отжимание на один рука|отжимание от скамья|подъём рука перед себя с гантель|обратный отжимание|планк на локоть|планк на прямой рука|перекрёстный касание плечо в планка|выпрямление рука из планка на локоть|пресснаклон вперд|баланс на один нога|боковой планк|скручивание с колено|медведьквадрат|боковой наклон из плие|скручивание лжа|двусторонний подъм корпус|поворот туловище|одновременный подъм рука и нога|скручивание велосипедист|усложннный боковой планк|косой vобразный скручивание|классический приседание|выпад на место|тяга на 1 нога|приседание с подъм на носка|выпад вперд в стиль становой тяга|мах из собака морда вниз|ягодичный мостик с 1 нога|ягодичный мостик с мах нога|подъм нога лжа на живот|разножка лжа на живот|приседание в стиль сумо|мах нога по диагональ|диагональный выпад на место|мах в сторона с гантель|плие с подъм на носка|сгибание колено лжа|подтягивание колено к грудь|подъм нога в бок|изометрический отведение бедро у стена|отведение нога назад с гантель|раковинамый приседание|отведение нога лёжа на бок|подъм нога лжа на живот|сгибание бедро сидя|выпад на место с гантель|растяжка на один колено|растяжка ягодичный мышца|бабочка|поза мост|поза с колено у грудь|половина поза саранча|поза ребнка|поза кошка|поза посох|наклон вперд стоя|поза воин|наклон в бок|поза на баланс|скручивание спина лжа|поза игольный ушко|бег на место|скакалка|фартлек|интервальный бег|бег с подъём по ступенька|бег на неровный поверхность|забег в гора|техника бег с короткий шаг|функциональный бег с применение препятствие|бег с растяжка|велосипед|подъём сидя|подъём вставать|спринт|интервальный тренировка|приседание в седло|техника катание назад|техника катание на один колесо|кроль|брасс|баттерфляй|плавание на спина|плавание с один рука|плавание с голова вниз|плавание с использование груз на нога|драконий лодка|ускорение|плавание с спортивный инвентарь|плавание под вода|удержание тело в воздух|удержание тело в прогиб|виснуть на согнутый рука с перекладина у подбородок|растяжкакопь стоя|берпеть|мах нога на четвереньки|перекат на прямой нога с пятка на носка))'
CATEGORY_LEVEL1 = r'(?P<category_level1>(силовой|кардио|гибкость))'
CATEGORY_LEVEL2 = r'(?P<category_level2>(с свой вес|отягощать|бег|велосипед|плавание|йог|гимнастика))'
CATEGORY_LEVEL3 = r'(?P<category_level3>(свободный вес|тренажёр|на выносливость|на скорость|спортивный|рекреационный))'
SPORT_DIRECTION = r'(?P<sport_direction>(набор масса|поддерживать форма|поддержать форма|поддержание форма|укреплять мышца|укрепление мышца|укрепить мышца|похудеть|похудение))'
SPORT_LEVEL = r'(?P<sport_level>(низкий уровень|средний уровень|среднее уровень|высокий уровень))'
MUSCLE_GROUP = r'(?P<muscle_group>(нижний|верхний|всё))'
SPORT_EQUIP = r'(?P<sport_equip>(есть спортивный инвентарь|нет спортивный инвентарь))'
SPORT_EQUIP_EXTEND = r'.*{}.*'.format(SPORT_EQUIP)

# Feelings
WANT = r'(планирую|желать|хотеться|хотеть|нужно|нужный|надо|искать|есть|быть|предпочитать|выбирать|выбрать|дать|посмотреть)'
LIKE = r'(нравиться|обожать|любить|фанат|заниматься)'
DISLIKE = r'(не переносить|не нравиться|не подходить|не любить|терпеть не мочь|ненавидеть)'
SIMILAR_TO = r'(похожий|на подобие|аналог|тип)'
NOT_SIMILAR_TO = r'(не похожий|отличный от)'
HAS = r'(иметь|я)'
LIKE_EXTEND = r'({}|{})'.format(LIKE, SIMILAR_TO)
DISLIKE_EXTEND = r'({}|{})'.format(DISLIKE, NOT_SIMILAR_TO)
WANT_EXTEND = r'({}|{}|{})'.format(WANT, LIKE, HAS)
SIMILAR_TO_NAME = r'.*{}.*?{}.*'.format(LIKE_EXTEND, NAME)
NOT_SIMILAR_TO_NAME = r'.*{}.*?{}.*'.format(DISLIKE_EXTEND, NAME)
NO_NEED = r'(не требовать|не нужен)'

VERY = r'(очень|самый|супер|максимальный)'
LOW_HARDNESS = r'(просто сложность|легко сложность|низкий сложность|лёгкий)'
AVERAGE_HARDNESS = r'(нормальный сложность|средний сложность|обычный сложность|несложно)'
HIGH_HARDNESS = r'(сложно сложность|высокий сложность|тяжело сложность|тяжёлый|сложный|трудный)'
LOW_REPEATS = r'(мало подход|немного подход)'
AVERAGE_REPEATS = r'(нормально количество подход|средне количество подход)'
HIGH_REPEATS = r'(много подход)'

# Combine
WANT_CATEGORY_LEVEL1 = r'.*{}.*{}.*'.format(WANT_EXTEND, CATEGORY_LEVEL1)
WANT_CATEGORY_LEVEL2 = r'.*{}.*{}.*'.format(WANT_EXTEND, CATEGORY_LEVEL2)
WANT_CATEGORY_LEVEL3 = r'.*{}.*?{}.*'.format(WANT_EXTEND, CATEGORY_LEVEL3)
WANT_SPORT_DIRECTION = r'.*{}.*{}.*'.format(WANT_EXTEND, SPORT_DIRECTION)
WANT_SPORT_LEVEL = r'.*{}.*{}.*'.format(WANT_EXTEND, SPORT_LEVEL)
WANT_MUSCLE_GROUP = r'.*{}.*{}.*'.format(WANT_EXTEND, MUSCLE_GROUP)
WANT_SPORT_EQUIP = r'.*{}.*{}.*'.format(WANT_EXTEND, SPORT_EQUIP)
WANT_VERY_LOW_HARDNESS = r'.*{}.*{}.*{}.*'.format(WANT_EXTEND, VERY, LOW_HARDNESS)
WANT_LOW_HARDNESS = r'.*{}.*{}.*'.format(WANT_EXTEND, LOW_HARDNESS)
WANT_AVERAGE_HARDNESS = r'.*{}.*{}.*'.format(WANT_EXTEND, AVERAGE_HARDNESS)
WANT_HIGH_HARDNESS = r'.*{}.*{}.*'.format(WANT_EXTEND, HIGH_HARDNESS)
WANT_VERY_HIGH_HARDNESS = r'.*{}.*{}.*{}.*'.format(WANT_EXTEND, VERY, HIGH_HARDNESS)
WANT_VERY_LOW_REPEATS = r'.*{}.*{}.*{}.*'.format(WANT_EXTEND, VERY, LOW_REPEATS)
WANT_LOW_REPEATS = r'.*{}.*{}.*'.format(WANT_EXTEND, LOW_REPEATS)
WANT_AVERAGE_REPEATS = r'.*{}.*{}.*'.format(WANT_EXTEND, AVERAGE_REPEATS)
WANT_HIGH_REPEATS = r'.*{}.*{}.*'.format(WANT_EXTEND, HIGH_REPEATS)
WANT_VERY_HIGH_REPEATS = r'.*{}.*{}.*{}.*'.format(WANT_EXTEND, VERY, HIGH_REPEATS)

NO_NEED_SPORT_LEVEL = r'.*{}.*{}.*'.format(NO_NEED, SPORT_LEVEL)

# ANY
HELP = r'(посоветовать|помочь|предложить|подсказать|показать|порекомендовать|посмотреть|ознакомиться)'
NOT_KNOW_GENERAL = r'((не.*знать).*(хотеть|надо))'

GENERAL_QUESTION = r'что|какой'

SHOW_ANY = r'.*({}|{}).*'.format(HELP, NOT_KNOW_GENERAL)
WHAT_ANY = r'.*{}.*{}.*'.format(GENERAL_QUESTION, HELP)

# RESULT
RULE_ARR = [
    NOT_SIMILAR_TO_NAME,
    SIMILAR_TO_NAME,
    NO_NEED_SPORT_LEVEL,
    SPORT_EQUIP_EXTEND,
    WANT_SPORT_DIRECTION,
    WANT_SPORT_LEVEL,
    WANT_MUSCLE_GROUP,
    WANT_CATEGORY_LEVEL3,
    WANT_CATEGORY_LEVEL2,
    WANT_CATEGORY_LEVEL1,
    WANT_VERY_LOW_HARDNESS,
    WANT_LOW_HARDNESS,
    WANT_AVERAGE_HARDNESS,
    WANT_VERY_HIGH_HARDNESS,
    WANT_HIGH_HARDNESS,
    WANT_VERY_LOW_REPEATS,
    WANT_LOW_REPEATS,
    WANT_AVERAGE_REPEATS,
    WANT_VERY_HIGH_REPEATS,
    WANT_HIGH_REPEATS,
    SHOW_ANY,
    WHAT_ANY,
]
