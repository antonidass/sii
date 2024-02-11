# 0. Импорты
import itertools
import pandas as pd
import numpy as np
from IPython.display import display
from cmath import isnan
from numpy import dot
from numpy.linalg import norm
from collections import defaultdict
import plotly.express as px


# 1. Исходные данные
pd.set_option('display.max_columns', None)
df0 = pd.read_csv('data.csv', delimiter=';', encoding="utf8")
df = df0.copy(deep=True)


# 1.1. Дополнительные колонки для диалоговой системы
hierarchyList = []
[hierarchyList.extend(value.split(',')) for value in df["Иерархия"].values]
hierarchyList = list(set(hierarchyList))
for item in hierarchyList:
    df[item] = df["Иерархия"].map(lambda elem: 1 if item in elem else 0)

df["Очень легко"] = df["Время тренировки"].map(lambda elem: 1 if 1 <= elem <= 4 else 0)
df["Легко"] = df["Время тренировки"].map(lambda elem: 1 if 4 < elem <= 8 else 0)
df["Нормально"] = df["Время тренировки"].map(lambda elem: 1 if 8 < elem <= 34 else 0)
df["Сложно"] = df["Время тренировки"].map(lambda elem: 1 if 34 < elem <= 46 else 0)
df["Очень сложно"] = df["Время тренировки"].map(lambda elem: 1 if 46 < elem else 0)

df["Очень мало подходов"] = df["Количество подходов"].map(lambda elem: 1 if 1 <= elem <= 2 else 0)
df["Легко мало подходов"] = df["Количество подходов"].map(lambda elem: 1 if 2 < elem <= 4 else 0)
df["Средне подходов"] = df["Количество подходов"].map(lambda elem: 1 if 4 < elem <= 14 else 0)
df["Много подходов"] = df["Количество подходов"].map(lambda elem: 1 if 14 < elem <= 23 else 0)
df["Очень много подходов"] = df["Количество подходов"].map(lambda elem: 1 if 23 < elem else 0)



# 2. Преообразовать данные к числам - требование спортивного инвентаря
sportEquipDict = { "Нет": 0, "Да": 1 }
df["Требуется спортивный инвентарь"] = \
  df["Требуется спортивный инвентарь"].map(lambda elem: sportEquipDict[elem])

df["Иерархия"] = df["Иерархия"].map(lambda elem: elem.split(","))


# 3. Матрицы смежности 
# 3.1. Для требуемого уровня подготовки
sportLevel = {
  "Низкий": 0,
  "Средний": 1,
  "Высокий": 2,
}

sportLevelMatrix = np.zeros((len(sportLevel), len(sportLevel)))

sportLevelMatrix[sportLevel["Низкий"], sportLevel["Высокий"]] = \
  sportLevelMatrix[sportLevel["Высокий"], sportLevel["Низкий"]] = 1
sportLevelMatrix[sportLevel["Низкий"], sportLevel["Средний"]] = \
  sportLevelMatrix[sportLevel["Средний"], sportLevel["Низкий"]] = 0.5
sportLevelMatrix[sportLevel["Средний"], sportLevel["Высокий"]] = \
  sportLevelMatrix[sportLevel["Высокий"], sportLevel["Средний"]] = 0.5


# 3.2. Для направленности
sportDirection = {
  "Похудение": 0,
  "Поддержание формы": 1,
  "Укрепление мышц": 2,
  "Набор массы": 3,
}

sportDirectionMatrix = np.zeros((len(sportDirection), len(sportDirection)))

sportDirectionMatrix[sportDirection["Похудение"], sportDirection["Поддержание формы"]] = \
  sportDirectionMatrix[sportDirection["Поддержание формы"], sportDirection["Похудение"]] = 0.3
sportDirectionMatrix[sportDirection["Похудение"], sportDirection["Укрепление мышц"]] = \
  sportDirectionMatrix[sportDirection["Укрепление мышц"], sportDirection["Похудение"]] = 0.7
sportDirectionMatrix[sportDirection["Похудение"], sportDirection["Набор массы"]] = \
  sportDirectionMatrix[sportDirection["Набор массы"], sportDirection["Похудение"]] = 1

sportDirectionMatrix[sportDirection["Поддержание формы"], sportDirection["Укрепление мышц"]] = \
  sportDirectionMatrix[sportDirection["Укрепление мышц"], sportDirection["Поддержание формы"]] = 0.4
sportDirectionMatrix[sportDirection["Поддержание формы"], sportDirection["Набор массы"]] = \
  sportDirectionMatrix[sportDirection["Набор массы"], sportDirection["Поддержание формы"]] = 0.7

sportDirectionMatrix[sportDirection["Укрепление мышц"], sportDirection["Набор массы"]] = \
  sportDirectionMatrix[sportDirection["Набор массы"], sportDirection["Укрепление мышц"]] = 0.3


# 3.3. Для группы мышц
muscleGroup = {
  "Верхняя": 0,
  "Нижняя": 1,
  "Все": 2,
}

muscleGroupMatrix = np.zeros((len(muscleGroup), len(muscleGroup)))

muscleGroupMatrix[muscleGroup["Верхняя"], muscleGroup["Нижняя"]] = \
  muscleGroupMatrix[muscleGroup["Нижняя"], muscleGroup["Верхняя"]] = 1
muscleGroupMatrix[muscleGroup["Верхняя"], muscleGroup["Все"]] = \
  muscleGroupMatrix[muscleGroup["Все"], muscleGroup["Верхняя"]] = 0.5
muscleGroupMatrix[muscleGroup["Нижняя"], muscleGroup["Все"]] = \
  muscleGroupMatrix[muscleGroup["Все"], muscleGroup["Нижняя"]] = 0.5



# 4. Фрейм для категорий
nameArr = df["Название"]

dfTree = pd.DataFrame(
    columns=["Название", "Иерархия"], 
    data=df[["Название", "Иерархия"]].values
)

del df["Название"]
del df["Иерархия"]


# 5. Матрица смежности для категорий
# 5.1. Уровень 1
layer1 = {
  "Силовая": 0,
  "Кардио": 1,
  "Гибкость": 2,
}

treeLayer1 = np.zeros((len(layer1), len(layer1)))

treeLayer1[layer1["Силовая"], layer1["Кардио"]] = \
  treeLayer1[layer1["Кардио"], layer1["Силовая"]] = 0.6
treeLayer1[layer1["Силовая"], layer1["Гибкость"]] = \
  treeLayer1[layer1["Гибкость"], layer1["Силовая"]] = 1

treeLayer1[layer1["Кардио"], layer1["Гибкость"]] = \
  treeLayer1[layer1["Гибкость"], layer1["Кардио"]] = 0.4


# 5.2. Уровень 2
layer2 = {
  "Со своим весом": 0,
  "Отягощающие": 1,
  "Бег": 2,
  "Велосипед": 3,
  "Плавание": 4,
  "Йога": 5,
  "Гимнастика": 6,
}

treeLayer2 = np.zeros((len(layer2), len(layer2)))


treeLayer2[layer2["Со своим весом"], layer2["Отягощающие"]] = \
  treeLayer2[layer2["Отягощающие"], layer2["Со своим весом"]] = 0.2
treeLayer2[layer2["Со своим весом"], layer2["Бег"]] = \
  treeLayer2[layer2["Бег"], layer2["Со своим весом"]] = 0.5
treeLayer2[layer2["Со своим весом"], layer2["Велосипед"]] = \
  treeLayer2[layer2["Велосипед"], layer2["Со своим весом"]] = 0.6
treeLayer2[layer2["Со своим весом"], layer2["Плавание"]] = \
  treeLayer2[layer2["Плавание"], layer2["Со своим весом"]] = 0.7
treeLayer2[layer2["Со своим весом"], layer2["Йога"]] = \
  treeLayer2[layer2["Йога"], layer2["Со своим весом"]] = 1
treeLayer2[layer2["Со своим весом"], layer2["Гимнастика"]] = \
  treeLayer2[layer2["Гимнастика"], layer2["Со своим весом"]] = 0.9

treeLayer2[layer2["Отягощающие"], layer2["Бег"]] = \
  treeLayer2[layer2["Бег"], layer2["Отягощающие"]] = 0.6
treeLayer2[layer2["Отягощающие"], layer2["Велосипед"]] = \
  treeLayer2[layer2["Велосипед"], layer2["Отягощающие"]] = 0.7
treeLayer2[layer2["Отягощающие"], layer2["Плавание"]] = \
  treeLayer2[layer2["Плавание"], layer2["Отягощающие"]] = 0.8
treeLayer2[layer2["Отягощающие"], layer2["Йога"]] = \
  treeLayer2[layer2["Йога"], layer2["Отягощающие"]] = 0.9
treeLayer2[layer2["Отягощающие"], layer2["Гимнастика"]] = \
  treeLayer2[layer2["Гимнастика"], layer2["Отягощающие"]] = 1

treeLayer2[layer2["Бег"], layer2["Велосипед"]] = \
  treeLayer2[layer2["Велосипед"], layer2["Бег"]] = 0.1
treeLayer2[layer2["Бег"], layer2["Плавание"]] = \
  treeLayer2[layer2["Плавание"], layer2["Бег"]] = 0.2
treeLayer2[layer2["Бег"], layer2["Йога"]] = \
  treeLayer2[layer2["Йога"], layer2["Бег"]] = 0.7
treeLayer2[layer2["Бег"], layer2["Гимнастика"]] = \
  treeLayer2[layer2["Гимнастика"], layer2["Бег"]] = 0.8

treeLayer2[layer2["Велосипед"], layer2["Плавание"]] = \
  treeLayer2[layer2["Плавание"], layer2["Велосипед"]] = 0.2
treeLayer2[layer2["Велосипед"], layer2["Йога"]] = \
  treeLayer2[layer2["Йога"], layer2["Велосипед"]] = 0.6
treeLayer2[layer2["Велосипед"], layer2["Гимнастика"]] = \
  treeLayer2[layer2["Гимнастика"], layer2["Велосипед"]] = 0.7

treeLayer2[layer2["Плавание"], layer2["Йога"]] = \
  treeLayer2[layer2["Йога"], layer2["Плавание"]] = 0.6
treeLayer2[layer2["Плавание"], layer2["Гимнастика"]] = \
  treeLayer2[layer2["Гимнастика"], layer2["Плавание"]] = 0.7

treeLayer2[layer2["Йога"], layer2["Гимнастика"]] = \
  treeLayer2[layer2["Гимнастика"], layer2["Йога"]] = 0.3



# 5.3. Уровень 3
layer3 = {
    "Сводобные веса": 0,
    "Тренажеры": 1,
    "На скорость": 2,
    "На выносливость": 3,
    "Рекреационная": 4,
    "Спортивная": 5,
}

treeLayer3 = np.zeros((len(layer3), len(layer3)))

treeLayer3[layer3["Сводобные веса"], layer3["Тренажеры"]] = \
  treeLayer3[layer3["Тренажеры"], layer3["Сводобные веса"]] = 0.3
treeLayer3[layer3["Сводобные веса"], layer3["На скорость"]] = \
  treeLayer3[layer3["На скорость"], layer3["Сводобные веса"]] = 0.6
treeLayer3[layer3["Сводобные веса"], layer3["На выносливость"]] = \
  treeLayer3[layer3["На выносливость"], layer3["Сводобные веса"]] = 0.7
treeLayer3[layer3["Сводобные веса"], layer3["Рекреационная"]] = \
  treeLayer3[layer3["Рекреационная"], layer3["Сводобные веса"]] = 1
treeLayer3[layer3["Сводобные веса"], layer3["Спортивная"]] = \
  treeLayer3[layer3["Спортивная"], layer3["Сводобные веса"]] = 1

treeLayer3[layer3["Тренажеры"], layer3["На скорость"]] = \
  treeLayer3[layer3["На скорость"], layer3["Тренажеры"]] = 0.6
treeLayer3[layer3["Тренажеры"], layer3["На выносливость"]] = \
  treeLayer3[layer3["На выносливость"], layer3["Тренажеры"]] = 0.7
treeLayer3[layer3["Тренажеры"], layer3["Рекреационная"]] = \
  treeLayer3[layer3["Рекреационная"], layer3["Тренажеры"]] = 1
treeLayer3[layer3["Тренажеры"], layer3["Спортивная"]] = \
  treeLayer3[layer3["Спортивная"], layer3["Тренажеры"]] = 1

treeLayer3[layer3["На скорость"], layer3["На выносливость"]] = \
  treeLayer3[layer3["На выносливость"], layer3["На скорость"]] = 0.2
treeLayer3[layer3["На скорость"], layer3["Рекреационная"]] = \
  treeLayer3[layer3["Рекреационная"], layer3["На скорость"]] = 0.7
treeLayer3[layer3["На скорость"], layer3["Спортивная"]] = \
  treeLayer3[layer3["Спортивная"], layer3["На скорость"]] = 0.8

treeLayer3[layer3["На выносливость"], layer3["Рекреационная"]] = \
  treeLayer3[layer3["Рекреационная"], layer3["На выносливость"]] = 0.8
treeLayer3[layer3["На выносливость"], layer3["Спортивная"]] = \
  treeLayer3[layer3["Спортивная"], layer3["На выносливость"]] = 0.9

treeLayer3[layer3["Рекреационная"], layer3["Спортивная"]] = \
  treeLayer3[layer3["Спортивная"], layer3["Рекреационная"]] = 0.4


# 5.4. Объединение
layer = [layer1, layer2, layer3]
tree = [treeLayer1, treeLayer2, treeLayer3]



# 6. Функции вычисления расстояний
excludeFields = ["Требуемый уровень подготовки", "Направленность", "Группа мышц"]


def getDataFrameStat(df):
    dfStat = df.copy()
    for elem in excludeFields:
        del dfStat[elem]
    
    return dfStat


def _getDistance(v1, v2, nPow):
  res = 0
  for i in range(len(v1)):
    if isnan(v1[i]) or isnan(v2[i]):
      continue
    res += pow(abs(v1[i] - v2[i]), nPow)
      
  return pow(res, 1 / nPow)


# Манхэттенское расстояние
def getManhattanDistance(v1, v2):
  return _getDistance(v1, v2, 1)


# Евклидово расстояние
def getEuclideanDistance(v1, v2):
  return _getDistance(v1, v2, 2)


# Косинусное 
def getCos(v1, v2):
  v1T, v2T = v1.copy(), v2.copy()
  indArr = [i for i, (elem1, elem2) in enumerate(zip(v1T, v2T)) if isnan(elem1) or isnan(elem2)]
  v1T[:] = [elem for i, elem in enumerate(v1T) if i not in indArr]
  v2T[:] = [elem for i, elem in enumerate(v2T) if i not in indArr]

  return 1 - dot(v1T, v2T) / (norm(v1T) * norm(v2T))


# Расстояние по дереву
def getTreeDistance(v1, v2):
  res = 0
  size = max(len(v1), len(v2))

  for i in range(size):
    try:
      res += tree[i][layer[i][v1[i]]][layer[i][v2[i]]]
    except:
      res += 0.5
  
  return res / size


# Найти все похожие
def getSimilarity(id, matr, nameArr):
  data = matr[id]
  res = pd.DataFrame(
      zip(data, nameArr), 
      index=np.arange(len(matr)), 
      columns=["Расстояние", "Название"]
  )
  return res.sort_values("Расстояние")


# Сравнение уровня подготовки
def getSportLevelDistance(v1, v2):
  return sportLevelMatrix[sportLevel[v1], sportLevel[v2]]


# Сравнение направленности
def getSportDirectionDistance(v1, v2):
  return sportDirectionMatrix[sportDirection[v1], sportDirection[v2]]


# Сравнение групп мышц
def getMsucleDistance(v1, v2):
  return muscleGroupMatrix[muscleGroup[v1], muscleGroup[v2]]


def calcDistance(f, df):
  matrData = df.values.tolist()
  n = len(matrData)
  matrRes = np.zeros((n, n))
  for i in range(n):
    for j in range(i, n):
      matrRes[i][j] = matrRes[j][i] = f(matrData[i], matrData[j])
            
  return matrRes / matrRes.max()


def calcDistanceCombined(df, dfTree):
  dfTree = dfTree["Иерархия"]
  dfStatParams = getDataFrameStat(df)
  
  matrTree = calcDistance(getTreeDistance, dfTree)
  matrEucl = calcDistance(getEuclideanDistance, dfStatParams)
  matrSportLevel = calcDistance(getSportLevelDistance, df["Требуемый уровень подготовки"])
  matrSportDirection = calcDistance(getSportDirectionDistance, df["Направленность"])
  matrMuscle = calcDistance(getMsucleDistance, df["Группа мышц"])

  xTree = matrTree.max()
  xStat = matrEucl.max()
  xSportLevel = matrSportLevel.max()
  xSportDirection = matrSportDirection.max()
  xMuscle = matrMuscle.max()


  kTree, kStat, kSportLevel, kSportDirection, kMuscle = 2, 4, 1, 2, 2

  return (kTree * matrTree + kStat * matrEucl + kSportLevel * matrSportLevel + kSportDirection * matrSportDirection + kMuscle * matrMuscle) / \
    (kTree * xTree + kStat * xStat + kSportLevel * xSportLevel + kSportDirection * xSportDirection + kMuscle * xMuscle)


# 7. Функция отображения
def draw(matrRes, nameArr, title, color='Inferno'):
  fig = px.imshow(matrRes, x=nameArr, y=nameArr, color_continuous_scale=color, title=title)
  fig.update_layout(width=1000, height=1200)
  fig.update_traces(text=nameArr)
  fig.update_xaxes(side="top")
  fig.show()


# 8. Отображение расстояний
def drawManhatten():
  matrRes = calcDistance(getManhattanDistance, getDataFrameStat(df))
  draw(matrRes, nameArr, "Манхэттенское расстояние")


def drawEuclid():
  matrRes = calcDistance(getEuclideanDistance, getDataFrameStat(df))
  draw(matrRes, nameArr, "Евклидово расстояние")


def drawCos():
  matrRes = calcDistance(getCos, getDataFrameStat(df))
  draw(matrRes, nameArr, "Косинусная мера близости")


def drawSportLevel():
  matrRes = calcDistance(getSportLevelDistance, df["Требуемый уровень подготовки"])
  draw(matrRes, nameArr, "Расстояние по уровню подготовки")


def drawSportDirection():
  matrRes = calcDistance(getSportDirectionDistance, df["Направленность"])
  draw(matrRes, nameArr, "Расстояние по направленности")


def drawMuscle():
  matrRes = calcDistance(getMsucleDistance, df["Группа мышц"])
  draw(matrRes, nameArr, "Расстояние по группе мышц")


def drawTree():
  matrRes = calcDistance(getTreeDistance, dfTree["Иерархия"])
  draw(matrRes, nameArr, "Расстояние по дереву")


def drawCombine():
  draw(calcDistanceCombined(df, dfTree), nameArr, "Комбинированная мера")


# 9. Функции для подбора по лайкам/дизлайкам
matrSimilarity = calcDistanceCombined(df, dfTree)

# 9.1. Задача 1
F_NAME = "Название"
F_DIST = "Расстояние"
            
def _findSimilar(name):
  ind = df0[F_NAME].tolist().index(name)
  listSimilarity = getSimilarity(ind, matrSimilarity, nameArr)
  return listSimilarity


def findSimilar(name):
  listSimilarity = _findSimilar(name)
  return listSimilarity[listSimilarity[F_NAME] != name]


def _findSimilarMany(nameArr):
  recList = []
  for name in nameArr:
    rec = _findSimilar(name)
    recList.append(rec.loc[rec[F_NAME].isin(nameArr) == False])

  dfRes = defaultdict(lambda: 1e2)
  for rec in recList:
    for _, row in rec.iterrows():
      curName = row[F_NAME]
      curDist = row[F_DIST]
      dfRes[curName] = min(dfRes[curName], curDist)

  return dfRes


def findSimilarMany(nameArr):
  resDict = _findSimilarMany(nameArr)
  return sorted(
    [{key: elem} for key, elem in resDict.items()], 
    key=lambda elem: list(elem.values())[0]
  )


def delOpposite(dict, nameArr):
  for name in nameArr:
    if name in dict.keys():
      del dict[name]
  
  return dict


def findByReaction(likesArr=[], dislikesArr=[]):
  likesRec = delOpposite(_findSimilarMany(likesArr), dislikesArr)
  dislikesRec = delOpposite(_findSimilarMany(dislikesArr), likesArr)

  dictRes = {}
  if len(likesArr) == 0:
    for key, elem in dislikesRec.items():
      dictRes[key] = 1 - elem
    return sorted(
      [{key: elem} for key, elem in dictRes.items()], 
      key=lambda elem: list(elem.values())[0]
    )

  for key in likesRec.keys():
    if likesRec[key] <= dislikesRec[key]:
      dictRes[key] = likesRec[key]

  return sorted(
    [{key: elem} for key, elem in dictRes.items()], 
    key=lambda elem: list(elem.values())[0]
  )


# 10. Функции диалоговой системы
def sortDict(resDict):
  sorted_tuples = sorted(resDict.items(), key=lambda item: item[1], reverse=False)
  sorted_dict = {k: v for k, v in sorted_tuples}

  return sorted_dict


def getArrFromSeries(data):
  arr = []
  for elem in data:
    arr.append(elem)

  return arr

namesUI = getArrFromSeries(nameArr)


def _fromArrDictToDict(arrDict):
  resDict = {}
  for elem in arrDict:
    resDict.update(elem)

  return resDict


def _compareLikesParams(likesDict, paramsDict):
  resDict = {}
  for key, value in likesDict.items():
    if key in paramsDict.keys():
      resDict[key] = value * paramsDict[key]
      del paramsDict[key]
    else:
      resDict[key] = value

  for key, value in paramsDict.items():
    resDict[key] = value

  return resDict


def _getDefaultResultParams(nameArr):
  resDict = {}
  for name in nameArr:
    resDict[name] = 0

  return resDict


def _getRecommendationParams(
  categoriesSelected,
  sportDirectionsSelected,
  sportLevelsSelected,
  muscleGroupsSelected,
  needSportEquipSelected,
  hardnessSelected,
  repeatsSelected,
  df
):
  dfColumnsArr = df.columns.values.tolist()
  indexDict = {}
  indexDict[dfColumnsArr.index('Направленность')] = sportDirectionsSelected
  indexDict[dfColumnsArr.index('Требуемый уровень подготовки')] = sportLevelsSelected
  indexDict[dfColumnsArr.index('Группа мышц')] = muscleGroupsSelected
  indexDict[dfColumnsArr.index('Требуется спортивный инвентарь')] = needSportEquipSelected

  for category in categoriesSelected:
    indexDict[dfColumnsArr.index(category)] = [1]

  for hardness in hardnessSelected:
    indexDict[dfColumnsArr.index(hardness)] = [1]

  for repeat in repeatsSelected:
    indexDict[dfColumnsArr.index(repeat)] = [1]

  matrData = df.values.tolist()
  sDict = {}
  for i in range(len(matrData)):
    s = 0
    for ind in indexDict.keys():
      if matrData[i][ind] in indexDict[ind]:
        s += 1
    sDict[i] = s

  return sDict


def _updateResult(dataDict, nameArr, n):
  resDict = {}
  for key, value in dataDict.items():
    if value != 0:
      resDict[nameArr[key]] = 1 - value / n

  return sortDict(resDict)


def getRecommendationParams(
  categoriesSelected,
  sportDirectionsSelected,
  sportLevelsSelected,
  muscleGroupsSelected,
  needSportEquipSelected,
  hardnessSelected,
  repeatsSelected,
  df,
):
  nAll = 0
  if len(sportDirectionsSelected):
    nAll += 1
  if len(sportLevelsSelected):
    nAll += 1
  if len(muscleGroupsSelected):
    nAll += 1
  if len(needSportEquipSelected):
    nAll += 1

  nAll += len(categoriesSelected) + len(hardnessSelected) + len(repeatsSelected)
  if nAll == 0:
    recDict = _getDefaultResultParams(namesUI)
  else:
    recDict = _getRecommendationParams(
      categoriesSelected=categoriesSelected,
      sportDirectionsSelected=sportDirectionsSelected,
      sportLevelsSelected=sportLevelsSelected,
      muscleGroupsSelected=muscleGroupsSelected,
      needSportEquipSelected=needSportEquipSelected,
      hardnessSelected=hardnessSelected,
      repeatsSelected=repeatsSelected,
      df=df
    )

  return _updateResult(recDict, nameArr, nAll)


def _getRecommendationArr(likesArr, dislikesArr):
  recArr = None
  if len(likesArr) and len(dislikesArr):
    recArr = findByReaction(likesArr, dislikesArr)
  elif len(likesArr) and len(dislikesArr) == 0:
    recArr = findSimilarMany(likesArr)
  elif len(likesArr) == 0 and len(dislikesArr):
    recArr = findByReaction(likesArr, dislikesArr)
  else:
    recArr = []

  return recArr


def _splitMustMaybeDictArr(recDict):
  recMust, recMaybe = [], []
  for name, value in recDict.items():
    if value <= 0.2:
      recMust.append(name)
    else:
      recMaybe.append(name)

  return recMust, recMaybe


def giveRecommendationFull(
  likesSelected,
  dislikesSelected,
  categoriesSelected,
  sportDirectionsSelected,
  sportLevelsSelected,
  muscleGroupsSelected,
  needSportEquipSelected,
  hardnessSelected,
  repeatsSelected,
  df,
):
  recDict = getRecommendationParams(
    categoriesSelected=categoriesSelected,
    sportDirectionsSelected=sportDirectionsSelected,
    sportLevelsSelected=sportLevelsSelected,
    muscleGroupsSelected=muscleGroupsSelected,
    needSportEquipSelected=needSportEquipSelected,
    hardnessSelected=hardnessSelected,
    repeatsSelected=repeatsSelected,
    df=df
  )

  if len(likesSelected) or len(dislikesSelected):
    recLikesArr = _getRecommendationArr(likesSelected, dislikesSelected)
    recLikesDict = _fromArrDictToDict(recLikesArr)
    recDict = _compareLikesParams(recLikesDict, recDict)

  return _splitMustMaybeDictArr(sortDict(recDict))
