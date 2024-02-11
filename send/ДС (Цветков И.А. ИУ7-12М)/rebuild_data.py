from process import preprocessing

if __name__ == "__main__":
  with open("./data.csv") as f:
    data = f.read()

  items = data.split("\n")[1:]
  names = ""
  directions = ""
  levels = ""
  muscles = ""
  categories = ""

  for item in items:
    names += f"{preprocessing(item.split(';')[0])}|"
    directions += f"{preprocessing(item.split(';')[4])}|"
    levels += f"{preprocessing(item.split(';')[5])}|"
    muscles += f"{preprocessing(item.split(';')[6])}|"
    categories += f"{preprocessing(item.split(';')[7])}|"

  names = names[:-1].replace(" '", "\\'").replace(" & ", "&")
  print(names)
  print("\n")
  print(directions)
  print("\n")
  print(levels)
  print("\n")
  print(muscles)
  print("\n")
  print(categories)

