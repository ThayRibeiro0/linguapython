import csv

from cs50 import SQL

db = SQL("sqlite:///favorites.db")

title = input("Title: ").strip()

rows = db.execute("SELECT title FROM favorites WHERE title LIKE ?", title)

for row in rows:
    print(row["title"])

# import csv

# from cs50 import SQL

# db = SQL("sqlite:///favorites.db")

# title = input("Title: ").strip()

# rows = db.execute("SELECT COUNT(*) AS counter FROM favorites WHERE title LIKE ?", title)

# row = rows[0]

# print(row["counter"])




















# import csv
# import re

# # #tirar duplicados
# # titles = []
# # titles = {}
# # counter = 0

# title = input("Title: ").strip().upper()

# counter = 0

# #leitura de dados no excel e ineri-los em lista
# with open("favorites.csv", "r") as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         if row["title"].strip().upper() == title:
#         # title = row["title"].strip().upper()

# #         if re.search("^(OFFICE|THE.OFFICE)$", title):
# #         # if "OFFICE" in title:
# #         # if title == "THE OFFICE" or title == "OFFICE":
#             counter += 1
# print(counter)

# # print(f"Number of people who like The Office: {counter}")

# #         # #ordernar de A a Z
# #         # titles.add(title)
# #         # if not title in titles:
# #         #     titles[title] = 0
# #         # titles[title] += 1

# #         # if not title in titles:
# #         #     titles.append(title)

# #         #tirar duplicados
# # #         if not row["title"] in titles:
# # #             titles.append(row["title"])

# # # #ordena pela ordem de valores
# # # def get_value(title):
# # #     return titles[title]

# # # # #key anonima e colca tbm em ordem os valores
# # # for title in sorted(titles, key=lambda title: titles[title], reverse=True):
# # #     print(title, titles[title])
