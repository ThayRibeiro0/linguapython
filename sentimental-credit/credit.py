from cs50 import get_string

while True:
    credit = get_string("Number: ")
    if credit.isdigit():
        break

newcredit = list(credit)

num0 = []
num1 = []

if len(newcredit) < 13 or len(newcredit) > 16:
    print("INVALID")

else:
    for MI in range(len(newcredit) - 2, -1, -2):
        tmpInt = int(newcredit[MI]) * 2

        if tmpInt > 9:
            tmpStr = str(tmpInt)
            tmpArr = list(tmpStr)
            tmpProd = int(tmpArr[0]) + int(tmpArr[1])
            num0.append(tmpProd)
        else:
            num0.append(int(newcredit[MI]) * 2)

    for MI in range(len(newcredit) - 1, -1, -2):
        num1.append(int(newcredit[MI]))

    a = sum(num1) + sum(num0)

    if a % 10 == 0:
        if len(newcredit) == 15 and int(newcredit[1]) == 7 and int(newcredit[1]) == 4 or int(newcredit[0]) == 3:
            print("AMEX")
        elif len(newcredit) == 16 and int(newcredit[0]) == 5 and int(newcredit[1]) >= 1 and int(newcredit[1]) <= 5:
            print("MASTERCARD")
        elif int(newcredit[0]) == 4:
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")