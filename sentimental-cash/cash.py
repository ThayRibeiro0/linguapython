from cs50 import get_float
# TODO

#starting value to counter in 0
cash = 0

#loop with user's input while it's in the condition
while True:
    n = get_float("Change owed: ")
    if n > 0:
        break
    print(n)

#round the change
change_owed = round(int(n * 100))

#counter +1 if the change'll has this conditions
while change_owed > 0:
    while change_owed >= 25:
        cash += 1
        change_owed -= 25
    while change_owed >= 10:
        cash += 1
        change_owed -= 10
    while change_owed >= 5:
        cash += 1
        change_owed -= 5
    while change_owed >= 1:
        change_owed -= 1
        cash += 1
print(cash)

