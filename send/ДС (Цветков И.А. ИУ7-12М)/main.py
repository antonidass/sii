import re
import nltk
nltk.download('punkt')

from cmds import *
from questions import *
from prepare_data import initPrefer, initFilter
from process import preprocessing


def _getAnswer():
  while True:
    answer = input().lower()
    if answer == "да":
      return True
    elif answer == "нет":
      return False
    printYesNoValidation()


def isAdd():
  printAddDefinition()
  return _getAnswer()


def processDefinition(dictPrefer, dictFilter, dataList):
  flag = 0

  # print(f'\nОбработано\n{dataList}\n')
  
  for data in dataList:
    for rule in RULE_ARR:
      regexp = re.compile(rule)
      match = regexp.match(data)
      
      if match is not None:
        resDict = match.groupdict()
        if rule == NOT_SIMILAR_TO_NAME:
          dictPrefer["dislikes"].append(resDict["name"])
        elif rule == SIMILAR_TO_NAME:
          dictPrefer["likes"].append(resDict["name"])
        if rule == WANT_CATEGORY_LEVEL3:
          dictPrefer["categories"].append(resDict["category_level3"])
        elif rule == WANT_CATEGORY_LEVEL2:
          dictPrefer["categories"].append(resDict["category_level2"])
        elif rule == WANT_CATEGORY_LEVEL1:
          dictPrefer["categories"].append(resDict["category_level1"])
        elif rule == WANT_SPORT_DIRECTION:
          dictPrefer["sport_directions"].append(resDict["sport_direction"])
        elif rule == WANT_SPORT_LEVEL:
          dictPrefer["sport_levels"].append(resDict["sport_level"])
        elif rule == WANT_MUSCLE_GROUP:
          dictPrefer["muscle_groups"].append(resDict["muscle_group"])
        elif rule == SPORT_EQUIP_EXTEND:
          dictPrefer["need_sport_equipment"].append(resDict["sport_equip"])
        elif rule == WANT_VERY_LOW_HARDNESS:
          dictPrefer["hardness"].append("Очень легко")
        elif rule == WANT_LOW_HARDNESS:
          dictPrefer["hardness"].append("Легко")
        elif rule == WANT_AVERAGE_HARDNESS:
          dictPrefer["hardness"].append("Нормально")
        elif rule == WANT_HIGH_HARDNESS:
          dictPrefer["hardness"].append("Сложно")
        elif rule == WANT_VERY_HIGH_HARDNESS:
          dictPrefer["hardness"].append("Очень сложно")
        elif rule == WANT_VERY_LOW_REPEATS:
          dictPrefer["repeats"].append("Очень мало подходов")
        elif rule == WANT_LOW_REPEATS:
          dictPrefer["repeats"].append("Мало подходов")
        elif rule == WANT_AVERAGE_REPEATS:
          dictPrefer["repeats"].append("Средне подходов")
        elif rule == WANT_HIGH_REPEATS:
          dictPrefer["repeats"].append("Много подходов")
        elif rule == WANT_VERY_HIGH_REPEATS:
          dictPrefer["repeats"].append("Очень много подходов")
        elif rule == NO_NEED_SPORT_LEVEL:
          dictFilter["no_sport_level"].append(resDict["sport_level"])
        elif rule == WHAT_ANY or rule == SHOW_ANY:
          pass

        flag = 1
        break

  if flag == 0:
    printMissunderstanding()
  # print(f'\nНачальное\n{dictPrefer}\n')
  # print(f'\nНачальное (фильтр)\n{dictFilter}\n')
  printFind(dictPrefer, dictFilter)


def dialog():
  dictPrefer = initPrefer()
  dictFilter = initFilter()
  
  while True:
    printDescribe()
    dataProcessed = preprocessing(input())
    processDefinition(dictPrefer, dictFilter, re.split('[,;.!?]', dataProcessed))

    while True:
      if isAdd():
        break
      else:
        printGoodBye()
        return


def main():
  printWelcome()
  dialog()


if __name__ == "__main__":
  main()
