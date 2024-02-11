import pandas as pd
from dialog import df0, nameArr
from phrases import *
from prepare_data import find, transformFilterDict


def printOffer():
  print(DEFAULT_DATA)


def printWelcome():
  print(WELCOME_PHRASE)


def printGoodBye():
  print(GOODBYE_PHRASE)


def printDescribe():
  print(DESCRIBE)


def printYesNoValidation():
  print(YES_NO)


def printAddDefinition():
  print(ADD_DEFINITION)


def printMissunderstanding():
  print(MISUNDERSTANDING)


def printGiveMustRecomendation():
  print(MUST_LIKE)


def printGiveMayRecomendation():
  print(MAY_LIKE)


def filterDataFrame(df, filterDict):
  if len(filterDict["no_sport_level"]):
    for elem in filterDict["no_sport_level"]:
      df = df.loc[df["Требуемый уровень подготовки"] != elem]

  return df


def _printRecomendations(recArr: list, filterDict):
  df = df0.copy(deep=True)
  df = filterDataFrame(df, filterDict)
  iArr = []
  n = min(len(recArr), 7)
  i = 0

  while (i < n):
    if i >= len(recArr):
      break

    if recArr[i] in df["Название"].unique():
      iArr.append(df.index[df["Название"] == recArr[i]].tolist()[0])
    else:
      n += 1
    i += 1

  pd.set_option('display.width', 1000)
  print(df.loc[iArr, ["Название", "Время тренировки",
                       "Количество подходов", "Направленность",
                       "Требуемый уровень подготовки", "Группа мышц"]])


def printFind(dictPrefer, dictFilter):
  recMust, recMaybe = find(dictPrefer)
  dictFilter = transformFilterDict(dictFilter)

  if len(recMust):
    printGiveMustRecomendation()
    _printRecomendations(recMust, dictFilter)

  if len(recMaybe):
    printGiveMayRecomendation()
    _printRecomendations(recMaybe, dictFilter)

  if len(recMust) == 0 and len(recMaybe) == 0:
    printOffer()
    _printRecomendations(nameArr, dictFilter)
