import re
import pymorphy3
from nltk.tokenize import word_tokenize


morph = pymorphy3.MorphAnalyzer(lang='ru')


def getNormalFormWord(word):
  return morph.parse(word)[0].normal_form


def delUselessSigns(phrase):
  return re.sub("[^а-яa-z0-9'№ &-,;.!?]", "", phrase)


def getNormalFormPhrase(phrase):
  wordArr = word_tokenize(phrase, language="russian")
  return ' '.join(getNormalFormWord(word) for word in wordArr)


def toLower(phrase: str):
  return phrase.lower()


def preprocessing(phrase: str):
  phrase = toLower(phrase)
  phrase = delUselessSigns(phrase)

  return getNormalFormPhrase(phrase)
