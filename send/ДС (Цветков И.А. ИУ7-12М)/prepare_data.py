from dialog import namesUI, giveRecommendationFull, df
from process import getNormalFormPhrase


def initPrefer():
  return {
    "likes": [], 
    "dislikes": [],
    "categories": [],
    "sport_directions": [], 
    "sport_levels": [],
    "muscle_groups": [],
    "need_sport_equipment": [],
    "hardness": [],
    "repeats": [],
  }


def initFilter():
  return {
    "no_sport_level": [],
  }


def _replaceNames(inputArr):
  namesArr = []
  namesDict = {}
  for i in range(len(namesUI)):
    namesDict[getNormalFormPhrase(namesUI[i].lower().replace('-', ''))] = i

  for name in inputArr:
    if name in namesDict.keys():
      if namesUI[namesDict[name]] not in namesArr:
        namesArr.append(namesUI[namesDict[name]])
    else:
      namesArr.append(name)

  return namesArr


def _replaceCategories(inputArr):
  categoriesArr = []
  categoriesDict = {
    "силовой": "Силовая",
    "кардио": "Кардио",
    "гибкость": "Гибкость",
    "с свой вес": "Со своим весом",
    "отягощать": "Отягощающие",
    "бег": "Бег",
    "велосипед": "Велосипед",
    "плавание": "Плавание",
    "йог": "Йога",
    "гимнастика": "Гимнастика",
    "свободный вес": "Сводобные веса",
    "тренажёр": "Тренажеры",
    "на выносливость": "На выносливость",
    "на скорость": "На скорость",
    "спортивный": "Спортивная",
    "рекреационный": "Рекреационная",
  }
  
  for category in inputArr:
    if category not in categoriesDict.values() and \
      category in categoriesDict.keys():
      if categoriesDict[category] not in categoriesArr:
        categoriesArr.append(categoriesDict[category])
    else:
      categoriesArr.append(category)

  return categoriesArr


def _replaceSportDirections(inputArr):
  sportDirectionsArr = []
  sportDirectionsDict = {
    "набор масса": "Набор массы",
    "поддерживать форма": "Поддержание формы",
    "поддержать форма": "Поддержание формы",
    "поддержание форма": "Поддержание формы",
    "укреплять мышца": "Укрепление мышц",
    "укрепление мышца": "Укрепление мышц",
    "укрепить мышца": "Укрепление мышц",
    "похудеть": "Похудение",
    "похудение": "Похудение",
  }

  for sportDirection in inputArr:
    if sportDirection not in sportDirectionsDict.values() and \
      sportDirection in sportDirectionsDict.keys():
      if sportDirectionsDict[sportDirection] not in sportDirectionsArr:
        sportDirectionsArr.append(sportDirectionsDict[sportDirection])
    else:
      sportDirectionsArr.append(sportDirection)

  return sportDirectionsArr


def _replaceSportLevels(inputArr):
  sportLevelsArr = []
  sportLevelsDict = {
    "низкий уровень": "Низкий",
    "средний уровень": "Средний",
    "среднее уровень": "Средний",
    "высокий уровень": "Высокий",
  }
  
  for sportLevel in inputArr:
    if sportLevel not in sportLevelsDict.values() and \
      sportLevel in sportLevelsDict.keys():
      if sportLevelsDict[sportLevel] not in sportLevelsArr:
        sportLevelsArr.append(sportLevelsDict[sportLevel])
    else:
      sportLevelsArr.append(sportLevel)

  return sportLevelsArr


def _replaceMuscleGroups(inputArr):
  muscleGroupsArr = []
  muscleGroupsDict = {
    "верхний": "Верхняя",
    "нижний": "Нижняя",
    "всё": "Все",
  }
  
  for muscleGroup in inputArr:
    if muscleGroup not in muscleGroupsDict.values() and \
      muscleGroup in muscleGroupsDict.keys():
      if muscleGroupsDict[muscleGroup] not in muscleGroupsArr:
        muscleGroupsArr.append(muscleGroupsDict[muscleGroup])
    else:
      muscleGroupsArr.append(muscleGroup)

  return muscleGroupsArr


def _replaceSportEquips(inputArr):
  sportEquipsArr = []
  sportEquipsDict = {
    "есть спортивный инвентарь": "Да",
    "нет спортивный инвентарь": "Нет",
  }
  
  for sportEquip in inputArr:
    if sportEquip not in sportEquipsDict.values() and \
      sportEquip in sportEquipsDict.keys():
      if sportEquipsDict[sportEquip] not in sportEquipsArr:
        sportEquipsArr.append(sportEquipsDict[sportEquip])
    else:
      sportEquipsArr.append(sportEquip)

  return sportEquipsArr


def transformParamDict(paramDict):
  paramDict["likes"] = _replaceNames(paramDict["likes"])
  paramDict["dislikes"] = _replaceNames(paramDict["dislikes"])
  paramDict["categories"] = _replaceCategories(paramDict["categories"])
  paramDict["sport_directions"] = _replaceSportDirections(paramDict["sport_directions"])
  paramDict["sport_levels"] = _replaceSportLevels(paramDict["sport_levels"])
  paramDict["muscle_groups"] = _replaceMuscleGroups(paramDict["muscle_groups"])
  paramDict["need_sport_equipment"] = _replaceSportEquips(paramDict["need_sport_equipment"])

  # print(f'\nОбновлено\n{paramDict}\n')
  return paramDict


def transformFilterDict(filterDict):
  filterDict["no_sport_level"] = _replaceSportLevels(filterDict["no_sport_level"])

  # print(f'\nОбновлено (фильтр)\n{filterDict}\n')
  return filterDict


def find(paramDict):
  paramDict = transformParamDict(paramDict)
             
  return giveRecommendationFull(
    likesSelected=paramDict["likes"],
    dislikesSelected=paramDict["dislikes"],
    categoriesSelected=paramDict["categories"],
    sportDirectionsSelected=paramDict["sport_directions"],
    sportLevelsSelected=paramDict["sport_levels"],
    muscleGroupsSelected=paramDict["muscle_groups"],
    needSportEquipSelected=paramDict["need_sport_equipment"],
    hardnessSelected=paramDict["hardness"],
    repeatsSelected=paramDict["repeats"],
    df=df,
  )
