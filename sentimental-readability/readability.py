from cs50 import get_string
import re

input = get_string("Text: ")

letters = 0
words = len(input.split())
sentences = len(re.split(r'[.!?]', input))-1

for update in range(len(input)):
    if input[update].isalpha():
        letters = letters + 1

L = letters * (100 / words)
S = sentences * (100 / words)

update1 = round(0.0588 * L - 0.296 * S - 15.8)

update2 = 0.0588 * (100 * float(letters) / float(words)) - 0.296 * (100 * float(sentences) / float(words)) - 15.8
print("update2:", update2)

print("Letters: ", letters)
print("Words: ", words)
print("Sentence: ", sentences)

if update1 >= 16:
    grade = "Grade 16+"
elif update1 <= 1:
    grade = "Before Grade 1"
else:
    grade = f"Grade {update1}"

print(grade)